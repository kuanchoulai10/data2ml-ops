# Integrate Ray Tune with Optuna, Imblearn, MLflow and MinIO

This guide walks you through how to use Ray Tune for hyperparameter tuning in a fraud detection model. The workflow includes:

1. Loading training data from MinIO
2. Defining a search space with **Optuna**, using over-sampling and down-sampling techniques like `AllKNN` and `SMOTE` specifically in `imblearn` packages to handle class imbalance.
3. Training an **XGBoost** binary classifier with boosters like `gbtree`, `gblinear`, and `dart`, and tuning hyperparameters such as lambda, alpha, and eta.
4. Logging metrics including accuracy, precision, recall, F1, and ROC AUC to both Ray Tune and MLflow.
5. Manually configuring MLflow to support parent-child runs, instead of using the default `MLflowLoggerCallback` and `setup_mlflow`
6. Retraining and saving the best model with the optimal hyperparameters after tuning.

Here is a full training transcipt.

??? note "Full Training Script"

    ```python title="training.py"
    --8<-- "./data2ml-ops/docs/ray/training.py"
    ```


## Import Packages

First, let’s import the required packages.

```python title="training.py"
--8<-- "./data2ml-ops/docs/ray/training.py:packages"
```

## MinIO Integration

We’ll use `pyarrow.fs.S3FileSystem` to interact with MinIO deployed on Kubernetes. There are two main tasks here.

1. Load training data stored in MinIO.
2. Save Ray Tune metadata (like checkpoints and logs) back to MinIO during the tuning process.

Here's how we configure the connection to MinIO using `S3FileSystem`, including the access key, secret key, and endpoint.

```python title="training.py"
--8<-- "./data2ml-ops/docs/ray/training.py:minio-fs"
```

These values should match what you specified when deploying MinIO on Kubernetes. For more details, refer to the configuration section below or revisit [this article](../minio/deployment.md).

??? info 

    ```yaml title="minio.yaml"
    --8<-- "./data2ml-ops/docs/minio/minio.yaml"
    ```

