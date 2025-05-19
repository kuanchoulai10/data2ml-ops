# Integrate Ray Tune with Optuna, Imblearn, MLflow and MinIO

??? note "Full Training Script"

    ```python title="training.py"
    --8<-- "./ray/training.py"
    ```

1. Import packages
2. Get the training data
3. Define the TuneConfig, RunConfig and Trainable
4. Run the Ray Tune
5. Retrain and save the model with the best hyperparameters

## Import Packages

```python title="training.py"
--8<-- "./ray/training.py:packages"
```

## MinIO Integration


```python title="training.py"
--8<-- "./ray/training.py:minio-fs"
```

??? info 

    ```yaml title="minio.yaml"
    --8<-- "./minio/minio.yaml"
    ```

### Get the Training Data

```python title="training.py"
--8<-- "./ray/training.py:data"
```

### Define the RunConfig

```python title="training.py"
--8<-- "./ray/training.py:run_config"
```

## Optuna Integration (TuneConfig)

### Define the Search Space

```python title="training.py"
--8<-- "./ray/training.py:space"
```

### Define the Search Algorithm
```python title="training.py"
--8<-- "./ray/training.py:optuna"
```

## MLflow Integration

### Set up the Tracking URI and the Experiment in the Driver Process

```python title="training.py"
--8<-- "./ray/training.py:constants"
```

??? info

    ```yaml title="tracking-server.yaml"
    --8<-- "./mlflow/chart/templates/tracking-server.yaml:service"
    ```

    ```yaml title="values.yaml"
    --8<-- "./mlflow/chart/values.yaml:tracking-server"
    ```

```python title="training.py"
--8<-- "./ray/training.py:mlflow"
```

### Start the Parent Run in the Driver Process

```python linenums="1" hl_lines="3 8-10" title="training.py"
--8<-- "./ray/training.py:main_tune"
```

### Integrate with MLflow in the Worker Process 

```python linenums="1" hl_lines="3 5-7 42-46 62-63" title="training.py"
--8<-- "./ray/training.py:training_function"
```

- 接收來自Driver Process的arguments (run_id, mlflow_tracking_uri, experiment_name)
- Set up the tracking uri and the experiment
- Start the nested run
- Log hyperparameters and metrics

### Retrain and Save the Model with Best Params in the Driver Process

```python  linenums="1" hl_lines="48-54" title="training.py"
--8<-- "./ray/training.py:retrain"
```


## Training Function (Trainable)

```python linenums="1" hl_lines="2 9-21 23-39 47-64" title="training.py"
--8<-- "./ray/training.py:training_function"
```

- Get the hyperparameters and the training data
- Split the data
- Define the model (integrate with Imbalanced Learn and XGboost)
- Train and evalute the model

## Run Ray Tune

### Run the Hyperparameter Optimization

```python title="training.py"
--8<-- "./ray/training.py:main_tune"
```

`Tuner`

- `Trainable`: `tune.with_parameters()`
- `TuneConfig`
- `RunConfig`

### Retrain and Save the Model with the Best Hyperparameters

```python title="training.py"
--8<-- "./ray/training.py:retrain"
```
