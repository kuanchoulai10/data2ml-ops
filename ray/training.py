# --8<-- [start:packages]
# Import packages
import time
from datetime import datetime, timedelta
from pprint import pprint
from typing import Any, Dict, Optional

import pandas as pd
import pyarrow.fs
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from imblearn.under_sampling import AllKNN
from sklearn.metrics import (accuracy_score, average_precision_score, f1_score,
                             log_loss, precision_score, recall_score,
                             roc_auc_score)
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

import mlflow
import ray
from feast import FeatureStore
from ray import tune
from ray.tune.search import ConcurrencyLimiter
from ray.tune.search.optuna import OptunaSearch
# --8<-- [end:packages]


# --8<-- [start:minio-fs]
fs = pyarrow.fs.S3FileSystem(
    access_key="minio_user",
    secret_key="minio_password",
    scheme="http",
    endpoint_override="minio-api.minio.svc.cluster.local:9000"
)
# --8<-- [end:minio-fs]

# --8<-- [start:data]
# Get Training Data
with fs.open_input_file("ray/training_data.csv") as f:
    data = pd.read_csv(f)

# Alternative 1: Ray Data
# ds = ray.data.read_csv(
#     "s3://ray/training_data.csv",
#     filesystem=fs
# )

# Alternative 2: Feast
# now = datetime.now()
# two_days_ago = datetime.now() - timedelta(days=2)
# store = FeatureStore('.')
# fs_fraud_detection_v1 = store.get_feature_service('fraud_detection_v1')
# data = store.get_historical_features(
#     entity_df=f"""
#     select 
#         src_account as entity_id,
#         timestamp as event_timestamp,
#         is_fraud
#     from
#         feast-oss.fraud_tutorial.transactions
#     where
#         timestamp between timestamp('{two_days_ago.isoformat()}') 
#         and timestamp('{now.isoformat()}')""",
#     features=fs_fraud_detection_v1,
#     full_feature_names=False
# ).to_df()
# --8<-- [end:data]

# Configure Ray Tune
# --8<-- [start:space]
def space(trial) -> Optional[Dict[str, Any]]:
    """Define-by-run function to construct a conditional search space.
    Ensure no actual computation takes place here.

    Args:
        trial: Optuna Trial object
        
    Returns:
        Dict containing constant parameters or None
    """
    # Resampler
    resampler = trial.suggest_categorical("resampler", ["allknn", "smote", "passthrough"])
    
    # Booster
    booster = trial.suggest_categorical("booster", ["gbtree", "gblinear", "dart"])
    lmbd = trial.suggest_float("lambda", 1e-8, 1.0, log=True)
    alpha = trial.suggest_float("alpha", 1e-8, 1.0, log=True)
    if booster in ["gbtree", "dart"]:
        max_depth = trial.suggest_int("max_depth", 3, 10)
        eta = trial.suggest_float("eta", 1e-3, 0.3, log=True)
        gamma = trial.suggest_float("gamma", 1e-8, 1.0, log=True)
        grow_policy = trial.suggest_categorical("grow_policy", ["depthwise", "lossguide"])
    # Constants
    return {
        "objective": "binary:logistic",
        "random_state": 1025
    }
# --8<-- [end:space]

# --8<-- [start:training_function]
def training_function(
    config, data,
    run_id, mlflow_tracking_uri, experiment_name
):
    # Set up mlflow 
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    mlflow.set_experiment(experiment_name=experiment_name)

    # Split data
    X = data[[
        'has_fraud_7d',
        'num_transactions_7d',
        'credit_score',
        'account_age_days',
        'has_2fa_installed'
    ]]
    y = data['is_fraud']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y,
        random_state=config["random_state"]
    )
    
    # Define the resampler
    if config["resampler"] == "allknn":
        resampler = AllKNN()
    elif config["resampler"] == "smote":
        resampler = SMOTE()
    else:
        resampler = "passthrough"
    
    # Define the classifier
    new_config = {k: v for k, v in config.items() if k != "resampler"}
    classifier = XGBClassifier(**new_config)
    
    # Combine the resampler and classifier together
    model = Pipeline(steps=[
        ("resampler", resampler),
        ("classifier", classifier)
    ])
    
    # Train the model
    with mlflow.start_run(run_id=run_id):
        with mlflow.start_run(
            run_name=f"{config['resampler']}-{config['booster']}-{config['lambda']:.2f}-{config['alpha']:.2f}",
            nested=True
        ):
            model.fit(X_train, y_train)
            # Evaluate the model
            y_prob = model.predict_proba(X_test)
            y_prob = y_prob[:, 1]
            y_pred = (y_prob > 0.5).astype(int)
            metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred),
                "recall": recall_score(y_test, y_pred),
                "f1": f1_score(y_test, y_pred),
                "roc_auc": roc_auc_score(y_test, y_prob),
                "log_loss": log_loss(y_test, y_prob),
                "average_precision": average_precision_score(y_test, y_prob)
            }
            # Log the metrics and hyperparameters
            mlflow.log_params(config)
            mlflow.log_metrics(metrics)
            tune.report(metrics)