For other custom storage configuration, see [here](https://docs.ray.io/en/latest/train/user-guides/persistent-storage.html#custom-storage)[^1] for more.

### Get the Training Data

Since this is a demo project with a small dataset that fits into memory, we’ll use Pandas to read the CSV file directly through the configured filesystem.

If the dataset were larger or didn't fit in memory, we would use **Ray Data** instead. In the future, this could also integrate with **Feast Offline Feature Server**[^2] for more advanced feature management.


```python title="training.py"
--8<-- "./data2ml-ops/docs/ray/training.py:data"
```

### Define the RunConfig

Next, we configure where Ray Tune stores its metadata by setting the `storage_path` and `storage_filesystem` fields in `tune.RunConfig()`.

```python title="training.py"
--8<-- "./data2ml-ops/docs/ray/training.py:run_config"
```

## Optuna Integration (TuneConfig)

Ray Tune supports `OptunaSearch`[^3], which we’ll use to define the hyperparameter search strategy. A common way to define the search space is by passing a dictionary directly via the `param_space` argument in `tune.Tuner()`.

```python
tuner = tune.Tuner(
    objective,
    tune_config=tune.TuneConfig(
        metric="mean_loss",
        mode="min",
        search_alg=OptunaSearch(),
        num_samples=1000,
    ),
    param_space={
        "steps": 100,
        "width": tune.uniform(0, 20),
        "height": tune.uniform(-100, 100),
        "activation": tune.choice(["relu", "tanh"]),        
    },
)
results = tuner.fit()
```


### Define the Search Space

Sometimes, we want a more flexible search space—especially one with conditional logic. In such cases, we can pass a **define-by-run function** to `OptunaSearch()`, which dynamically defines the search space at runtime.[^3]

This function, typically called `space`, takes a `trial` object as input. We use `trial.suggest_*()` methods from Optuna, along with conditionals and loops, to construct the space.[^4]

This setup is helpful for handling more complex scenarios—such as including or excluding hyperparameters based on earlier choices.

```python title="training.py"
--8<-- "./data2ml-ops/docs/ray/training.py:space"
```

This `space()` function defines a **conditional hyperparameter search space** using Optuna's **define-by-run API**. Instead of declaring all parameters upfront, the search space is built dynamically as the `trial` runs. The function suggests different values for categorical and numerical hyperparameters, such as the `resampler` method (`allknn`[^5], `smote`[^6], or `passthrough`)[^5] and the `booster` type (`gbtree`, `gblinear`, or `dart`). Based on the chosen booster, additional parameters like `max_depth`, `eta`, and `grow_policy` are conditionally added.

Importantly, no actual model training or heavy computation is done inside this function—it only defines the search space structure.[^3] The function returns a dictionary of constant parameters (like the learning `objective` and `random_state`) to be merged later with the sampled hyperparameters. This design keeps the search logic modular and clean, separating the definition of search space from the training logic.

### Define the Search Algorithm

Now we configure the search algorithm using Optuna. We pass our `space()` function into `OptunaSearch`, specifying that we want to **maximize the F1 score**. To avoid exhausting system resources, we wrap it in a `ConcurrencyLimiter` that restricts parallel trials to 4. Finally, the `TuneConfig` object ties everything together, specifying the search algorithm and the total number of trials (`num_samples=100`) to explore.

```python title="training.py"
--8<-- "./data2ml-ops/docs/ray/training.py:optuna"
```

## MLflow Integration

Ray offers built-in integration with MLflow through [`MLflowLoggerCallback`](https://docs.ray.io/en/latest/tune/examples/tune-mlflow.html#mlflow-logger-api)[^7] and [`setup_mlflow`](https://docs.ray.io/en/latest/tune/examples/tune-mlflow.html#mlflow-setup-api)[^7]. These are convenient options, but they don't support **parent-child runs**[^8], which are essential for organizing experiments hierarchically. I've tried Databricks approach[^9] for setting up parent-child runs but it didn't work.

Thankfully, it's not difficult to manually integrate MLflow. So instead of using the built-in methods, we manually set up MLflow tracking inside the script. This integration spans multiple parts of the pipeline:

1. Set up the tracking URI and experiment in the driver process.
2. Start a parent run in the driver.
3. Set up and log to MLflow from within each trial (i.e., in the worker process).
4. After all trials finish, retrain the best model and log it under the parent run.


### Set up the Tracking URI and the Experiment in the Driver Process

We begin by setting the experiment name, the run name for this tuning session, and the address of the MLflow tracking server running inside the Kubernetes cluster.

```python title="training.py"
--8<-- "./data2ml-ops/docs/ray/training.py:constants"
```

```python title="training.py"
--8<-- "./data2ml-ops/docs/ray/training.py:mlflow"
```

These values should match what you specified when deploying MLflow on Kubernetes. For more details, refer to the configuration section below or revisit [this article](../mlflow/deployment.md).

??? info

    ```yaml title="tracking-server.yaml"
    --8<-- "./data2ml-ops/docs/mlflow/chart/templates/tracking-server.yaml:service"
    ```

    ```yaml title="values.yaml"
    --8<-- "./data2ml-ops/docs/mlflow/chart/values.yaml:tracking-server"
    ```

### Start the Parent Run in the Driver Process

When we launch `Tuner.fit()`, we also start an MLflow parent run inside the Ray **driver process**. Since each trial runs in a **worker process**, it won’t automatically inherit the MLflow context. So we need to explicitly pass the MLflow tracking URI, experiment name, and parent run ID into each worker so they can log their results correctly under the parent run.

```python linenums="1" hl_lines="3 8-10" title="training.py"
--8<-- "./data2ml-ops/docs/ray/training.py:main_tune"
```

### Integrate with MLflow in the Worker Process 

Each trial starts by configuring MLflow to point to the correct tracking server and parent run. Inside the trial, we begin a **nested (child) run** under the parent run. After training, we log hyperparameters and evaluation metrics, which will be associated with this specific trial.

```python linenums="1" hl_lines="3 5-7 42-46 62-63" title="training.py"
--8<-- "./data2ml-ops/docs/ray/training.py:training_function"
```

### Retrain and Save the Model with Best Params in the Driver Process

Once all trials finish, we return to the **driver process**, where we access the `ResultGrid`. This object contains all trial results. We then select the best set of hyperparameters (e.g., the one with the highest F1 score), retrain the model with those parameters, and log the final model to MLflow under the original parent run.

```python  linenums="1" hl_lines="48-54" title="training.py"
--8<-- "./data2ml-ops/docs/ray/training.py:retrain"
```


## Training Function (Trainable)

This is the training logic executed inside each worker process. Here's the typical workflow:

```python linenums="1" hl_lines="2 9-21 23-39 47-64" title="training.py"
--8<-- "./data2ml-ops/docs/ray/training.py:training_function"
```

1. Retrieve hyperparameters and the dataset (from `config` and `data`).
2. Split the dataset into training and validation sets.
3. Set up a pipeline with the selected resampling method and booster.
4. Train the model and log evaluation metrics and hyperparameters.

## Run Ray Tune

### Run the Hyperparameter Optimization

With the data ready, search space and Optuna strategy defined, and MLflow properly configured, we’re all set to launch Ray Tune via `tune.Tuner()`.

```python title="training.py"
--8<-- "./data2ml-ops/docs/ray/training.py:main_tune"
```


### Retrain and Save the Model with the Best Hyperparameters

After `tune.fit()` completes and all trials are evaluated, we move on to retraining the best model and logging it—just as explained in the [previous section](#retrain-and-save-the-model-with-best-params-in-the-driver-process).

Once everything is in place, the next step is to **submit the script to a Ray cluster**. There are several ways to do that, and we’ll cover them in the next article.

[^1]: [Configuring Persistent Storage | Ray Docs](https://docs.ray.io/en/latest/train/user-guides/persistent-storage.html#custom-storage)
[^2]: [Feast Offline Feature Server | Feast Docs](https://docs.feast.dev/reference/feature-servers/offline-feature-server)
[^3]: [Running Tune experiments with Optuna | Ray Docs](https://docs.ray.io/en/latest/tune/examples/optuna_example.html#conditional-search-spaces)
[^4]: [Pythonic Search Space | Optuna Docs](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/002_configurations.html)
[^5]: [AllKNN | imbalanced-learn Docs](https://imbalanced-learn.org/stable/references/generated/imblearn.under_sampling.AllKNN.html)
[^6]: [SMOTE | imbalanced-learn Docs](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html)
[^7]: [Using MLflow with Tune | Ray Docs](https://docs.ray.io/en/latest/tune/examples/tune-mlflow.html)
[^8]: [Understanding Parent and Child Runs in MLflow | MLflow Docs](https://mlflow.org/docs/latest/traditional-ml/hyperparameter-tuning-with-child-runs/part1-child-runs/)
[^9]: [Integrate MLflow and Ray | Databricks Docs](https://docs.databricks.com/gcp/en/machine-learning/ray/ray-mlflow#child-run-approach-for-logging)