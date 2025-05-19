# Deploy Ray Cluster on Kubernetes Using KubeRay

<figure markdown="span">
    ![](../architecture.drawio.svg)
  <figcaption>Architecture (Click to Enlarge)</figcaption>
</figure>

<!--  TODO: 第一段說明KubeRay是什麼 -->


## Install KubeRay Operator

Add kuberay helm repo

```bash
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
```

```
"kuberay" has been added to your repositories
```

Update kuberay helm repo

```bash
helm repo update
```

```
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "kuberay" chart repository
Update Complete. ⎈Happy Helming!⎈
```

Create kuberay namespace

```bash
kubectl create ns kuberay
```

```
namespace/kuberay created
```

Create KubeRay Operator

```bash
helm install kuberay-operator kuberay/kuberay-operator --version 1.3.0 -n kuberay
```

```
NAME: kuberay-operator
LAST DEPLOYED: Wed May 14 20:29:44 2025
NAMESPACE: kuberay
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Validate your KubeRay Operator pod is deployed successfully

```bash
kubectl get pods -n kuberay
```

```
NAME                                READY   STATUS    RESTARTS   AGE
kuberay-operator-66d848f5cd-5npp6   1/1     Running   0          23s
```

## Deploy a Ray Cluster

```bash
helm show values kuberay/ray-cluster > values.yaml
nano values.yaml
```

??? info "values.yaml"

    ```yaml title="values.yaml" hl_lines="80-87 163-169 241-247" linenums="1"
    --8<-- "./ray/values.yaml"
    ```

Install Ray Cluster

```bash
helm install raycluster kuberay/ray-cluster \
  --version 1.3.0 \
  --set 'image.tag=2.46.0-py310-aarch64' \
  -n kuberay \
  -f values.yaml
```

```
NAME: raycluster
LAST DEPLOYED: Wed May 14 20:31:53 2025
NAMESPACE: kuberay
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Once the RayCluster CR has been created, you can view it by running:

```bash
kubectl get rayclusters -n kuberay
```

```
NAME                 DESIRED WORKERS   AVAILABLE WORKERS   CPUS   MEMORY   GPUS   STATUS   AGE
raycluster-kuberay   1                                     2      3G       0               62s
```

To view Ray cluster’s pods, run the following command

```bash
kubectl get pods --selector=ray.io/cluster=raycluster-kuberay -n kuberay
```

```
NAME                                          READY   STATUS    RESTARTS   AGE
raycluster-kuberay-head-k6ktp                 1/1     Running   0          5m49s
raycluster-kuberay-workergroup-worker-zrxbj   1/1     Running   0          5m49s
```
