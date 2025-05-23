import numpy as np
import pandas as pd
from google.cloud import storage
from joblib import dump
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

# Define constants for important information
BUCKET_NAME = "bikeshare-mlops-kcl"
MODEL_NAME = "model.joblib"
DATA_NAME = "hour.csv"

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)


def load_data(filename):
    df = pd.read_csv(filename)
    return df


def preprocess_data(df):
    df = df.rename(columns={
        'weathersit': 'weather',
        'yr': 'year',
        'mnth': 'month',
        'hr': 'hour',
        'hum': 'humidity',
        'cnt': 'count'
    })
    df = df.drop(columns=['instant', 'dteday', 'year'])
    cols = [
        'season', 'month', 'hour', 'holiday',
        'weekday', 'workingday', 'weather'
    ]
    for col in cols:
        df[col] = df[col].astype('category')
    df['count'] = np.log(df['count'])
    df_oh = df.copy()
    for col in cols:
        df_oh = one_hot_encoding(df_oh, col)
    X = df_oh.drop(
        columns=['atemp', 'windspeed', 'casual', 'registered', 'count'],
        axis=1
    )
    y = df_oh['count']
    return X, y


def one_hot_encoding(data, column):
    data = pd.concat(
        [
            data,
            pd.get_dummies(data[column], prefix=column, drop_first=True)
        ],
        axis=1
    )
    data = data.drop([column], axis=1)
    return data


def train_model(model_name, x_train, y_train):
    if model_name == 'random_forest_regressor':
        model = RandomForestRegressor()
    else:
        raise ValueError("Invalid model name.")

    pipeline = make_pipeline(model)
    pipeline.fit(x_train, y_train)
    return pipeline


def save_model_artifact(model_name, pipeline):
    dump(pipeline, MODEL_NAME)
    model_artifact = bucket.blob(MODEL_NAME)
    model_artifact.upload_from_filename(MODEL_NAME)


def main():
    model_name = "random_forest_regressor"
    df = load_data(f'gs:/{BUCKET_NAME}/{DATA_NAME}')
    X, y = preprocess_data(df)
    # model, rmse = train_model(X, y)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )
    pipeline = train_model(model_name, X_train, y_train)
    y_pred = pipeline.predict(X_test)
    save_model_artifact(model_name, pipeline)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print('RMSE:', rmse)


if __name__ == '__main__':
    main()
