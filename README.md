# MLOps



1. Create a service account and grant the necessary permissions

```shell
gcloud projects add-iam-policy-binding udemy-mlops \
    --member=serviceAccount:vertexai-sa@udemy-mlops.iam.gserviceaccount.com \
    --role=roles/aiplatform.customCodeServiceAgent

gcloud projects add-iam-policy-binding udemy-mlops \
    --member=serviceAccount:vertexai-sa@udemy-mlops.iam.gserviceaccount.com \
    --role=roles/aiplatform.admin

gcloud projects add-iam-policy-binding udemy-mlops \
    --member=serviceAccount:vertexai-sa@udemy-mlops.iam.gserviceaccount.com \
    --role=roles/storage.objectAdmin
```

2. 

```shell
# Step-1 - Build the image 
docker build -t vertex-bikeshare-model .

# Step-2 - Tag the image locally
docker tag vertex-bikeshare-model gcr.io/udemy-mlops/vertex-bikeshare-model

# Step-3 - Push the image to Google Cloud Registry 
docker push gcr.io/udemy-mlops/vertex-bikeshare-model

# Step-4 - Submit a custom model training job  
gcloud ai custom-jobs create --region=us-central1 \
--project=udemy-mlops \
--worker-pool-spec=replica-count=1,machine-type='n1-standard-4',container-image-uri='gcr.io/udemy-mlops/vertex-bikeshare-model' \
--display-name=bike-sharing-model-training
```

## 
Cloud Build

1. Build Docker Image
2. Push Docker Image To GCR
3. Execute Tests
4. Submit Training Job
5. Upload Model
6. Fetch Model ID
7. Create Endpoint
8. Deploy Model Endpoint

## model_training_code.py

1. load data
2. preprocess data (rename columns, drop columns, one-hot-encodings)
3. train test split
4. train model
5. dump model("gs://sid-vertex-mlops/bike-share-rf-regression-artifact/model.joblib")