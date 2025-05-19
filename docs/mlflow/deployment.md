# Deploy MLflow on Kubernetes

<figure markdown="span">
    ![](../architecture.drawio.svg)
  <figcaption>Architecture (Click to Enlarge)</figcaption>
</figure>


## Artifact Store (MinIO)

First deploy an S3-compatible object store - MinIO for our MLflow artifact store to store artifacts like figures, models, reports, etc. See [here](../minio/minio-installation.md) for deploying MinIO.

After deploying MinIO and the `mlflow` bucket created, in MLflow's helm chart, we could specify artifact store's configuration

```yaml linenums="1" title="values.yaml"
--8<-- "./mlflow/chart/values.yaml:artifact-store"
```

## Backend Store

```yaml linenums="1" title="values.yaml"
--8<-- "./mlflow/chart/values.yaml:backend-store"
```

```yaml linenums="1" title="backend-store.yaml"
--8<-- "./mlflow/chart/templates/backend-store.yaml:deployment"
```

```yaml linenums="1" title="backend-store.yaml"
--8<-- "./mlflow/chart/templates/backend-store.yaml:service"
```

## Tracking Server

```yaml linenums="1" title="values.yaml"
--8<-- "./mlflow/chart/values.yaml:tracking-server"
```

```yaml linenums="1" title="tracking-server.yaml"
--8<-- "./mlflow/chart/templates/tracking-server.yaml:deployment"
```

```yaml linenums="1" title="tracking-server.yaml"
--8<-- "./mlflow/chart/templates/tracking-server.yaml:service"
```
