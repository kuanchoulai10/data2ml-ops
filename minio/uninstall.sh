#!/bin/bash

set -euo pipefail

kubectl delete -f minio.yaml
kubectl delete ns minio
