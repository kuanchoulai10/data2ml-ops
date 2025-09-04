#!/bin/bash

set -euo pipefail

kubectl create ns minio
kubectl apply -f minio.yaml
