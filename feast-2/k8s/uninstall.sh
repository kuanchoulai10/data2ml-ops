#!/bin/bash

echo "Step 1: Delete Feast Online Feature Server"
kubectl delete -f online-feature-server.yaml
kubectl delete -f secret.yaml

echo "Step 2: Delete Registry"
kubectl delete -f registry.yaml

echo "Step 3: Delete Online Store"
kubectl delete -f online-store.yaml

echo "Step 4: Delete feast Namespace"
kubectl delete ns feast
