# Vibe Fashion - Google Cloud Run Deployment Guide

This guide will walk you through deploying the Vibe Fashion application to Google Cloud Run.

## 📋 Prerequisites

Before you begin, ensure you have:

1. **Google Cloud Account**: Sign up at [cloud.google.com](https://cloud.google.com)
2. **Google Cloud Project**: Create a new project or use an existing one
3. **gcloud CLI**: Install from [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
4. **Billing Enabled**: Enable billing for your Google Cloud project
5. **Required APIs**: The deployment script will enable these automatically, but you can do it manually:
   - Cloud Run API
   - Cloud Build API
   - Artifact Registry API

## 🏗️ Architecture

The application consists of three services:

1. **Backend** (FastAPI): Python backend with fashion workflow processing
2. **Frontend** (Next.js): React-based user interface
3. **Ollama** (Already deployed): LLM service for text generation

## 🚀 Quick Start Deployment

### Step 1: Authenticate with Google Cloud

```bash
gcloud auth login
gcloud auth application-default login
```

### Step 2: Set Your Project ID

```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_REGION=europe-west1
```

### Step 3: Make the Deployment Script Executable

```bash
chmod +x deploy.sh
```

### Step 4: Deploy All Services

```bash
./deploy.sh
```

This will deploy both the backend and frontend services.

#### Deploy Individual Services

Deploy only the backend:
```bash
./deploy.sh --backend-only
```

Deploy only the frontend:
```bash
./deploy.sh --frontend-only
```

## 📝 Manual Deployment Steps

If you prefer to deploy manually or need more control:

### Deploy Backend

```bash
cd services/backend

# Deploy to Cloud Run
gcloud run deploy vibe-fashion-backend \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars "DEBUG=False" \
  --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=True" \
  --set-env-vars "GOOGLE_CLOUD_LOCATION=europe-west1" \
  --set-env-vars "OLLAMA_API_BASE=https://ollama-153939933605.europe-west1.run.app" \
  --set-env-vars "GEMMA_MODEL_NAME=gemma3:12b"

cd ../..
```

### Deploy Frontend

```bash
cd frontend

# Get your backend URL first
BACKEND_URL=$(gcloud run services describe vibe-fashion-backend \
  --platform managed \
  --region europe-west1 \
  --format 'value(status.url)')

# Deploy to Cloud Run
gcloud run deploy vibe-fashion-frontend \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 60 \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars "NEXT_PUBLIC_API_URL=$BACKEND_URL"

cd ..
```

## 🔧 Environment Variables

### Backend Environment Variables

Required environment variables for the backend service:

```bash
# API Configuration
DEBUG=False                              # Set to False for production
API_HOST=0.0.0.0                         # Host to bind to
PORT=8080                                # Port (set by Cloud Run automatically)

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id     # Your GCP project ID
GOOGLE_CLOUD_LOCATION=europe-west1       # GCP region
GOOGLE_GENAI_USE_VERTEXAI=True          # Use Vertex AI for Google's Gemini
GOOGLE_API=your-google-api-key          # Google API key (if needed)

# Ollama Configuration
OLLAMA_API_BASE=https://ollama-153939933605.europe-west1.run.app  # Ollama service URL
GEMMA_MODEL_NAME=gemma3:12b             # Model name to use
```

### Frontend Environment Variables

Required environment variables for the frontend service:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=https://your-backend-service.run.app  # Your backend Cloud Run URL
```

## 🔐 Setting Environment Variables

### Via gcloud CLI

```bash
# Set a single environment variable
gcloud run services update vibe-fashion-backend \
  --region europe-west1 \
  --set-env-vars "DEBUG=False"

# Set multiple environment variables
gcloud run services update vibe-fashion-backend \
  --region europe-west1 \
  --set-env-vars "DEBUG=False,GOOGLE_CLOUD_LOCATION=europe-west1"
```

### Via Google Cloud Console

1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Select your service
3. Click "Edit & Deploy New Revision"
4. Go to "Variables & Secrets" tab
5. Add your environment variables
6. Click "Deploy"

## 🔒 Security Considerations

### Authentication

By default, the services are deployed with `--allow-unauthenticated`. For production:

1. **Remove public access**:
   ```bash
   gcloud run services remove-iam-policy-binding vibe-fashion-backend \
     --region europe-west1 \
     --member="allUsers" \
     --role="roles/run.invoker"
   ```

2. **Add specific users/services**:
   ```bash
   gcloud run services add-iam-policy-binding vibe-fashion-backend \
     --region europe-west1 \
     --member="user:your-email@example.com" \
     --role="roles/run.invoker"
   ```

### Secrets Management

For sensitive data like API keys, use Google Secret Manager:

```bash
# Create a secret
echo -n "your-api-key" | gcloud secrets create google-api-key \
  --data-file=-

# Grant Cloud Run access to the secret
gcloud secrets add-iam-policy-binding google-api-key \
  --member="serviceAccount:your-project-number-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Deploy with secret
gcloud run deploy vibe-fashion-backend \
  --set-secrets="GOOGLE_API=google-api-key:latest"
```

## 📊 Monitoring and Logging

### View Logs

```bash
# Backend logs
gcloud run services logs read vibe-fashion-backend \
  --region europe-west1 \
  --limit 50

# Frontend logs
gcloud run services logs read vibe-fashion-frontend \
  --region europe-west1 \
  --limit 50
```

### View in Console

Access logs at: [Cloud Run Logs](https://console.cloud.google.com/run)

## 💰 Cost Optimization

### Adjust Resources

Modify the deployment to use fewer resources:

```bash
gcloud run services update vibe-fashion-backend \
  --region europe-west1 \
  --memory 1Gi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 5
```

### Set Request Limits

Cloud Run charges based on:
- CPU allocation time
- Memory allocation time
- Number of requests
- Egress traffic

Tips:
- Set `--min-instances 0` to scale to zero when not in use
- Use `--cpu-throttling` for cost savings if response time is not critical
- Set appropriate `--max-instances` to control costs

## 🔄 Continuous Deployment

### Using GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches:
      - main

env:
  PROJECT_ID: your-project-id
  REGION: europe-west1

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write

    steps:
      - uses: actions/checkout@v4

      - id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: 'projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_NAME/providers/PROVIDER_NAME'
          service_account: 'SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com'

      - name: Deploy Backend
        uses: google-github-actions/deploy-cloudrun@v2
        with:
          service: vibe-fashion-backend
          region: ${{ env.REGION }}
          source: ./services/backend
          env_vars: |
            DEBUG=False
            GOOGLE_GENAI_USE_VERTEXAI=True

  deploy-frontend:
    runs-on: ubuntu-latest
    needs: deploy-backend
    permissions:
      contents: read
      id-token: write

    steps:
      - uses: actions/checkout@v4

      - id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: 'projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_NAME/providers/PROVIDER_NAME'
          service_account: 'SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com'

      - name: Get Backend URL
        id: backend
        run: |
          BACKEND_URL=$(gcloud run services describe vibe-fashion-backend \
            --region ${{ env.REGION }} \
            --format 'value(status.url)')
          echo "url=$BACKEND_URL" >> $GITHUB_OUTPUT

      - name: Deploy Frontend
        uses: google-github-actions/deploy-cloudrun@v2
        with:
          service: vibe-fashion-frontend
          region: ${{ env.REGION }}
          source: ./frontend
          env_vars: |
            NEXT_PUBLIC_API_URL=${{ steps.backend.outputs.url }}
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Build Failures

**Error**: "Could not find dependency file"

**Solution**: Ensure all necessary files are not in `.dockerignore`

#### 2. Memory Issues

**Error**: "Memory limit exceeded"

**Solution**: Increase memory allocation:
```bash
gcloud run services update vibe-fashion-backend \
  --memory 4Gi
```

#### 3. Timeout Errors

**Error**: "Request timeout"

**Solution**: Increase timeout:
```bash
gcloud run services update vibe-fashion-backend \
  --timeout 600
```

#### 4. CORS Errors

**Error**: "CORS policy blocked"

**Solution**: Update backend CORS configuration in `api.py` to include your frontend URL

### Health Checks

Test your deployed services:

```bash
# Backend health check
curl https://your-backend-url.run.app/

# Should return: {"message": "Vibe Fashion API is running!", "status": "healthy"}
```

## 📚 Additional Resources

- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [Best Practices for Cloud Run](https://cloud.google.com/run/docs/best-practices)
- [Cloud Run Samples](https://github.com/GoogleCloudPlatform/cloud-run-samples)

## 🆘 Support

For issues specific to this deployment:
1. Check the logs using `gcloud run services logs read`
2. Review the Cloud Run service status in the console
3. Verify all environment variables are set correctly

For Google Cloud issues:
- [Google Cloud Support](https://cloud.google.com/support)
- [Stack Overflow - google-cloud-run tag](https://stackoverflow.com/questions/tagged/google-cloud-run)

## 🎉 Next Steps

After deployment:

1. **Set up a custom domain**: [Cloud Run Custom Domains](https://cloud.google.com/run/docs/mapping-custom-domains)
2. **Configure SSL**: Cloud Run provides SSL certificates automatically
3. **Set up monitoring**: Use Cloud Monitoring for alerts and dashboards
4. **Implement CI/CD**: Automate deployments with GitHub Actions or Cloud Build
5. **Add authentication**: Implement user authentication if needed

---

Happy deploying! 🚀

