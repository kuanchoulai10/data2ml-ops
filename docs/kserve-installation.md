# Deploy Kserve on Serverless Mode

- Install Knative Serving v1.15.0
- Install Istio v1.22.8

## [Install Knative Serving](https://knative.dev/docs/install/yaml-install/serving/install-serving-with-yaml/)



Install the required custom resources by running the command

```bash
kubectl apply -f https://github.com/knative/serving/releases/download/{==knative-v1.15.0/serving-crds.yaml==}
```

??? note "Result"

    ```
    customresourcedefinition.apiextensions.k8s.io/certificates.networking.internal.knative.dev created
    customresourcedefinition.apiextensions.k8s.io/configurations.serving.knative.dev created
    customresourcedefinition.apiextensions.k8s.io/clusterdomainclaims.networking.internal.knative.dev created
    customresourcedefinition.apiextensions.k8s.io/domainmappings.serving.knative.dev created
    customresourcedefinition.apiextensions.k8s.io/ingresses.networking.internal.knative.dev created
    customresourcedefinition.apiextensions.k8s.io/metrics.autoscaling.internal.knative.dev created
    customresourcedefinition.apiextensions.k8s.io/podautoscalers.autoscaling.internal.knative.dev created
    customresourcedefinition.apiextensions.k8s.io/revisions.serving.knative.dev created
    customresourcedefinition.apiextensions.k8s.io/routes.serving.knative.dev created
    customresourcedefinition.apiextensions.k8s.io/serverlessservices.networking.internal.knative.dev created
    customresourcedefinition.apiextensions.k8s.io/services.serving.knative.dev created
    customresourcedefinition.apiextensions.k8s.io/images.caching.internal.knative.dev created
    ```

Install the core components of Knative Serving to you kubernetes cluster (namespace `knative-serving`) by running the command:

```bash
kubectl apply -f https://github.com/knative/serving/releases/download/{==knative-v1.15.0/serving-core.yaml==}
```

??? note "Result"

    ```
    {==namespace/knative-serving created==}
    role.rbac.authorization.k8s.io/knative-serving-activator created
    clusterrole.rbac.authorization.k8s.io/knative-serving-activator-cluster created
    clusterrole.rbac.authorization.k8s.io/knative-serving-aggregated-addressable-resolver created
    clusterrole.rbac.authorization.k8s.io/knative-serving-addressable-resolver created
    clusterrole.rbac.authorization.k8s.io/knative-serving-namespaced-admin created
    clusterrole.rbac.authorization.k8s.io/knative-serving-namespaced-edit created
    clusterrole.rbac.authorization.k8s.io/knative-serving-namespaced-view created
    clusterrole.rbac.authorization.k8s.io/knative-serving-core created
    clusterrole.rbac.authorization.k8s.io/knative-serving-podspecable-binding created
    serviceaccount/controller created
    clusterrole.rbac.authorization.k8s.io/knative-serving-admin created
    clusterrolebinding.rbac.authorization.k8s.io/knative-serving-controller-admin created
    clusterrolebinding.rbac.authorization.k8s.io/knative-serving-controller-addressable-resolver created
    serviceaccount/activator created
    rolebinding.rbac.authorization.k8s.io/knative-serving-activator created
    clusterrolebinding.rbac.authorization.k8s.io/knative-serving-activator-cluster created
    customresourcedefinition.apiextensions.k8s.io/images.caching.internal.knative.dev unchanged
    certificate.networking.internal.knative.dev/routing-serving-certs created
    customresourcedefinition.apiextensions.k8s.io/certificates.networking.internal.knative.dev unchanged
    customresourcedefinition.apiextensions.k8s.io/configurations.serving.knative.dev unchanged
    customresourcedefinition.apiextensions.k8s.io/clusterdomainclaims.networking.internal.knative.dev unchanged
    customresourcedefinition.apiextensions.k8s.io/domainmappings.serving.knative.dev unchanged
    customresourcedefinition.apiextensions.k8s.io/ingresses.networking.internal.knative.dev unchanged
    customresourcedefinition.apiextensions.k8s.io/metrics.autoscaling.internal.knative.dev unchanged
    customresourcedefinition.apiextensions.k8s.io/podautoscalers.autoscaling.internal.knative.dev unchanged
    customresourcedefinition.apiextensions.k8s.io/revisions.serving.knative.dev unchanged
    customresourcedefinition.apiextensions.k8s.io/routes.serving.knative.dev unchanged
    customresourcedefinition.apiextensions.k8s.io/serverlessservices.networking.internal.knative.dev unchanged
    customresourcedefinition.apiextensions.k8s.io/services.serving.knative.dev unchanged
    image.caching.internal.knative.dev/queue-proxy created
    configmap/config-autoscaler created
    configmap/config-certmanager created
    configmap/config-defaults created
    configmap/config-deployment created
    configmap/config-domain created
    configmap/config-features created
    configmap/config-gc created
    configmap/config-leader-election created
    configmap/config-logging created
    configmap/config-network created
    configmap/config-observability created
    configmap/config-tracing created
    horizontalpodautoscaler.autoscaling/activator created
    poddisruptionbudget.policy/activator-pdb created
    deployment.apps/activator created
    service/activator-service created
    deployment.apps/autoscaler created
    service/autoscaler created
    deployment.apps/controller created
    service/controller created
    horizontalpodautoscaler.autoscaling/webhook created
    poddisruptionbudget.policy/webhook-pdb created
    deployment.apps/webhook created
    service/webhook created
    validatingwebhookconfiguration.admissionregistration.k8s.io/config.webhook.serving.knative.dev created
    mutatingwebhookconfiguration.admissionregistration.k8s.io/webhook.serving.knative.dev created
    validatingwebhookconfiguration.admissionregistration.k8s.io/validation.webhook.serving.knative.dev created
    secret/webhook-certs created
    ```

