---
tags:
  - Istio
---
# What Is Istio?

<iframe width="560" height="315" src="https://www.youtube.com/embed/16fgzklcF7Y?si=FS2wVxcUEgDc73Xb" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<figure span="markdown">
  ![](https://istio.io/latest/docs/ops/deployment/architecture/arch.svg)
  [*Architecture*](https://istio.io/latest/docs/ops/deployment/architecture/)
</figure>


- Istio is an open source service mesh that layers transparently onto existing distributed applications.
- Istio extends Kubernetes to establish a programmable, application-aware network. Working with both Kubernetes and traditional workloads, Istio brings standard, universal traffic management, telemetry, and security to complex deployments.
- It gives you:
    - Secure service-to-service communication in a cluster with mutual TLS encryption, strong identity-based authentication and authorization
    - Automatic load balancing for HTTP, gRPC, WebSocket, and TCP traffic
    - Fine-grained control of traffic behavior with rich routing rules, retries, failovers, and fault injection
    - A pluggable policy layer and configuration API supporting access controls, rate limits and quotas
    - Automatic metrics, logs, and traces for all traffic within a cluster, including cluster ingress and egress

## How It Works?

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

## What happens after installing Istio

After completing the Istio installation, the system creates a namespace called `istio-system` in Kubernetes, which serves as the **primary location where Istio's control plane components operate**. Multiple core components are automatically deployed within this namespace, presented as services and pods, with Istio extending its own resource model through Custom Resource Definitions (CRDs).

First, the most important control component is `istiod`, an integrated control plane component that has consolidated the previously separate Pilot, Mixer, and Citadel components since Istio 1.5. This pod manages service discovery, sidecar configuration distribution (XDS), mTLS certificate issuance, and security policy distribution. You'll see a pod named `istiod-xxxx` in the `istio-system` namespace, with the corresponding service typically being `istiod` or `istio-pilot`, depending on the version and installation method.

Additionally, if you enable the Ingress Gateway (which most people do), you'll also see a deployment, service, and pod called `istio-ingressgateway`. This is an Envoy-based proxy server responsible for **receiving external HTTP/TCP traffic**, typically configured as a `NodePort` or `LoadBalancer` service type.

Beyond the control components mentioned above, Istio installation also includes various extension resources. Most notably, it provides a series of CRDs such as **`VirtualService`**, **`DestinationRule`**, **`Gateway`**, **`PeerAuthentication`**, and **`AuthorizationPolicy`**. These are the resources you'll use when working with Istio for routing control, traffic splitting, and security policies.

These resources form Istio's core foundation, enabling you to establish a controllable, secure, and traffic-observable service mesh on Kubernetes.

## Why Istio?

Simple and powerful

Istio is characterized as "simple and powerful" for several key reasons:

- It provides comprehensive functionality, covering nearly all service mesh governance requirements
- Once established, it makes microservice operations and governance genuinely straightforward
- It abstracts underlying complexity through standardized proxy layers and policy definitions
- The newly introduced Ambient mode further reduces deployment and learning barriers

Initially, I found Istio somewhat complex, given the numerous terminologies like sidecar, control plane, and mTLS. However, after truly understanding it, I believe there's solid reasoning behind calling it "simple and powerful."

The "powerful" aspect is that it handles virtually all network governance between microservices. Features like TLS encryption, zero-trust architecture, traffic splitting, error retries, fault injection, and A/B testing that previously required individual development, testing, and deployment can now be accomplished simply by defining a YAML configuration.

The "simple" designation comes from a system-level perspective. Once you establish the service mesh with Istio, you'll genuinely feel that "service management complexity" has been significantly reduced. Particularly with the introduction of Ambient mode, there's no need for sidecar injection or constant pod spec modifications, making deployment cleaner and scaling easier.

To be honest, Istio itself may not be truly "beginner-friendly," but it makes subsequent operations simpler and more reliable.

## Why Not Just Use Kubernetes?

First, regarding **traffic control**, **Kubernetes'** native Ingress can only handle requests entering the cluster from external sources and has no control over internal communication between services. It cannot adjust routing logic based on versions, headers, user identity, or other conditions. **Istio**, through `VirtualService` and `DestinationRule` resources, enables fine-grained specification of traffic distribution. For example, directing specific users to new versions, implementing A/B testing, or canary releases, all while achieving flexible routing without modifying applications.

- `VirtualService`: How you route your traffic **TO** a given destination
- `DestinationRule`: Configure what happens to traffic **FOR** that destination

Next is the **security** aspect. While **Kubernetes** supports Role-Based Access Control (RBAC) and NetworkPolicy, it cannot ensure that communication between services is encrypted or verify the identities of communicating parties. **Istio** establishes encrypted channels between services through automated mutual TLS (mTLS) mechanisms, combined with authentication and authorization policies, ensuring that only authorized services can communicate with each other, thereby implementing the fundamental principles of zero-trust architecture.

Regarding **observability**, while **Kubernetes** allows viewing Pod logs and some basic metrics, its native functionality is clearly insufficient for microservice tracing, latency analysis, and traffic bottleneck identification. **Istio** deploys proxies at each service edge, enabling automatic collection of detailed telemetry information, including request-level tracing, traffic metrics, and error rates, integrated with tools like Prometheus, Grafana, and Jaeger—achieving comprehensive monitoring with minimal application modifications.

Finally, in terms of **flexibility** and **extensibility**, **Kubernetes** cannot inject custom network processing logic for individual services. **Istio**, through sidecar mode (or the newer ambient mode), provides each service with its own network proxy and supports WebAssembly plugins, allowing dynamic insertion of authentication logic, data transformation, or even fault simulation, adapting network behavior to meet business requirements.


## References

- [What is Istio? | Istio](https://istio.io/latest/docs/overview/what-is-istio/)
- [Sidecar or ambient? | Istio](https://istio.io/latest/docs/overview/dataplane-modes/)