# --8<-- [end:training_function]

# --8<-- [start:optuna]
search_alg = OptunaSearch(space=space, metric="f1", mode="max")
search_alg = ConcurrencyLimiter(search_alg, max_concurrent=4)
tune_config = tune.TuneConfig(
    search_alg=search_alg,
    num_samples=100,
)
# --8<-- [end:optuna]

# --8<-- [start:constants]
EXPERIMENT_NAME = 'fraud_detection'
RUN_NAME = 'first'
TRACKING_URI = "http://tracking-server.mlflow.svc.cluster.local:5000"
# --8<-- [end:constants]
# --8<-- [start:mlflow]
mlflow.set_tracking_uri(TRACKING_URI)
if mlflow.get_experiment_by_name(EXPERIMENT_NAME) == None:
    mlflow.create_experiment(EXPERIMENT_NAME)
mlflow.set_experiment(EXPERIMENT_NAME)
# --8<-- [end:mlflow]
# --8<-- [start:run_config]
run_config = tune.RunConfig(
    name=EXPERIMENT_NAME,
    storage_path="ray/",
    storage_filesystem=fs
)
# --8<-- [end:run_config]

# --8<-- [start:main_tune]
# Run Ray Tune
ray.init()
with mlflow.start_run(run_name=RUN_NAME, nested=True) as run:
    tuner = tune.Tuner(
        tune.with_parameters(
            training_function,
            data=data,
            run_id=run.info.run_id,
            mlflow_tracking_uri=TRACKING_URI,
            experiment_name=EXPERIMENT_NAME
        ),
        tune_config=tune_config,
        run_config=run_config
    )
    results = tuner.fit()
# --8<-- [end:main_tune]

    # --8<-- [start:retrain]
    # Retrain the model with the hyperparameters with best result
    config = results.get_best_result(metric='f1', mode='max').config

    # 1. Split data
    X = data[[
        'has_fraud_7d',
        'num_transactions_7d',
        'credit_score',
        'account_age_days',
        'has_2fa_installed'
    ]]
    y = data['is_fraud']

    # 2. Define resampler
    if config["resampler"] == "allknn":
        resampler = AllKNN()
    elif config["resampler"] == "smote":
        resampler = SMOTE()
    else:
        resampler = "passthrough"

    # 3. Define classifier
    new_config = {k: v for k, v in config.items() if k != "resampler"}
    classifier = XGBClassifier(**new_config)

    # 4. Combine the resampler and classifier together
    model = Pipeline(steps=[
        ("resampler", resampler),
        ("classifier", classifier)
    ])

    # 5. Train and evaluate the model
    model.fit(X, y)
    y_prob = model.predict_proba(X)
    y_prob = y_prob[:, 1]
    y_pred = (y_prob > 0.5).astype(int)
    metrics = {
        "accuracy": accuracy_score(y, y_pred),
        "precision": precision_score(y, y_pred),
        "recall": recall_score(y, y_pred),
        "f1": f1_score(y, y_pred),
        "roc_auc": roc_auc_score(y, y_prob),
        "log_loss": log_loss(y, y_prob),
        "average_precision": average_precision_score(y, y_prob)
    }

    # 6. Log the hyperparameters, metrics and the model
    mlflow.log_params(config)
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        input_example=X.iloc[[0]],
        metadata={"version": f"{EXPERIMENT_NAME}_v1"}
    )
    # --8<-- [end:retrain]