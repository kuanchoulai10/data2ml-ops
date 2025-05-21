# Deploy Ray Cluster on Kubernetes Using KubeRay

KubeRay simplifies managing Ray clusters on Kubernetes by introducing three key Custom Resource Definitions (CRDs): RayCluster, RayJob, and RayService. These CRDs make it easy to tailor Ray clusters for different use cases.[^1]

The **KubeRay operator** offers a Kubernetes-native approach to managing Ray clusters. A typical Ray cluster includes a **head node pod** and multiple **worker node pods**. With optional **autoscaling**, the operator can dynamically adjust the cluster size based on workload demands, adding or removing pods as needed.[^1]

<figure markdown="span">
  ![](https://docs.ray.io/en/latest/_images/ray_on_kubernetes.png)
  *What is KubeRay?*[^1]
</figure>

---

<figure markdown="span">
    ![](../architecture.drawio.svg)
  <figcaption>Architecture (Click to Enlarge)</figcaption>
</figure>

Setting up KubeRay is straightforward. This guide will walk you through installing the KubeRay operator and deploying your first Ray cluster using Helm. By the end, you'll have a fully functional Ray environment running on your Kubernetes cluster.[^2][^3]

## Install KubeRay Operator

Start by adding the KubeRay Helm repository to access the required charts:

```bash
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
```

```
"kuberay" has been added to your repositories
```

Update your local Helm chart list to ensure you're using the latest version:

```bash
helm repo update
```

```
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "kuberay" chart repository
Update Complete. ⎈Happy Helming!⎈
```

Next, create a namespace to manage KubeRay resources:

```bash
kubectl create ns kuberay
```

```
namespace/kuberay created
```

Now, install the KubeRay operator in the namespace. This sets up the controller to manage Ray clusters:

```bash
helm install kuberay-operator kuberay/kuberay-operator \
  --version 1.3.0 \
  -n kuberay
```

```
NAME: kuberay-operator
LAST DEPLOYED: Wed May 14 20:29:44 2025
NAMESPACE: kuberay
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Verify that the KubeRay operator pod is running:

```bash
kubectl get pods -n kuberay
```

```
NAME                                READY   STATUS    RESTARTS   AGE
kuberay-operator-66d848f5cd-5npp6   1/1     {==Running==}   0          23s
```

## Deploy a Ray Cluster

Export the default `values.yaml` file to customize memory settings. If you've encountered OOM issues, it's a good idea to increase memory allocation upfront.[^4]

```bash
helm show values kuberay/ray-cluster > values.yaml
nano values.yaml
```

??? info "values.yaml"

    ```yaml title="values.yaml" hl_lines="80-87 163-169 241-247" linenums="1"
    --8<-- "./data2ml-ops/docs/ray/values.yaml"
    ```

Install the Ray cluster using the customized `values.yaml`. Here, we're using the image tag `2.46.0-py310-aarch64` for Python 3.10, Ray 2.46.0, and MacOS ARM architecture. You can find all supported Ray images on Docker Hub.[^5]

```bash
helm install raycluster kuberay/ray-cluster \
  --version 1.3.0 \
  --set 'image.tag=2.46.0-py310-aarch64' \
  -n kuberay \
  -f values.yaml
```

```
NAME: {==raycluster==}
LAST DEPLOYED: Wed May 14 20:31:53 2025
NAMESPACE: {==kuberay==}
STATUS: {==deployed==}
REVISION: 1
TEST SUITE: None
```

Once the RayCluster CR is created, you can check its status:

```bash
kubectl get rayclusters -n kuberay
```

```
NAME                 DESIRED WORKERS   AVAILABLE WORKERS   CPUS   MEMORY   GPUS   STATUS   AGE
raycluster-kuberay   1                                     2      {==4G==}       0               62s
```

To view the running pods in your Ray cluster, use:

```bash
kubectl get pods --selector=ray.io/cluster=raycluster-kuberay -n kuberay
```

```
NAME                                          READY   STATUS    RESTARTS   AGE
raycluster-kuberay-head-k6ktp                 1/1     {==Running==}   0          5m49s
raycluster-kuberay-workergroup-worker-zrxbj   1/1     {==Running==}   0          5m49s
```

[^1]: [Ray on Kubernetes | Ray Docs](https://docs.ray.io/en/latest/cluster/kubernetes/index.html)
[^2]: [KubeRay Operator Installation | Ray Docs](https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/kuberay-operator-installation.html)
[^3]: [RayCluster Quickstart | Ray Docs](https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/raycluster-quick-start.html)
[^4]: [Out-Of-Memory Prevention | Ray Docs](https://docs.ray.io/en/latest/ray-core/scheduling/ray-oom-prevention.html)
[^5]: [rayproject/ray | Docker Hub](https://hub.docker.com/r/rayproject/ray/tags)
