# Use Python 3.10 slim as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

COPY feature_store.yaml /app/feature_store.yaml
COPY requirements.txt /app/requirements.txt
COPY fraud_features.py /app/fraud_features.py
COPY entrypoint.sh /app/entrypoint.sh

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x entrypoint.sh

# Set the entrypoint to run Feast
ENTRYPOINT ["./entrypoint.sh"]