## [Install Networking Layer - Istio](https://knative.dev/docs/install/installing-istio/)

Install Istio 1.22.8

```
curl -L https://istio.io/downloadIstio | ISTIO_VERSION={==1.22.8==} sh -
```

??? note "Result"

    ```
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100   102  100   102    0     0    350      0 --:--:-- --:--:-- --:--:--   351
    100  5124  100  5124    0     0   6834      0 --:--:-- --:--:-- --:--:-- 13343

    Downloading istio-1.22.8 from https://github.com/istio/istio/releases/download/1.22.8/istio-1.22.8-osx-arm64.tar.gz ...

    Istio 1.22.8 download complete!

    The Istio release archive has been downloaded to the istio-1.22.8 directory.

    To configure the istioctl client tool for your workstation,
    add the /Users/kcl/istio-1.22.8/bin directory to your environment path variable with:
        {==export PATH="$PATH:/Users/kcl/istio-1.22.8/bin"==}

    Begin the Istio pre-installation check by running:
        istioctl x precheck 

    Try Istio in ambient mode
        https://istio.io/latest/docs/ambient/getting-started/
    Try Istio in sidecar mode
        https://istio.io/latest/docs/setup/getting-started/
    Install guides for ambient mode
        https://istio.io/latest/docs/ambient/install/
    Install guides for sidecar mode
        https://istio.io/latest/docs/setup/install/

    Need more information? Visit https://istio.io/latest/docs/
    ```

Add `istioctl` to the path

```sh
export PATH="$PATH:/User/kcl/istio-1.22.8/bin"
```


You can easily install and customize your Istio installation with `istioctl`. It will deploy the resources to your kubernetes cluster in the namespace `istio-system`

```
istioctl install -y
```

??? note "Result"

    ```
    WARNING: Istio 1.22.0 may be out of support (EOL) already: see https://istio.io/latest/docs/releases/supported-releases/ for supported releases
    ✔ Istio core installed                       
    ✔ Istiod installed                           
    ✔ Ingress gateways installed
    ✔ Installation complete
    Made this installation the default for injection and validation.
    ```

Check the versions

```bash
istioctl version
```

??? note "Result"

    ```
    client version: 1.22.8
    control plane version: 1.22.8
    data plane version: 1.22.8 (1 proxies)
    ```

Check all the deployed resources

```bash
kubectl get all -n istio-system
```

