# Deploy Your Model on Kubernetes

## Prerequisites

- MinIO must be running and contain a bucket named `mlflow`.  
    - If you haven’t set it up, see [MinIO Deployment](../minio/deployment.md) for instructions.
- A Ray Tune job must have completed and logged the best model to MLflow, which was stored in MinIO. If you haven’t done this yet, refer to the following guides:
    - [MLflow Deployment](../mlflow/deployment.md): Set up the MLflow tracking server and configure MinIO as the artifact store.
    - [Ray Deployment](../ray/deployment.md): Deploy a Ray cluster on Kubernetes.
    - [Ray Tune Integration Guide](../ray/ray-tune.md): Learn how to integrate Ray Tune with MLflow, Optuna imbalanced-learn, XGBoost and MinIO.
    - [Ray Tune Job Submission](../ray/ray-job.md): Run the tuning job and log the best model to MLflow.
- `gRPCurl` installed
    ```bash
    brew install grpcurl
    ```


This guide walks you through how to deploy the model you previously trained with Ray and logged to MinIO via MLflow. You'll learn how to serve it using KServe with both REST and gRPC endpoints, and enable autoscaling—including scale-to-zero support.

## Grant KServe Permission to Load Models from MinIO [^1]

To allow KServe to pull models from MinIO (or any S3-compatible storage), you'll need to provide access credentials via a Kubernetes `Secret` and bind it to a `ServiceAccount`. Then, reference that service account in your `InferenceService`.

Start by creating a `Secret` that holds your S3 credentials. This secret should include your access key and secret key, and be annotated with the MinIO endpoint and settings to disable HTTPS if you're working in a local or test environment.


```yaml title="secret.yaml" linenums="1" hl_lines="4"
--8<-- "./kserve/secret.yaml"
```

These values should match what you specified when deploying MinIO on Kubernetes. For more details, refer to the configuration section below or revisit [this article](../minio/deployment.md).

??? info 

    ```yaml title="minio.yaml"
    --8<-- "./minio/minio.yaml"
    ```

Next, create a `ServiceAccount` that references the secret. This will allow KServe to inject the credentials when pulling models.

```yaml title="sa.yaml" linenums="1" hl_lines="4 6"
--8<-- "./kserve/sa.yaml"
```

Finally, define an `InferenceService` that uses the `ServiceAccount` and points to the model artifact stored in MinIO. In this example, we are deploying a model saved in MLflow format using the v2 inference protocol.

=== "REST"

    ```yaml title="inference-service-rest-v2.yaml" linenums="1" hl_lines="15"
    --8<-- "./kserve/inference-service-rest-v2.yaml"
    ```

=== "gRPC"

    ```yaml title="inference-service-grpc-v2.yaml" linenums="1" hl_lines="19"
    --8<-- "./kserve/inference-service-grpc-v2.yaml"
    ```



##  Deploy the Fraud Detection MLflow Model with InferenceService[^2][^3]

This example shows how to deploy your trained MLflow model on KServe using both the REST and gRPC protocol. The `InferenceService` configuration specifies the model format (`mlflow`), the s2 inference protocol, and the S3 URI where the model is stored. The `serviceAccountName` field allows KServe to access the model stored in MinIO using the credentials provided earlier.


=== "REST"

    ```yaml title="inference-service-rest-v2.yaml"
    --8<-- "./kserve/inference-service-rest-v2.yaml"
    ```
    
    Apply the configuration using `kubectl`:

    ```bash
    kubectl apply -f inference-service-rest-v2.yaml
    ```

    Once deployed, KServe will expose a REST endpoint where you can send inference requests. You can verify the service status using:
    
    ```bash
    kubectl get inferenceservice fraud-detection-http
    ```

=== "gRPC"

    ```yaml title="inference-service-grpc-v2.yaml"
    --8<-- "./kserve/inference-service-grpc-v2.yaml"
    ```

    Apply the configuration using `kubectl`:

    ```bash
    kubectl apply -f inference-service-grpc-v2.yaml
    ```

    Once deployed, KServe will expose a gRPC endpoint where you can send inference requests. You can verify the service status using: 
    
    ```bash
    kubectl get inferenceservice fraud-detection-grpc
    ```

Make sure the `storageUri` matches the path where your model is saved.

