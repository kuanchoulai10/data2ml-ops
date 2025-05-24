# Prerequisites

Before getting started, ensure your environment is properly set up with the following installations:

- Homebrew
- Minikube
- Docker Desktop
- kubectl

```
{==brew --version==}

Homebrew 4.5.1
```

```
{==minikube version==}

minikube version: {==v1.33.1==}
commit: 248d1ec5b3f9be5569977749a725f47b018078ff
```

```
{==docker version==}

Client:
 Version:           {==28.1.1==}
 API version:       {==1.49==}
 Go version:        go1.23.8
 Git commit:        4eba377
 Built:             Fri Apr 18 09:49:45 2025
 OS/Arch:           darwin/arm64
 Context:           desktop-linux

Server: Docker Desktop {==4.41.1==} (191279)
 {==Engine==}:
  Version:          {==28.1.1==}
  API version:      {==1.49==} (minimum version 1.24)
  Go version:       {==go1.23.8==}
  Git commit:       01f442b
  Built:            Fri Apr 18 09:52:08 2025
  OS/Arch:          linux/arm64
  Experimental:     false
 {==containerd==}:
  Version:          {==1.7.27==}
  GitCommit:        05044ec0a9a75232cad458027ca83437aae3f4da
 {==runc==}:
  Version:          {==1.2.5==}
  GitCommit:        v1.2.5-0-g59923ef
 {==docker-init==}:
  Version:          {==0.19.0==}
  GitCommit:        de40ad0
```

```
{==kubectl version==}

Client Version: {==v1.30.2==}
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
Server Version: {==v1.30.0==}
```

This series of articles provides detailed explanations and step-by-step guides. If you prefer to focus on the practical implementation, follow the sequence below to build the architecture step by step.

- [Modeling Data](./dbt/modeling-data.md)
- [Modeling Features](./feast/modeling-features.md)
- [Deploy Feast on Kubernetes](./feast/deployment.md)
- [Deploy MinIO on Kubernetes](./minio/deployment.md)
- [Deploy MLflow on Kubernetes](./mlflow/deployment.md)
- [Deploy Ray Cluster on Kubernetes Using KubeRay](./ray/deployment.md)
- [Integrate Ray Tune with Optuna, Imblearn, MLflow and MinIO](./ray/ray-tune.md)
- [Submit a Ray Tune Job to Your Ray Cluster](./ray/ray-job.md)
- [Install KServe in Serverless Mode](./kserve/installation.md)
- [Feast Transformer](./kserve/feast-transformer.md)
- [Deploy Your Model on Kubernetes Using Kserve InferenceService](./kserve/deployment.md)