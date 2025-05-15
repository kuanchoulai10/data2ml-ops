# Deploy Feast Server

```
minikube start --cpus=4 --memory=7000 --driver=docker
```

## Create GCP Service Account Key

```bash
gcloud config get-value project

mlops-437709
```


```bash
gcloud iam service-accounts create feast-sa \
    --display-name "Feast Service Account"

Reauthentication required.
Please enter your password:
Reauthentication successful.
Created service account [feast-sa].
```


```bash
ggcloud projects add-iam-policy-binding mlops-437709 \
    --member="serviceAccount:feast-sa@mlops-437709.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"
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

```bash
gcloud iam service-accounts keys create feast-gcp-key.json \
    --iam-account=feast-sa@mlops-437709.iam.gserviceaccount.com
created key [a2609fffff05f5fdf311de233f1a2e1e89288ab5] of type [json] as [feast-gcp-key.json] for [feast-sa@mlops-437709.iam.gserviceaccount.com]
```

```bash
ll | grep key

.rw-------@ 2.3k kcl   7 May 14:52  feast-gcp-key.json
```

## Local Docker Build

```bash
ll

Permissions Size User Date Modified Name
.rw-r--r--@  458 kcl   7 May 15:09  Dockerfile
.rw-r--r--@  139 kcl   7 May 15:01  entrypoint.sh
.rw-------@ 2.3k kcl   7 May 14:52  feast-gcp-key.json
.rw-r--r--@  616 kcl   6 May 18:49  feature_store.yaml
.rw-r--r--@ 1.2k kcl   6 May 19:19  fraud_features.py
drwxr-xr-x@    - kcl   7 May 00:04  k8s
.rw-r--r--@  340 kcl   6 May 19:48  request-get-online-features.json
.rw-r--r--@   33 kcl   6 May 20:07  request-materialize-incremental.json
.rw-r--r--@   70 kcl   6 May 20:08  request-materialize.json
.rw-r--r--@ 5.0k kcl   7 May 00:16  requirements.txt
```

```
--8<-- "./feast-2/feature_store.yaml"
```

```
--8<-- "./feast-2/fraud_features.py"
```

```
--8<-- "./feast-2/requirements.txt"
```

```
--8<-- "./feast-2/entrypoint.sh"
```

```
--8<-- "./feast-2/Dockerfile"
```

```bash
docker buildx build \
  --platform linux/amd64 \
  -t feast:v0.1.0 \
  -t feast:latest \
  .
```

```bash
docker images --filter=reference="feast*"
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
{==feast==}        v0.1.0    {==436abcf371e9==}   55 seconds ago   596MB
```

## Load local docker image to minikube cluster
@minikube

```bash
minikube ssh
docker@minikube:~$ docker images
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

@local
```bash
minikube image load feast:v0.1.0
```

@minikube
```bash
docker@minikube:~$ docker images
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

## Create K8S Secret

```bash
cat ../feast-gcp-key.json | base64
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: feast-gcp-key
  namespace: feast
type: Opaque
data:
  key.json: <base64 encoded string>
```

```bash
bash install.sh

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

```bash
minikube service online-feature-server -n feast

|-----------|-----------------------|-------------|---------------------------|
| NAMESPACE |         NAME          | TARGET PORT |            URL            |
|-----------|-----------------------|-------------|---------------------------|
| feast     | online-feature-server |        8080 | http://192.168.49.2:30000 |
|-----------|-----------------------|-------------|---------------------------|
🏃  Starting tunnel for service online-feature-server.
|-----------|-----------------------|-------------|------------------------|
| NAMESPACE |         NAME          | TARGET PORT |          URL           |
|-----------|-----------------------|-------------|------------------------|
| feast     | online-feature-server |             | http://127.0.0.1:52316 |
|-----------|-----------------------|-------------|------------------------|
🎉  Opening service feast/online-feature-server in default browser...
❗  Because you are using a Docker driver on darwin, the terminal needs to be open to run it.
```

```bash
curl -X POST http://127.0.0.1:52316/get-online-features \
     -H "Content-Type: application/json" \
     -d @request-get-online-features.json | jq

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--   100  1010  100   682  100   328  10006   4812 --:--:-- --:--:-- --:--:-- 14852
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