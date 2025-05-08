#!/bin/bash

echo "Step 0: Create feast Namespace"
kubectl create ns feast

echo "Step 1: Deploy Online Store"
kubectl apply -f online-store.yaml
kubectl rollout status deployment/online-store -n feast

echo "Step 2: Deploy Registry"
kubectl apply -f registry.yaml
kubectl rollout status deployment/registry -n feast

echo "Step 3: Deploy Feast Online Feature Server"
kubectl apply -f secret.yaml
kubectl apply -f online-feature-server.yaml
kubectl rollout status deployment/online-feature-server -n feast
