#!/bin/bash
set -e

echo "Running feast apply..."
feast apply

echo "Starting feast server..."
exec feast serve --host 0.0.0.0 --port 8080
