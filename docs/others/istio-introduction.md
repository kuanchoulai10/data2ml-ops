# Istio

## What is Istio

- Istio is an open source service mesh that layers transparently onto existing distributed applications.
- Istio extends Kubernetes to establish a programmable, application-aware network. Working with both Kubernetes and traditional workloads, Istio brings standard, universal traffic management, telemetry, and security to complex deployments.
- It gives you:
    - Secure service-to-service communication in a cluster with mutual TLS encryption, strong identity-based authentication and authorization
    - Automatic load balancing for HTTP, gRPC, WebSocket, and TCP traffic
    - Fine-grained control of traffic behavior with rich routing rules, retries, failovers, and fault injection
    - A pluggable policy layer and configuration API supporting access controls, rate limits and quotas
    - Automatic metrics, logs, and traces for all traffic within a cluster, including cluster ingress and egress

## How it works?

- The **control plane** takes your desired configuration, and its view of the services, and dynamically programs the proxy servers, updating them as the rules or the environment changes.
- The **data plane** is the **communication between services**. Without a service mesh, the network doesn’t understand the traffic being sent over, and can’t make any decisions based on what type of traffic it is, or who it is from or to. It supports two data planes:
    - **sidecar mode**, which deploys an **Envoy proxy** along with each pod that you start in your cluster, or running alongside services running on VMs.
    - **ambient mode**, which uses a per-node Layer 4 proxy, and optionally a per-namespace Envoy proxy for Layer 7 features

### Sidecar Mode vs. Ambient Mode in Istio

| Feature                  | Sidecar Mode                      | Ambient Mode                                      |
|--------------------------|-----------------------------------|---------------------------------------------------|
| **Proxy location**       | One per pod (sidecar)             | One per node (`ztunnel`), plus optional waypoint proxies |
| **Setup complexity**     | Requires injection into each pod  | No sidecar; label namespace only                  |
| **Resource usage**       | Higher                            | Lower                                             |
| **Feature maturity**     | Very mature                       | Newer, still evolving                             |
| **Transparency to app**  | Yes                               | Yes                                               |
| **Traffic interception** | iptables per pod                  | eBPF or iptables at node level                    |

## Why Istio?

Simple and powerful

Istio 之所以被稱為 simple and powerful，是因為：

- 它功能完整，幾乎涵蓋所有 service mesh 所需的治理需求
- 一旦建構完成，它讓微服務的運維與治理變得真正簡單
- 透過標準化代理層和策略定義，抽象了底層複雜性
- 新推出的 Ambient 模式更降低了部署與學習門檻

其實我一開始也覺得 Istio 有點複雜，畢竟裡面名詞一堆、又有什麼 sidecar、control plane、mTLS 之類的。但後來真的理解它之後，我覺得它會被說成「simple and powerful」不是沒道理的。

Powerful 的地方超明顯，它幾乎幫你包辦了所有微服務之間的網路治理：像是 TLS 加密、零信任架構、流量分流、錯誤重試、異常注入、A/B 測試這些，過去要自己一個一個開發、測試、布署，但用 Istio 的話，只要定義一個 YAML 檔就搞定了。

而它被說 simple，其實是從整個系統層級來看。你用它把 service mesh 架起來之後，真的會覺得「管理服務的複雜度」被大幅降低。特別是現在有了 Ambient mode，不需要再注入 sidecar，也不用一直改 pod spec，讓部署更乾淨、擴展更容易。

所以老實說，Istio 本身可能不是真的「入門超簡單」，但它可以讓你後續維運變得更簡單、更安心。

The Envoy proxy

Istio inherits all the power and flexibility of Envoy, including world-class extensibility using WebAssembly

a high performance service proxy initially built by Lyft

Envoy would go on to become the load balancer that powers Google Cloud as well as the proxy for almost every other service mesh platform.

首先，在流量控制方面，Kubernetes 本身的 Ingress 只能處理從外部進入集群的請求，對於服務之間的內部通訊毫無控制能力。它無法根據版本、Header、使用者身分等條件來調整路由邏輯。Istio 則透過 VirtualService 和 DestinationRule 這兩種資源，讓你能精細地指定流量該如何分流，比如針對特定用戶導向新版本、實作 A/B 測試、灰階釋出等，在不改變應用程式的情況下做到彈性路由。

