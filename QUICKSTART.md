# 🚀 Quick Start - Deploy to Google Cloud Run

This is a simplified guide to get your Vibe Fashion app deployed quickly.

## Prerequisites

1. Install gcloud CLI: https://cloud.google.com/sdk/docs/install
2. Have a Google Cloud project with billing enabled

## Step-by-Step Deployment

### 1. Authenticate

```bash
gcloud auth login
gcloud auth application-default login
```

### 2. Set Your Project

```bash
# Replace with your actual project ID
export GOOGLE_CLOUD_PROJECT="your-project-id"
gcloud config set project $GOOGLE_CLOUD_PROJECT
```

### 3. Enable Required APIs

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### 4. Deploy Backend

```bash
cd services/backend

gcloud run deploy vibe-fashion-backend \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --set-env-vars "DEBUG=False,GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_CLOUD_LOCATION=europe-west1"

cd ../..
```

### 5. Get Backend URL

```bash
BACKEND_URL=$(gcloud run services describe vibe-fashion-backend \
  --region europe-west1 \
  --format 'value(status.url)')

echo "Backend URL: $BACKEND_URL"
```

### 6. Deploy Frontend

```bash
cd frontend

gcloud run deploy vibe-fashion-frontend \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --set-env-vars "NEXT_PUBLIC_API_URL=$BACKEND_URL"

cd ..
```

### 7. Get Frontend URL

```bash
FRONTEND_URL=$(gcloud run services describe vibe-fashion-frontend \
  --region europe-west1 \
  --format 'value(status.url)')

echo "🎉 Your app is live at: $FRONTEND_URL"
```

## Or Use the Automated Script

```bash
# Make script executable
chmod +x deploy.sh

# Set your project ID
export GOOGLE_CLOUD_PROJECT="your-project-id"

# Deploy everything
./deploy.sh
```

## Verify Deployment

Test your backend:
```bash
curl $BACKEND_URL
# Should return: {"message": "Vibe Fashion API is running!", "status": "healthy"}
```

Open your frontend in a browser:
```bash
open $FRONTEND_URL
```

## Need More Details?

See [DEPLOYMENT.md](./DEPLOYMENT.md) for:
- Environment variable configuration
- Security best practices
- Continuous deployment setup
- Troubleshooting
- Cost optimization

## Common Commands

```bash
# View backend logs
gcloud run services logs read vibe-fashion-backend --region europe-west1

# View frontend logs
gcloud run services logs read vibe-fashion-frontend --region europe-west1

# Update environment variables
gcloud run services update vibe-fashion-backend \
  --region europe-west1 \
  --set-env-vars "KEY=value"

# Delete services
gcloud run services delete vibe-fashion-backend --region europe-west1
gcloud run services delete vibe-fashion-frontend --region europe-west1
```

## Cost Estimate

With default settings:
- **Backend**: ~$0.05 - $0.10 per hour when active
- **Frontend**: ~$0.02 - $0.05 per hour when active
- Both scale to zero when not in use (no charge)

First 2 million requests per month are free on Cloud Run!

---

Need help? Check [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed documentation.

