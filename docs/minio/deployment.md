# Deploy MinIO on Kubernetes

<figure markdown="span">
    ![](../architecture.drawio.svg)
  <figcaption>Architecture (Click to Enlarge)</figcaption>
</figure>

## Deployment

```yaml linenums="1" title="minio.yaml" hl_lines="20-23 25-28 30-33"
--8<-- "./data2ml-ops/minio/minio.yaml:deployment"
```

## Job

```yaml linenums="1" title="minio.yaml" hl_lines="2 15 18-25 27-42"
--8<-- "./data2ml-ops/minio/minio.yaml:job"
```

## Services

```yaml linenums="1" title="minio.yaml" hl_lines="4 11-14 19 26-28"
--8<-- "./data2ml-ops/minio/minio.yaml:services"
```