??? note "Result"

    ```
    NAME                                        READY   STATUS    RESTARTS   AGE
    pod/istio-ingressgateway-5d4bc8b8c6-ql8tb   1/1     Running   0          34m
    pod/istiod-6db4dfd884-k77x4                 1/1     Running   0          34m

    NAME                            TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)                                      AGE
    {==service/istio-ingressgateway==}    LoadBalancer   10.97.200.129    {==<pending>==}     15021:31297/TCP,80:32665/TCP,443:30210/TCP   34m
    service/istiod                  ClusterIP      10.110.251.34    <none>        15010/TCP,15012/TCP,443/TCP,15014/TCP        34m
    service/knative-local-gateway   ClusterIP      10.111.160.103   <none>        80/TCP,443/TCP                               33m

    NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/istio-ingressgateway   1/1     1            1           34m
    deployment.apps/istiod                 1/1     1            1           34m

    NAME                                              DESIRED   CURRENT   READY   AGE
    replicaset.apps/istio-ingressgateway-5d4bc8b8c6   1         1         1       34m
    replicaset.apps/istiod-6db4dfd884                 1         1         1       34m

    NAME                                                       REFERENCE                         TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
    horizontalpodautoscaler.autoscaling/istio-ingressgateway   Deployment/istio-ingressgateway   <unknown>/80%   1         5         1          34m
    horizontalpodautoscaler.autoscaling/istiod                 Deployment/istiod                 <unknown>/80%   1         5         1          34m
    ```

To integrate Istio with Knative Serving install the Knative Istio controller by running the command

```
kubectl apply -f https://github.com/knative/net-istio/releases/download/{==knative-v1.15.0/net-istio.yaml==}
```

??? note "Result"

    ```
    clusterrole.rbac.authorization.k8s.io/knative-serving-istio created
    gateway.networking.istio.io/knative-ingress-gateway created
    gateway.networking.istio.io/knative-local-gateway created
    service/knative-local-gateway created
    configmap/config-istio created
    peerauthentication.security.istio.io/webhook created
    peerauthentication.security.istio.io/net-istio-webhook created
    deployment.apps/net-istio-controller created
    deployment.apps/net-istio-webhook created
    secret/net-istio-webhook-certs created
    service/net-istio-webhook created
    mutatingwebhookconfiguration.admissionregistration.k8s.io/webhook.istio.networking.internal.knative.dev created
    validatingwebhookconfiguration.admissionregistration.k8s.io/config.webhook.istio.networking.internal.knative.dev created
    ```

Verify the installation

```
kubectl get pods -n knative-serving
```

??? note "Result"

    ```
    NAME                                    READY   STATUS    RESTARTS   AGE
    activator-d87b89f55-kq9b7               1/1     Running   0          118m
    autoscaler-788d5c7f85-gl9kr             1/1     Running   0          118m
    controller-c55cbcc66-cr74s              1/1     Running   0          118m
    net-istio-controller-85f48fbb75-kr8tp   1/1     Running   0          37m
    net-istio-webhook-d4f6d7b45-l4kct       1/1     Running   0          37m
    webhook-65fc6c7bd8-h47wc                1/1     Running   0          118m
    ```

## Configure DNS

You can configure DNS to prevent the need to run curl commands with a host header.

Knative provides a Kubernetes Job called default-domain that configures Knative Serving to use sslip.io as the default DNS suffix. This will only work if the cluster LoadBalancer Service exposes an IPv4 address or hostname, so it will not work with IPv6 clusters or local setups like minikube unless `minikube tunnel` is running.


```bash
minikube tunnel
```

??? note "Result"

    ```
    ✅  Tunnel successfully started

    📌  NOTE: Please do not close this terminal as this process must stay alive for the tunnel to be accessible ...

    ❗  The service/ingress istio-ingressgateway requires privileged ports to be exposed: [80 443]
    🔑  sudo permission will be asked for it.
    🏃  Starting tunnel for service istio-ingressgateway.
    ```

```bash
kubectl get svc istio-ingressgateway -n istio-system
```

??? note "Result"

    ```
    NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                                      AGE
    {==istio-ingressgateway==}   LoadBalancer   10.97.200.129   {==127.0.0.1==}     15021:31297/TCP,80:32665/TCP,443:30210/TCP   71m
    ```


```
kubectl apply -f https://github.com/knative/serving/releases/download/{==knative-v1.15.0/serving-default-domain.yaml==}
```

??? note "Result"

    ```
    job.batch/default-domain created
    service/default-domain-service created
    ```

