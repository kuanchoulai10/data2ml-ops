# Deploy Your Model on Kubernetes Using Kserve InferenceService

## Prerequisites

### S3 Credential

```yaml title="secret.yaml"
--8<-- "./data2ml-ops/kserve/secret.yaml"
```

```yaml title="sa.yaml"
--8<-- "./data2ml-ops/kserve/sa.yaml"
```

### Install grpcurl

```bash
brew install grpcurl
```

## Deploy Model

=== "REST"

    ```yaml title="inference-service-http.yaml"
    --8<-- "./data2ml-ops/kserve/inference-service-http.yaml"
    ```

    ```bash
    kubectl apply -f inference-service-http.yaml
    ```

=== "gRPC"

    ```yaml title="inference-service-grpc.yaml"
    --8<-- "./data2ml-ops/kserve/inference-service-grpc.yaml"
    ```

    ```bash
    kubectl apply -f inference-service-grpc.yaml
    ```


## Test Endpoints

=== "REST"

    ```bash
    curl -v \
    -H "Host: ${SERVICE_HOSTNAME}" \
    -H "Content-Type: application/json" \
    -d @./input_example.json \
    http://127.0.0.1:80/v2/models/mlflow-apple-demand/infer
    ```

    ???+ note "Result"

        ```
        *   Trying 127.0.0.1:80...
        * Connected to 127.0.0.1 (127.0.0.1) port 80
        > POST /v2/models/mlflow-apple-demand/infer HTTP/1.1
        > Host: {==mlflow-apple-demand.default.127.0.0.1.sslip.io==}
        > User-Agent: curl/8.7.1
        > Accept: */*
        > Content-Type: application/json
        > Content-Length: 1089
        > 
        * upload completely sent off: 1089 bytes
        < HTTP/1.1 200 OK
        < ce-endpoint: mlflow-apple-demand
        < ce-id: 9ddc841e-a8d4-405f-a7e4-73f7aa9bab09
        < ce-inferenceservicename: {==mlserver==}
        < ce-modelid: {==mlflow-apple-demand==}
        < ce-namespace: default
        < ce-requestid: 9ddc841e-a8d4-405f-a7e4-73f7aa9bab09
        < ce-source: io.seldon.serving.deployment.mlserver.default
        < ce-specversion: 0.3
        < ce-type: io.seldon.serving.inference.response
        < content-length: 240
        < content-type: application/json
        < date: Fri, 02 May 2025 04:06:58 GMT
        < server: istio-envoy
        < x-envoy-upstream-service-time: 247
        < 
        * Connection #0 to host 127.0.0.1 left intact
        {=={"model_name":"mlflow-apple-demand","id":"9ddc841e-a8d4-405f-a7e4-73f7aa9bab09","parameters":{"content_type":"np"},"outputs":[{"name":"output-1","shape":[1,1],"datatype":"FP32","parameters":{"content_type":"np"},"data":[1486.56298828125]}]}==}
        ```

=== "gRPC"

    ```bash
    grpcurl \
      -vv \
      -plaintext \
      -proto ${PROTO_FILE} \
      -authority ${SERVICE_HOSTNAME} \
      -d @ \
      ${INGRESS_HOST}:${INGRESS_PORT} \
      inference.GRPCInferenceService.ModelInfer \
      <<< $(cat "$INPUT_PATH")
    ```


## References

- [Deploy MLflow models with InferenceService | KServe](https://kserve.github.io/website/latest/modelserving/v1beta1/mlflow/v2/)
- [Deploy InferenceService with a saved model on S3 | KServe](https://kserve.github.io/website/latest/modelserving/storage/s3/s3/)
- [Deploy InferenceService with a saved model on GCS | KServe](https://kserve.github.io/website/latest/modelserving/storage/gcs/gcs/)
- [KServe Debugging Guide](https://kserve.github.io/website/latest/developer/debug/)
- [Develop ML model with MLflow and deploy to Kubernetes | MLflow](https://mlflow.org/docs/latest/deployment/deploy-model-to-kubernetes/tutorial/)

