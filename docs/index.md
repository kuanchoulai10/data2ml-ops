---
tags:
  - dbt
  - Feast
  - Ray
  - MLflow
  - KServe
  - MLOps
  - Kubernetes
---
# Fraud Detection: from DataOps to MLOps
## 💡 Highlights

=== "Data & Features"

    !!! success "Highlights"

        - [x] Built modular, testable SQL pipelines with **dbt**, enabling reproducible and version-controlled feature generation
        - [x] Registered features to **Feast (open source feature store)** for consistent usage in both **batch training** and **real-time serving**
        - [x] Enabled **feature backfilling** and **time-travel queries**, supporting **point-in-time** correctness for fraud detection models

=== "AutoML"

    !!! success "Highlights"

        - [x] Performed **distributed Bayesian hyperparameter optimization** using **Ray Tune + Optuna**, accelerating tuning efficiency at scale
        - [x] Handled imbalanced datasets using **imbalanced-learn** to dynamically apply over- and under-sampling strategies, improving model prediction performance
        - [x] Ensured **reproducibility** by tracking fixed random seeds, stratified sampling, and consistent data splits across trials

=== "Orchestration & Infrastructure"

    !!! success "Highlights"

        - [x] Deployed the entire pipeline on **Kubernetes**, enabling scalable, containerized execution of distributed services
        - [ ] (WIP) Orchestrated pipeline stages with **Airflow**, improving automation, observability, and task dependency management
        - [x] Integrated **MinIO (S3-compatible)** storage for storing intermediate features and trained models across components

=== "Experiment Tracking"

    !!! success "Highlights"

        - [x] Integrated **MLflow** to auto-log training parameters, metrics, and artifacts, enabling experiment **reproducibility** and **traceability**
        - [x] Versioned models and experiments using MLflow’s tracking server, enabling full **auditability** and **rollback**
        - [x] Stored **model artifacts** in **remote object storage (MinIO)**, making them accessible for downstream deployment

=== "Real-Time Inference"

    !!! success "Highlights"

        - [x] Deployed models as **gRPC** and **REST** endpoints using **KServe**, supporting diverse integration requirements
        - [x] Ensured **compatibility between training-time and serving-time** features via Feast’s online store integration
        - [x] Enabled **autoscaling** and **scale-to-zero**, optimizing cost for infrequently used models
        - [x] Configured **A/B testing traffic split**, allowing controlled experimentation in production deployments

---

In real-world machine learning projects, managing the workflow from **data transformation to model deployment** is often fragmented, error-prone, and hard to scale.

This project demonstrates how to streamline and automate the entire lifecycle—**from feature engineering to hyperparameter tuning, model tracking, and deployment**—using modern open source tools and **running fully on Kubernetes**.

The use case for this project is **fraud detection**, a high-impact and time-sensitive problem where **real-time inference** is critical. It serves as a practical demo of how to operationalize machine learning pipelines that are **version-controlled**, **reproducible**, and **ready for production**.

It’s designed to be:

- [x] **Reproducible** – All data transformations, features, and models are versioned via dbt, Feast, and MLflow
- [x] **Scalable** – Built on Kubernetes, enabling distributed training and resource orchestration across services
- [x] **Modular** – Each stage is decoupled and replaceable, promoting clear responsibility and reuse
- [x] **Open Source** – Fully built on open source tools like dbt, Feast, Ray, Optuna, MLflow, and KServe
- [x] **Portable** – Easily adapted to other use cases beyond fraud detection

Whether you're a data engineer, ML practitioner, or platform builder, this project offers a clear, working example of how to **bridge DataOps and MLOps** on a scalable, production-ready foundation.


##  🏗️ Architecture

<figure markdown="span">
    ![](./architecture.drawio.svg)
  <figcaption>Architecture (Click to Enlarge)</figcaption>
</figure>

=== "dbt"

    !!! success "Highlights"

        - [x] Developed incremental models to process data in minibatches, improving pipeline efficiency and reducing compute cost
        - [x] Implemented test coverage and schema validation, ensuring data quality across transformations
        - [x] Generated documentation automatically from dbt models, enhancing maintainability and team collaboration

=== "SQLMesh"

    !!! success "Highlights"

        Work In Progress

=== "Feast"

    !!! success "Highlights"

        - [x] Materialized online features to Redis, enabling real-time feature retrieval for low-latency inference
        - [x] Supported both batch and online inference by separating offline and online stores
        - [x] Enabled time-travel and point-in-time feature retrieval, ensuring training-serving consistency for fraud detection

=== "Airflow"

    !!! success "Highlights"

        Work In Progress

=== "Ray"

    !!! success "Highlights"

        - [x] Performed distributed Bayesian hyperparameter tuning using Ray Tune and Optuna, accelerating model search and training time
        - [x] Integrated imbalanced-learn to automatically select appropriate over- and under-sampling strategies, improving performance on imbalanced datasets
        - [x] Scaled training across nodes on Kubernetes, leveraging Ray cluster for efficient resource utilization

=== "MLflow"

    !!! success "Highlights"

        - [x] Integrated MLflow to auto-log parameters, metrics, and artifacts during training, enabling experiment tracking and auditability
        - [x] Logged final model as a versioned artifact, facilitating reproducible deployment and rollback
        - [x] Enabled reproducibility across environments by centralizing tracking and storage in a MinIO-based S3-compatible backend

=== "KServe"

    !!! success "Highlights"

        - [x] Deployed models as **gRPC** and **REST** endpoints using **KServe**, supporting diverse integration requirements
        - [x] Ensured **compatibility between training-time and serving-time** features via Feast’s online store integration
        - [x] Enabled **autoscaling** and **scale-to-zero**, optimizing cost for infrequently used models
        - [x] Configured **A/B testing traffic split**, allowing controlled experimentation in production deployments

## 🗂️ What's Inside?

```
.
├── dbt/       - Transform raw data into feature tables
├── sqlmesh/   - (Work In Progress)
├── feast/     - Define and manage features with Feast
├── airflow/   - (Work In Progress)
├── ray/       - Run distributed hyperparameter tuning with Ray and Optuna
├── mlflow/    - Track experiments and log models with MLflow
├── kserve/    - Deploy trained models using KServe
├── minio/     - Configure MinIO (S3-compatible) for model/data storage
```

