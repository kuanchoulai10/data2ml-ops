# Write a Custom Transformer using Feast Online Feature Store
## Deploy InferenceService with Transformer using Feast Online Feature Store

To deploy an InferenceService with a custom transformer that uses the Feast online feature store, follow the detailed guide provided in the [KServe documentation](https://kserve.github.io/website/latest/modelserving/v1beta1/transformer/feast/).

This guide demonstrates how to integrate Feast with KServe, enabling feature retrieval and transformation during inference.

## Writing a Custom Transformer

A custom transformer is an implementation that retrieves features from the Feast online feature store and processes them as part of the inference pipeline. This approach allows dynamic feature retrieval and transformation based on the incoming inference requests.

### Steps to Implement a Custom Transformer

1. **Extend the Model Class**  
    Create a Python class that extends the `KServe.Model` base class. Implement the `preprocess` method to retrieve features dynamically based on the input data and append them to the inference request.

    Example:
    ```python
    from kserve import Model
    from feast import FeatureStore

    class CustomTransformer(Model):
         def __init__(self, name: str, feast_serving_url: str, feature_refs: list):
              super().__init__(name)
              self.store = FeatureStore(serving_url=feast_serving_url)
              self.feature_refs = feature_refs

         def preprocess(self, inputs: dict) -> dict:
              entity_rows = [{"key": input_data["key"]} for input_data in inputs["instances"]]
              features = self.store.get_online_features(
                    entity_rows=entity_rows,
                    features=self.feature_refs
              ).to_dict()
              inputs["features"] = features
              return inputs
    ```

2. **Containerize the Transformer**  
    Package the transformer code into a Docker container. Ensure the container includes all dependencies, such as the Feast SDK and KServe runtime.

    Example `Dockerfile`:
    ```dockerfile
    FROM python:3.8-slim
    WORKDIR /app
    COPY . /app
    RUN pip install kserve feast
    CMD ["python", "-m", "custom_transformer"]
    ```

3. **Deploy the Transformer with KServe**  
    Update the KServe InferenceService YAML to include the transformer container. Specify the container image built in the previous step.

    Example YAML:
    ```yaml
    apiVersion: "serving.kserve.io/v1beta1"
    kind: "InferenceService"
    metadata:
      name: "custom-transformer"
    spec:
      predictor:
         sklearn:
            storageUri: "gs://model-bucket/model"
      transformer:
         containers:
         - image: "gcr.io/your-project/custom-transformer:latest"
            name: transformer
            args:
            - --feast_serving_url
            - "feature-server-service.default.svc.cluster.local:6566"
            - --feature_refs
            - "feature1"
            - "feature2"
    ```

4. **Test the Deployment**  
    Send an inference request to the deployed InferenceService and verify that the transformer retrieves and appends the features correctly.

By following these steps, you can implement and deploy a custom transformer using Feast with KServe.