During deployment, you may encounter a few common issues:

1. The model fails to load inside the pod during the storage initialization phase[^4]. This is usually a permission issue—make sure your access credentials are correctly configured as shown in the section above.
2. Sometimes the model loads successfully into the model server, but inference requests still fail. This could be due to:
    - **A mismatch between the model version and the model server runtime**. In this case, try explicitly setting the `runtimeVersion`[^5].
    - **Incorrect port settings**, which prevent the server from responding properly.
    - **Architecture mismatch**—for example, if you trained the model on a Mac (ARM64) but are using an x86-based KServe runtime image.
    - **Deployment in a control plane namespace**. Namespaces labeled with `control-plane` are skipped by KServe’s webhook to avoid privilege escalation. This prevents the storage initializer from being injected into the pod, leading to errors like: `No such file or directory: '/mnt/models'`.

## Test the Endpoints

[Determine the ingress IP and port](https://kserve.github.io/website/latest/get_started/first_isvc/#4-determine-the-ingress-ip-and-ports):


```bash
export INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')
```

This step retrieves the external IP address of the Istio Ingress Gateway and stores it in `INGRESS_HOST`, and extracts the port named `http2` to set as `INGRESS_PORT`, allowing you to construct the full service endpoint for sending inference requests.

=== "REST"

    Set the required environment variables for the HTTP inference request:

    ```bash
    export INPUT_PATH=input-example-rest-v2.json
    export SERVICE_HOSTNAME=$(kubectl get inferenceservice fraud-detection-rest -o jsonpath='{.status.url}' | cut -d "/" -f 3)
    ```

    ??? note "input-example-rest-v2.json"

        ```bash title="input-example-rest-v2.json"
        --8<-- "./kserve/input-example-rest-v2.json"
        ```

    ```bash title="test-commands.txt"
    --8<-- "./kserve/test-commands.txt:rest"
    ```

    !!! success "Expected Output"

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

    Download the `open_inference_grpc.proto` file:

    ```bash
    curl -O https://raw.githubusercontent.com/kserve/open-inference-protocol/main/specification/protocol/open_inference_grpc.proto
    ```

    ??? note "open_inference_grpc.proto"

        ```proto title="open_inference_grpc.proto" linenums="1" hl_lines="19-45 138-206 208-260"
        --8<-- "https://raw.githubusercontent.com/kserve/open-inference-protocol/main/specification/protocol/open_inference_grpc.proto"
        ```

    Downloading this `.proto` file gives you the standard gRPC interface definition for the Open Inference Protocol. It allows your client or server to communicate with ML model servers using a unified API.

    Set the required environment variables for the gRPC inference request:

    ```bash
    export PROTO_FILE=open_inference_grpc.proto
    export INPUT_PATH=input-example-grpc-v2.json
    export SERVICE_HOSTNAME=$(kubectl get inferenceservice fraud-detection-grpc -o jsonpath='{.status.url}' | cut -d "/" -f 3)
    ```

    These variables specify the protobuf schema for gRPC, the input payload to send, and the target hostname for routing the request through the ingress gateway.

    ??? note "input-example-grpc-v2.json"

        ```bash title="input-example-grpc-v2.json"
        --8<-- "./kserve/input-example-grpc-v2.json"
        ```

    ```bash title="test-commands.txt"
    --8<-- "./kserve/test-commands.txt:grpc"
    ```

    !!! success "Expected Output"

        ```
        TODO: Add expected output for gRPC inference request
        ```

[^1]: [Deploy InferenceService with a saved model on S3 | KServe](https://kserve.github.io/website/latest/modelserving/storage/s3/s3/)
[^2]: [Deploy MLflow models with InferenceService | KServe](https://kserve.github.io/website/latest/modelserving/v1beta1/mlflow/v2/)
[^3]: [Develop ML model with MLflow and deploy to Kubernetes | MLflow](https://mlflow.org/docs/latest/deployment/deploy-model-to-kubernetes/tutorial/)
[^4]: [Storage Initializer fails to download model | KServe Debugging Guide](https://kserve.github.io/website/latest/developer/debug/#storage-initializer-fails-to-download-model)
[^5]: [Explicitly Specify a Runtime Version](https://kserve.github.io/website/latest/modelserving/servingruntimes/#using-servingruntimes)

