# Deploy Feast on Kubernetes

- Offline Store: BigQuery
- Registry: postgresql
- Online Store: Redis

<figure markdown="span">
    ![](../architecture.drawio.svg)
  <figcaption>Architecture (Click to Enlarge)</figcaption>
</figure>

```
minikube start --cpus=4 --memory=7000 --driver=docker
```

## Build Feast Docker Image Locally

go to `feast/` folder. 就會看到以下檔案

```Dockerfile title="Dockerfile"
--8<-- "./feast-2/Dockerfile"
```

```yaml title="feature_store.yaml" linenums="1" hl_lines="2-4 11-15"
--8<-- "./feast-2/feature_store.yaml"
```

```sh title="entrypoint.sh"
--8<-- "./feast-2/entrypoint.sh"
```


Build image

```bash
docker buildx build \
  --platform linux/amd64 \
  -t feast:v0.1.0 \
  -t feast:latest \
  .
```

我是使用MacOS，我們使用`docker buildx`，for amd64架構

確認是否建置成功

```bash
docker images --filter=reference="feast*"
```

```
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
{==feast==}        v0.1.0    {==436abcf371e9==}   55 seconds ago   596MB
```

## Load Image into Minikube Cluster

在Local進入minikube

```bash
minikube ssh
```

查看目前minikube裡有的images，沒有feast
```bash
docker@minikube:~$ docker images
```

!!! success "Expected Output"

    ```
    REPOSITORY                                TAG        IMAGE ID       CREATED         SIZE
    registry.k8s.io/kube-apiserver            v1.30.0    181f57fd3cdb   12 months ago   112MB
    registry.k8s.io/kube-controller-manager   v1.30.0    68feac521c0f   12 months ago   107MB
    registry.k8s.io/kube-proxy                v1.30.0    cb7eac0b42cc   12 months ago   87.9MB
    registry.k8s.io/kube-scheduler            v1.30.0    547adae34140   12 months ago   60.5MB
    registry.k8s.io/etcd                      3.5.12-0   014faa467e29   15 months ago   139MB
    registry.k8s.io/coredns/coredns           v1.11.1    2437cf762177   21 months ago   57.4MB
    registry.k8s.io/pause                     3.9        829e9de338bd   2 years ago     514kB
    gcr.io/k8s-minikube/storage-provisioner   v5         ba04bb24b957   4 years ago     29MB
    docker@minikube:~$ 
    ```

在local開啟另個terminal，將local的docker image載入到minikube cluster裡

```bash
minikube image load feast:v0.1.0
```


回到minikube裡，查看images，有feast了

```bash
docker@minikube:~$ docker images
```

!!! success "Expected Output"

    ```
    REPOSITORY                                TAG        IMAGE ID       CREATED          SIZE
    {==feast==}                                     v0.1.0     {==436abcf371e9==}   33 minutes ago   596MB
    registry.k8s.io/kube-apiserver            v1.30.0    181f57fd3cdb   12 months ago    112MB
    registry.k8s.io/kube-controller-manager   v1.30.0    68feac521c0f   12 months ago    107MB
    registry.k8s.io/kube-scheduler            v1.30.0    547adae34140   12 months ago    60.5MB
    registry.k8s.io/kube-proxy                v1.30.0    cb7eac0b42cc   12 months ago    87.9MB
    registry.k8s.io/etcd                      3.5.12-0   014faa467e29   15 months ago    139MB
    registry.k8s.io/coredns/coredns           v1.11.1    2437cf762177   21 months ago    57.4MB
    registry.k8s.io/pause                     3.9        829e9de338bd   2 years ago      514kB
    gcr.io/k8s-minikube/storage-provisioner   v5         ba04bb24b957   4 years ago      29MB
    ```


## K8S

### Registry

```yaml title="registry.yaml"
--8<-- "./feast-2/k8s/registry.yaml"
```

### Online Store

```yaml title="online-store.yaml"
--8<-- "./feast-2/k8s/online-store.yaml"
```


### Secret

#### Create GCP Service Account Key

確認Project id

```bash
gcloud config get-value project
```

!!! success "Expected Output"

    ```
    mlops-437709
    ```


建立Service Account

```bash
gcloud iam service-accounts create feast-sa \
    --display-name "Feast Service Account"
```

!!! success "Expected Output"

    ```
    Reauthentication required.
    Please enter your password:
    Reauthentication successful.
    Created service account [feast-sa].
    ```

