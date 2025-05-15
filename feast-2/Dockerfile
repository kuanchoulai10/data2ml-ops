# Use Python 3.10 slim as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x entrypoint.sh

COPY feature_store.yaml /app/feature_store.yaml
COPY account_features.py /app/account_features.py

# Set the entrypoint to run Feast
ENTRYPOINT ["./entrypoint.sh"]
