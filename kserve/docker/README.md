# Feast Transformer Project Documentation

## Overview
This project contains a `FeastTransformer` implementation designed to work with KServe for preprocessing and transforming data before sending it to a model for inference. The repository includes several key files that facilitate containerization, dependency management, and the functionality of the transformer.


## 1. Using the Dockerfile

### Purpose of the Dockerfile
The `Dockerfile` is used to build a container image for deploying the `FeastTransformer` application. It ensures that all dependencies are installed and the application is configured to run in a consistent environment.

### How to Use the Dockerfile

1. **Build the Docker Image**:
    Run the following command in the directory containing the `Dockerfile`:
    ```bash
    docker build -t feast-transformer:latest .
    ```

2. **Run the Docker Container**:
    After building the image, you can run the container using:
    ```bash
    docker run -p 8080:8080 feast-transformer:latest
    ```

3. **Pass Required Arguments**:
    The `FeastTransformer` requires specific arguments to run. These can be passed as environment variables or command-line arguments when running the container. For example:
    ```bash
    docker run -p 8080:8080 feast-transformer:latest \
        --feast_url <feast_url> \
        --feast_entity_id <entity_id> \
        --feature_service <feature_service>
    ```

### What the Dockerfile Does

- Sets up a Python environment with the required dependencies.
- Copies the application code into the container.
- Configures the container to run the `FeastTransformer` application as the entry point.


## 2. Dependency Management with `pyproject.toml` and `uv.lock`

### `pyproject.toml`

The `pyproject.toml` file defines the project metadata and dependencies. It includes:
- **Project Metadata**: Information such as the project name, version, and description.
- **Dependencies**: Lists the required Python packages for the project, including:
  - `kserve`: For building and deploying the transformer with KServe.
  - `numpy`: For numerical computations.
  - `requests`: For making HTTP requests to the Feast feature store.
- **Editable Installation**: The project is marked as editable, allowing local development without reinstalling the package.

### `uv.lock`

The `uv.lock` file is a lockfile that ensures consistent dependency resolution across environments. It includes:

- **Resolved Dependencies**: Lists all dependencies, their versions, and their sources.
- **Compatibility Information**: Specifies Python version constraints and platform-specific details.
- **Dependency Tree**: Provides a detailed breakdown of direct and transitive dependencies.

To install dependencies using these files, run:

```bash
pip install -r requirements.txt
```

or use a tool like `poetry` or `pip-tools` if configured.


## 3. Purpose of the `feast_transformer`

### What is the `FeastTransformer`?

The `FeastTransformer` is a Python class that preprocesses incoming data for machine learning models deployed with KServe. It integrates with the Feast feature store to retrieve feature data and transform it into a format suitable for model inference.

### Key Features

- **Feature Retrieval**: Connects to a Feast online feature store to fetch features based on entity IDs.
- **Data Transformation**: Processes the retrieved features and formats them into a structure compatible with the model's input requirements.
- **Protocol Support**: Supports both REST and gRPC protocols for communication with the model server.

### How It Works

1. **Initialization**:
    - The transformer is initialized with parameters such as the Feast URL, entity ID, feature service name, and model server details.
2. **Preprocessing**:
    - Extracts entity IDs from the incoming payload.
    - Queries the Feast feature store for features.
    - Formats the features into a model-compatible structure.

3. **Integration with KServe**:
    - The transformer is deployed as part of a KServe inference pipeline, acting as a preprocessing step before the model server.

### Example Use Case

The `FeastTransformer` can be used in scenarios where real-time feature retrieval and preprocessing are required, such as:

- Fraud detection systems.
- Recommendation engines.
- Predictive maintenance applications.


## Conclusion

This repository provides a robust framework for deploying a `FeastTransformer` with KServe. By leveraging the `Dockerfile`, `pyproject.toml`, and `uv.lock`, you can ensure a consistent and reliable deployment process. The `FeastTransformer` itself is a powerful tool for integrating feature stores into machine learning inference pipelines.