接著是安全性問題。Kubernetes 雖然支援 Role-Based Access Control（RBAC）與 NetworkPolicy，卻無法確保服務之間的通訊是加密的，也無法驗證通訊雙方的身分。Istio 則藉由自動化的 mutual TLS（mTLS）機制，在每個服務之間建立加密通道，並搭配身份驗證與授權策略，確保只有被授權的服務能互相通訊，實現零信任架構的基本原則。

再來是可觀察性。Kubernetes 雖然可以查看 Pod logs 和一些基本的 metrics，但對於微服務之間的追蹤、延遲分析、流量瓶頸等問題，原生功能明顯不足。Istio 在每個服務邊緣部署 proxy，這讓它可以自動收集詳細的 telemetry 資訊，包括 request-level tracing、流量指標與錯誤率，並整合到像 Prometheus、Grafana、Jaeger 等工具中，幾乎不需要修改應用程式就能做到全面監控。

最後，在靈活性與擴展性上，Kubernetes 無法針對個別服務注入自訂的網路處理邏輯。Istio 透過 sidecar 模式（或較新的 ambient 模式）讓每個服務都擁有自己的網路代理，並支援 WebAssembly 插件，你可以動態插入認證邏輯、資料轉換甚至異常模擬，將網路行為調整為符合業務需求的模樣。

## What happened after installing Istio

在完成 Istio 的安裝後，系統會在 Kubernetes 中建立一個名為 istio-system 的命名空間，這是 Istio 控制平面（Control Plane）元件所運作的主要位置。裡面會自動部署多個核心元件，這些元件透過服務與 Pod 的形式呈現，並且藉由 CRD 讓 Istio 能擴展出自己的資源模型。

首先，最重要的控制元件是 istiod，它是一個整合型的控制平面元件，從 Istio 1.5 起開始整併了過去的 Pilot、Mixer、Citadel 等元件。這個 Pod 負責管理 service discovery、sidecar 的設定發送（XDS）、mTLS 憑證簽發、安全性策略下發等工作。你會在 istio-system 中看到一個叫做 istiod-xxxx 的 Pod，對應的 Service 則通常是 istiod 或 istio-pilot，取決於版本與安裝方式。

此外，若你啟用了 Ingress Gateway（大多數人會），你還會看到一個叫做 istio-ingressgateway 的 Deployment、Service 和 Pod。這是一個以 Envoy 為核心的負責接收外部 HTTP/TCP 流量的代理伺服器，通常會是 NodePort 或 LoadBalancer 型別的 Service

- istiod：這是 Istio 的控制平面核心。它負責管理服務發現（service discovery）、發送代理設定（xDS）、mTLS 憑證簽發與安全策略下發。從 Istio 1.5 開始，這個元件整合了過去的 Pilot、Citadel、Galley 等角色。
- istio-ingressgateway：這是一個使用 Envoy 實作的 Ingress Gateway，是外部流量進入服務網格的入口，通常用來接收 HTTP、HTTPS、gRPC 等外部請求，並轉發至集群內部的服務。

除了上述控制元件之外，Istio 安裝也會附帶一些擴充資源。最明顯的是一系列的 CRD，像是 VirtualService、DestinationRule、Gateway、PeerAuthentication、AuthorizationPolicy 等。這些都是你在使用 Istio 做路由控制、流量分流、安全策略時會用到的資源。這些 CRD 可以透過 kubectl get crd 查看，名稱通常會是 virtualservices.networking.istio.io 這樣的格式。

這些資源構成了 Istio 的核心基礎，讓你得以在 Kubernetes 上建立一個可控、安全且具有流量觀察能力的服務網格。

## References

- [What is Istio? | Istio](https://istio.io/latest/docs/overview/what-is-istio/)
- [Sidecar or ambient? | Istio](https://istio.io/latest/docs/overview/dataplane-modes/)