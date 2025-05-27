#!/bin/bash

set -e

echo "🚀 Installing Knative + Istio + KServe..."

# Install Knative Serving CRDs and Core
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.15.0/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.15.0/serving-core.yaml

# Download and install Istio
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.22.8 DESTDIR=$HOME sh -
export PATH="$PATH:$HOME/istio-1.22.8/bin"

# Add Istio to .zshrc if not already present
grep -qxF 'export PATH="$PATH:$HOME/istio-1.22.8/bin"' ~/.zshrc || echo 'export PATH="$PATH:$HOME/istio-1.22.8/bin"' >> ~/.zshrc

# Install Istio components
$HOME/istio-1.22.8/bin/istioctl install -y

# Install Knative net-istio integration
kubectl apply -f https://github.com/knative/net-istio/releases/download/knative-v1.15.0/net-istio.yaml

# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.17.2/cert-manager.yaml

# Create namespace for KServe (if not already exists)
kubectl create ns kserve --dry-run=client -o yaml | kubectl apply -f -

# Install KServe CRDs and components
helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd \
  --version v0.15.1 \
  -n kserve

helm install kserve oci://ghcr.io/kserve/charts/kserve \
  --version v0.15.1 \
  -n kserve

echo "✅ Installation complete. You may want to run:"
echo "   source ~/.zshrc"