替Service Account加上BigQuery權限

```bash
gcloud projects add-iam-policy-binding mlops-437709 \
    --member="serviceAccount:feast-sa@mlops-437709.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"
```

??? success "Expected Output"

    ```
    [1] EXPRESSION=request.time < timestamp("2025-04-09T07:42:05.596Z"), TITLE=cloudbuild-connection-setup
    [2] None
    [3] Specify a new condition
    The policy contains bindings with conditions, so specifying a condition is required when adding a binding. Please specify a condition.:  2

    Updated IAM policy for project [mlops-437709].
    bindings:
    - members:
      - serviceAccount:service-362026176730@gcp-sa-aiplatform-cc.iam.gserviceaccount.com
      role: roles/aiplatform.customCodeServiceAgent
    - members:
      - serviceAccount:service-362026176730@gcp-sa-vertex-op.iam.gserviceaccount.com
      role: roles/aiplatform.onlinePredictionServiceAgent
    - members:
      - serviceAccount:service-362026176730@gcp-sa-aiplatform.iam.gserviceaccount.com
      role: roles/aiplatform.serviceAgent
    - members:
      - serviceAccount:service-362026176730@gcp-sa-artifactregistry.iam.gserviceaccount.com
      role: roles/artifactregistry.serviceAgent
    - members:
      - serviceAccount:feast-sa@mlops-437709.iam.gserviceaccount.com
      role: roles/bigquery.admin
    - members:
      - serviceAccount:362026176730@cloudbuild.gserviceaccount.com
      role: roles/cloudbuild.builds.builder
    - members:
      - serviceAccount:service-362026176730@gcp-sa-cloudbuild.iam.gserviceaccount.com
      role: roles/cloudbuild.serviceAgent
    - members:
      - serviceAccount:service-362026176730@containerregistry.iam.gserviceaccount.com
      role: roles/containerregistry.ServiceAgent
    - members:
      - serviceAccount:362026176730-compute@developer.gserviceaccount.com
      role: roles/editor
    - members:
      - serviceAccount:service-362026176730@gcp-sa-firestore.iam.gserviceaccount.com
      role: roles/firestore.serviceAgent
    - members:
      - serviceAccount:362026176730@cloudbuild.gserviceaccount.com
      role: roles/iam.serviceAccountUser
    - members:
      - serviceAccount:service-362026176730@cloud-ml.google.com.iam.gserviceaccount.com
      role: roles/ml.serviceAgent
    - members:
      - user:edison@kcl10.com
      role: roles/owner
    - members:
      - serviceAccount:service-362026176730@gcp-sa-pubsub.iam.gserviceaccount.com
      role: roles/pubsub.serviceAgent
    - members:
      - serviceAccount:362026176730@cloudbuild.gserviceaccount.com
      role: roles/run.admin
    - members:
      - serviceAccount:service-362026176730@serverless-robot-prod.iam.gserviceaccount.com
      role: roles/run.serviceAgent
    - condition:
        expression: request.time < timestamp("2025-04-09T07:42:05.596Z")
        title: cloudbuild-connection-setup
      members:
      - serviceAccount:service-362026176730@gcp-sa-cloudbuild.iam.gserviceaccount.com
      role: roles/secretmanager.admin
    etag: BwY0his6v7Y=
    version: 3
    ```

建立Key

```bash
gcloud iam service-accounts keys create feast-gcp-key.json \
    --iam-account=feast-sa@mlops-437709.iam.gserviceaccount.com
```

!!! success "Expected Output"

    ```
    created key [a2609fffff05f5fdf311de233f1a2e1e89288ab5] of type [json] as [feast-gcp-key.json] for [feast-sa@mlops-437709.iam.gserviceaccount.com]
    ```

#### Create K8S Secret

```bash
cat feast-gcp-key.json | base64
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: feast-gcp-key
  namespace: feast
type: Opaque
data:
  key.json: {==<base64 encoded string>==}
```

### Online Feature Server

```yaml title="online-feature-server.yaml"
--8<-- "./feast-2/k8s/online-feature-server.yaml"
```


## Deploy Your Feast Architecture

```sh title="install.sh"
--8<-- "./feast-2/k8s/install.sh"
```

```bash
./install.sh
```

