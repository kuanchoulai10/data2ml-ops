# What, Why, When

## What is KServe?

KServe is an open-source, Kubernetes-native platform designed to streamline the deployment and management of machine learning (ML) models at scale. It provides a standardized interface for serving models across various ML frameworks, including TensorFlow, PyTorch, XGBoost, scikit-learn, ONNX, and even large language models (LLMs)[^1].

Built upon Kubernetes and Knative, KServe offers serverless capabilities such as autoscaling (including scaling down to zero)[^2], canary rollouts[^3], and model versioning. This architecture abstracts the complexities of infrastructure management, allowing data scientists and ML engineers to focus on developing and deploying models without delving into the intricacies of Kubernetes configurations.

For a comprehensive introduction to KServe, consider watching the following video:

<iframe width="560" height="315" src="https://www.youtube.com/embed/FX6naJLaq2Y" title="Exploring ML Model Serving with KServe" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Why KServe?

KServe caters to various roles within the ML lifecycle, offering tailored benefits:

For **Data Scientists**, With KServe's standardized APIs and support for multiple ML frameworks, data scientists can deploy models without worrying about the underlying infrastructure. Features like model explainability[^4] and inference graphs aid in understanding and refining model behavior.

For **ML Engineers**, KServe provides advanced deployment strategies, including canary rollouts and traffic splitting[^3], facilitating safe and controlled model updates. Its integration with monitoring tools like Prometheus and Grafana ensures observability and performance tracking[^5][^6].

For **MLOps Teams**, By leveraging Kubernetes' scalability and KServe's serverless capabilities, MLOps teams can manage model deployments efficiently across different environments, ensuring high availability and reliability.

## When to Use KServe?

### Deploying Models Across Diverse Frameworks

When working with a variety of ML frameworks, KServe's standardized serving interface[^7] allows for consistent deployment practices, reducing the overhead of managing different serving solutions.

### Scaling Inference Services Based on Demand

For applications with fluctuating traffic patterns, KServe's autoscaling features, including scaling down to zero during idle periods, ensure cost-effective resource utilization while maintaining responsiveness[^2].

### Implementing Safe and Controlled Model Updates

In scenarios requiring gradual model rollouts, KServe's support for canary deployments and traffic splitting enables testing new model versions with a subset of traffic before full-scale deployment[^3].

### Managing Complex Inference Pipelines

When dealing with intricate inference workflows involving preprocessing, postprocessing[^8], or chaining multiple models, KServe's inference graph[^9] feature allows for the composition of such pipelines, enhancing modularity and maintainability.


[^1]: [Model Serving Runtimes | KServe Docs](https://kserve.github.io/website/latest/modelserving/v1beta1/serving_runtime/)
[^2]: [Autoscale InferenceService with Knative Autoscaler | KServe Docs](https://kserve.github.io/website/latest/modelserving/autoscaling/autoscaling/)
[^3]: [Canary Rollout Example | KServe Docs](https://kserve.github.io/website/latest/modelserving/v1beta1/rollout/canary-example/)
[^4]: [InferenceService Explainer](https://kserve.github.io/website/latest/modelserving/explainer/explainer/)
[^5]: [Prometheus Metrics](https://kserve.github.io/website/latest/modelserving/observability/prometheus_metrics/)
[^6]: [Grafana Dashboards](https://kserve.github.io/website/latest/modelserving/observability/grafana_dashboards/)
[^7]: [Open Inference Protocol (V2 Inference Protocol)](https://kserve.github.io/website/latest/modelserving/data_plane/v2_protocol/)
[^8]: [How to write a custom transformer](https://kserve.github.io/website/latest/modelserving/v1beta1/transformer/torchserve_image_transformer/)
[^9]: [Inference Graph](https://kserve.github.io/website/latest/modelserving/inference_graph/)

[^2]: [KServe GitHub Repository](https://github.com/kserve/kserve)
[^3]: [Exploring ML Model Serving with KServe (YouTube)](https://www.youtube.com/watch?v=FX6naJLaq2Y)
[^4]: [KServe: Highly Scalable Machine Learning Deployment with Kubernetes](https://medium.com/data-science-collective/kserve-highly-scalable-machine-learning-deployment-with-kubernetes-aa7af0b71202)
[^5]: [KServe: Streamlining Machine Learning Model Serving in Kubernetes](https://blog.adyog.com/2025/01/16/kserve-streamlining-machine-learning-model-serving-in-kubernetes/)