## [Install Cert Manager](https://cert-manager.io/docs/installation/)

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/{==v1.17.2/cert-manager.yaml==}
```

??? note "Result"

    ```
    {==namespace/cert-manager created==}
    customresourcedefinition.apiextensions.k8s.io/certificaterequests.cert-manager.io created
    customresourcedefinition.apiextensions.k8s.io/certificates.cert-manager.io created
    customresourcedefinition.apiextensions.k8s.io/challenges.acme.cert-manager.io created
    customresourcedefinition.apiextensions.k8s.io/clusterissuers.cert-manager.io created
    customresourcedefinition.apiextensions.k8s.io/issuers.cert-manager.io created
    customresourcedefinition.apiextensions.k8s.io/orders.acme.cert-manager.io created
    serviceaccount/cert-manager-cainjector created
    serviceaccount/cert-manager created
    serviceaccount/cert-manager-webhook created
    clusterrole.rbac.authorization.k8s.io/cert-manager-cainjector created
    clusterrole.rbac.authorization.k8s.io/cert-manager-controller-issuers created
    clusterrole.rbac.authorization.k8s.io/cert-manager-controller-clusterissuers created
    clusterrole.rbac.authorization.k8s.io/cert-manager-controller-certificates created
    clusterrole.rbac.authorization.k8s.io/cert-manager-controller-orders created
    clusterrole.rbac.authorization.k8s.io/cert-manager-controller-challenges created
    clusterrole.rbac.authorization.k8s.io/cert-manager-controller-ingress-shim created
    clusterrole.rbac.authorization.k8s.io/cert-manager-cluster-view created
    clusterrole.rbac.authorization.k8s.io/cert-manager-view created
    clusterrole.rbac.authorization.k8s.io/cert-manager-edit created
    clusterrole.rbac.authorization.k8s.io/cert-manager-controller-approve:cert-manager-io created
    clusterrole.rbac.authorization.k8s.io/cert-manager-controller-certificatesigningrequests created
    clusterrole.rbac.authorization.k8s.io/cert-manager-webhook:subjectaccessreviews created
    clusterrolebinding.rbac.authorization.k8s.io/cert-manager-cainjector created
    clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-issuers created
    clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-clusterissuers created
    clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-certificates created
    clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-orders created
    clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-challenges created
    clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-ingress-shim created
    clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-approve:cert-manager-io created
    clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-certificatesigningrequests created
    clusterrolebinding.rbac.authorization.k8s.io/cert-manager-webhook:subjectaccessreviews created
    role.rbac.authorization.k8s.io/cert-manager-cainjector:leaderelection created
    role.rbac.authorization.k8s.io/cert-manager:leaderelection created
    role.rbac.authorization.k8s.io/cert-manager-tokenrequest created
    role.rbac.authorization.k8s.io/cert-manager-webhook:dynamic-serving created
    rolebinding.rbac.authorization.k8s.io/cert-manager-cainjector:leaderelection created
    rolebinding.rbac.authorization.k8s.io/cert-manager:leaderelection created
    rolebinding.rbac.authorization.k8s.io/cert-manager-cert-manager-tokenrequest created
    rolebinding.rbac.authorization.k8s.io/cert-manager-webhook:dynamic-serving created
    service/cert-manager-cainjector created
    service/cert-manager created
    service/cert-manager-webhook created
    deployment.apps/cert-manager-cainjector created
    deployment.apps/cert-manager created
    deployment.apps/cert-manager-webhook created
    mutatingwebhookconfiguration.admissionregistration.k8s.io/cert-manager-webhook created
    validatingwebhookconfiguration.admissionregistration.k8s.io/cert-manager-webhook created
    ```

## [Install KServe](https://kserve.github.io/website/master/admin/serverless/serverless/#4-install-kserve)

Install KServe CRDs

```bash
helm install kserve-crd oci://ghcr.io/kserve/charts/{==kserve-crd==} --version {==v0.14.1==}
```

??? note "Result"

    ```
    Pulled: ghcr.io/kserve/charts/kserve-crd:v0.14.1
    Digest: sha256:b5f4f22fae8fa747ef839e1b228e74e97a78416235eb5f35da49110d25b3d1e7
    NAME: kserve-crd
    LAST DEPLOYED: Thu May  1 16:44:05 2025
    NAMESPACE: default
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
    ```

Install KServe Resources

```bash
helm install kserve oci://ghcr.io/kserve/charts/{==kserve==} --version {==v0.14.1==}
```

??? note "Result?

    ```
    Pulled: ghcr.io/kserve/charts/kserve:v0.14.1
    Digest: sha256:e65039d9e91b16d429f5fb56528e15a4695ff106a41eeae07f1f697abe974bd5
    NAME: kserve
    LAST DEPLOYED: Thu May  1 16:44:24 2025
    NAMESPACE: default
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
    ```

---

## References
- [Serverless Deployment](https://kserve.github.io/website/latest/admin/serverless/serverless/)