!!! success "Expected Output"

    ```
    Step 0: Create feast Namespace
    namespace/feast created

    Step 1: Deploy Online Store
    deployment.apps/online-store created
    service/online-store created
    Waiting for deployment "online-store" rollout to finish: 0 of 1 updated replicas are available...
    deployment "online-store" successfully rolled out

    Step 2: Deploy Registry
    deployment.apps/registry created
    service/registry created
    Waiting for deployment "registry" rollout to finish: 0 of 1 updated replicas are available...
    deployment "registry" successfully rolled out

    Step 3: Deploy Feast Online Feature Server
    secret/gcp-sa-key created
    deployment.apps/online-feature-server created
    service/online-feature-server created
    Waiting for deployment "online-feature-server" rollout to finish: 0 of 1 updated replicas are available...
    deployment "online-feature-server" successfully rolled out
    ```

## Test Your Feast Online Feature Server

首先要先將service 透過`minikube service` output給Local使用

```bash
minikube service online-feature-server -n feast
```

!!! success "Expected Output"

    ```
    |-----------|-----------------------|-------------|---------------------------|
    | NAMESPACE |         NAME          | TARGET PORT |            URL            |
    |-----------|-----------------------|-------------|---------------------------|
    | feast     | online-feature-server |        {==8080==} | {==http://192.168.49.2:30000==} |
    |-----------|-----------------------|-------------|---------------------------|
    🏃  Starting tunnel for service online-feature-server.
    |-----------|-----------------------|-------------|------------------------|
    | NAMESPACE |         NAME          | TARGET PORT |          URL           |
    |-----------|-----------------------|-------------|------------------------|
    | feast     | online-feature-server |             | {==http://127.0.0.1:52316==} |
    |-----------|-----------------------|-------------|------------------------|
    🎉  Opening service feast/online-feature-server in default browser...
    ❗  Because you are using a Docker driver on darwin, the terminal needs to be open to run it.
    ```

`http://127.0.0.1:52316`就是我們在localhost可以access得到的URL，待會測試時都會需要打這個URL


### Materialize Features to Online Store

#### `/materialize`

Materialize features within a specified time range

```bash
--8<-- "./feast-2/test-commands.txt:materialize"
```

where `request-materialize.json` is

```json
--8<-- "./feast-2/request-materialize.json"
```

!!! success "Expected Output"

    ```bash
    TODO
    ```

#### `/materialize-incremental`

Incrementally materialize features up to a specified timestamp

```bash
--8<-- "./feast-2/test-commands.txt:materialize-incremental"
```

where `request-materialize-incremental.json` is

```json
--8<-- "./feast-2/request-materialize-incremental.json"
```

!!! success "Expected Output"

    ```bash
    TODO
    ```

### Get Online Features

#### `/get-online-features`

Get online features from the feature store:

```bash
--8<-- "./feast-2/test-commands.txt:get-online-features"
```

where `request-get-online-features.json` is 

```json
--8<-- "./feast-2/request-get-online-features.json"
```

!!! success "Expected Output"

    ```json
    {
      "metadata": {
        "feature_names": [
          "user_id",
          "transaction_count_7d",
          "credit_score",
          "account_age_days",
          "user_has_2fa_installed",
          "user_has_fraudulent_transactions_7d"
        ]
      },
      "results": [
        {
          "values": [
            "v5zlw0"
          ],
          "statuses": [
            "PRESENT"
          ],
          "event_timestamps": [
            "1970-01-01T00:00:00Z"
          ]
        },
        {
          "values": [
            null
          ],
          "statuses": [
            "PRESENT"
          ],
          "event_timestamps": [
            "1970-01-01T00:00:00Z"
          ]
        },
        {
          "values": [
            480
          ],
          "statuses": [
            "PRESENT"
          ],
          "event_timestamps": [
            "2025-04-29T22:00:34Z"
          ]
        },
        {
          "values": [
            655
          ],
          "statuses": [
            "PRESENT"
          ],
          "event_timestamps": [
            "2025-04-29T22:00:34Z"
          ]
        },
        {
          "values": [
            1
          ],
          "statuses": [
            "PRESENT"
          ],
          "event_timestamps": [
            "2025-04-29T22:00:34Z"
          ]
        },
        {
          "values": [
            0.0
          ],
          "statuses": [
            "PRESENT"
          ],
          "event_timestamps": [
            "2025-05-05T22:00:50Z"
          ]
        }
      ]
    }
    ```

https://docs.feast.dev/reference/feature-servers/python-feature-server
