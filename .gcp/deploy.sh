#!/usr/bin/env bash
set -e

# ==============================================================================
# StreamGuard AI — Google Cloud Run Automated Deployment Script (Grafana Track)
# ==============================================================================

PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
SERVICE_NAME="streamguard-ai"
REPO_NAME="streamguard-repo"
IMAGE_NAME="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:latest"

echo "======================================================================"
echo " Deploying StreamGuard AI to Google Cloud Run (Grafana Track)"
echo " Project ID : ${PROJECT_ID}"
echo " Region     : ${REGION}"
echo " Service    : ${SERVICE_NAME}"
echo "======================================================================"

echo "[1/4] Enabling required Google Cloud APIs..."
gcloud services enable \
    aiplatform.googleapis.com \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    secretmanager.googleapis.com

echo "[2/4] Ensuring Artifact Registry repository exists..."
gcloud artifacts repositories describe ${REPO_NAME} --location=${REGION} >/dev/null 2>&1 || \
gcloud artifacts repositories create ${REPO_NAME} \
    --repository-format=docker \
    --location=${REGION} \
    --description="Docker repository for StreamGuard AI"

echo "[3/4] Building image with Google Cloud Build..."
gcloud builds submit --tag ${IMAGE_NAME} .

echo "[4/4] Deploying to Google Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --set-env-vars="PROJECT_ID=${PROJECT_ID},LOCATION=${REGION}" \
    --memory 2Gi \
    --cpu 2

echo "======================================================================"
echo " ✅ StreamGuard AI Deployment Successful!"
echo " Live Service URL: $(gcloud run services describe ${SERVICE_NAME} --platform managed --region ${REGION} --format 'value(status.url)')"
echo "======================================================================"
