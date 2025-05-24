#!/bin/bash

set -e

echo "Uninstalling KServe, Knative, Istio, and Cert-Manager..."

# Uninstall KServe
helm uninstall kserve -n kserve || echo "kserve not found"
helm uninstall kserve-crd -n kserve || echo "kserve-crd not found"
kubectl delete ns kserve --ignore-not-found

# Uninstall cert-manager
kubectl delete -f https://github.com/cert-manager/cert-manager/releases/download/v1.17.2/cert-manager.yaml || echo "cert-manager not installed"
kubectl delete ns cert-manager --ignore-not-found

# Uninstall Knative net-istio and serving
kubectl delete -f https://github.com/knative/net-istio/releases/download/knative-v1.15.0/net-istio.yaml || echo "net-istio not installed"
kubectl delete -f https://github.com/knative/serving/releases/download/knative-v1.15.0/serving-core.yaml || echo "knative-core not installed"
kubectl delete -f https://github.com/knative/serving/releases/download/knative-v1.15.0/serving-crds.yaml || echo "knative-crds not installed"

# Uninstall Istio
$HOME/istio-1.22.8/bin/istioctl uninstall --purge -y || echo "istioctl uninstall failed"
kubectl delete ns istio-system --ignore-not-found

# Optional: Remove istioctl binary and path from .zshrc
echo "Cleaning up istioctl binary and .zshrc entry..."
sed -i '' '/istio-1.22.8\/bin/d' ~/.zshrc 2>/dev/null || true
rm -rf $HOME/istio-1.22.8

echo "Uninstallation completed."
