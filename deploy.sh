#!/bin/bash

# Vibe Fashion - Google Cloud Run Deployment Script
# This script deploys the backend and frontend services to Google Cloud Run

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-your-project-id}"
REGION="${GOOGLE_CLOUD_REGION:-europe-west1}"
BACKEND_SERVICE_NAME="${BACKEND_SERVICE_NAME:-vibe-fashion-backend}"
FRONTEND_SERVICE_NAME="${FRONTEND_SERVICE_NAME:-vibe-fashion-frontend}"

# Print functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    print_error "gcloud CLI is not installed. Please install it from https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if project ID is set
if [ "$PROJECT_ID" = "your-project-id" ]; then
    print_error "Please set your Google Cloud project ID"
    echo "You can do this by:"
    echo "  export GOOGLE_CLOUD_PROJECT=your-project-id"
    echo "  Or edit this script and change the PROJECT_ID variable"
    exit 1
fi

# Authenticate and set project
print_info "Setting Google Cloud project to: $PROJECT_ID"
gcloud config set project "$PROJECT_ID"

# Enable required APIs
print_info "Enabling required Google Cloud APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Function to deploy backend
deploy_backend() {
    print_info "Deploying Backend Service..."
    
    cd services/backend
    
    gcloud run deploy "$BACKEND_SERVICE_NAME" \
        --source . \
        --platform managed \
        --region "$REGION" \
        --allow-unauthenticated \
        --memory 2Gi \
        --cpu 2 \
        --timeout 300 \
        --min-instances 0 \
        --max-instances 10 \
        --set-env-vars "DEBUG=False" \
        --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=True" \
        --set-env-vars "GOOGLE_CLOUD_LOCATION=$REGION" \
        --quiet
    
    # Get backend URL
    BACKEND_URL=$(gcloud run services describe "$BACKEND_SERVICE_NAME" \
        --platform managed \
        --region "$REGION" \
        --format 'value(status.url)')
    
    print_info "Backend deployed successfully at: $BACKEND_URL"
    
    cd ../..
    
    echo "$BACKEND_URL" > .backend_url
}

# Function to deploy frontend
deploy_frontend() {
    print_info "Deploying Frontend Service..."
    
    # Read backend URL if it exists
    if [ -f .backend_url ]; then
        BACKEND_URL=$(cat .backend_url)
    else
        print_warning "Backend URL not found. Please set NEXT_PUBLIC_API_URL manually"
        BACKEND_URL="https://your-backend-url"
    fi
    
    cd frontend
    
    gcloud run deploy "$FRONTEND_SERVICE_NAME" \
        --source . \
        --platform managed \
        --region "$REGION" \
        --allow-unauthenticated \
        --memory 1Gi \
        --cpu 1 \
        --timeout 60 \
        --min-instances 0 \
        --max-instances 10 \
        --set-env-vars "NEXT_PUBLIC_API_URL=$BACKEND_URL" \
        --quiet
    
    # Get frontend URL
    FRONTEND_URL=$(gcloud run services describe "$FRONTEND_SERVICE_NAME" \
        --platform managed \
        --region "$REGION" \
        --format 'value(status.url)')
    
    print_info "Frontend deployed successfully at: $FRONTEND_URL"
    
    cd ..
}

# Main deployment flow
print_info "Starting deployment to Google Cloud Run..."
print_info "Project: $PROJECT_ID"
print_info "Region: $REGION"
echo ""

# Parse command line arguments
DEPLOY_BACKEND=true
DEPLOY_FRONTEND=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-only)
            DEPLOY_FRONTEND=false
            shift
            ;;
        --frontend-only)
            DEPLOY_BACKEND=false
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Usage: $0 [--backend-only|--frontend-only]"
            exit 1
            ;;
    esac
done

# Deploy services
if [ "$DEPLOY_BACKEND" = true ]; then
    deploy_backend
fi

if [ "$DEPLOY_FRONTEND" = true ]; then
    deploy_frontend
fi

# Print summary
echo ""
print_info "========================================"
print_info "Deployment Summary"
print_info "========================================"

if [ "$DEPLOY_BACKEND" = true ]; then
    BACKEND_URL=$(gcloud run services describe "$BACKEND_SERVICE_NAME" \
        --platform managed \
        --region "$REGION" \
        --format 'value(status.url)' 2>/dev/null || echo "Not deployed")
    echo "Backend URL: $BACKEND_URL"
fi

if [ "$DEPLOY_FRONTEND" = true ]; then
    FRONTEND_URL=$(gcloud run services describe "$FRONTEND_SERVICE_NAME" \
        --platform managed \
        --region "$REGION" \
        --format 'value(status.url)' 2>/dev/null || echo "Not deployed")
    echo "Frontend URL: $FRONTEND_URL"
fi

print_info "========================================"
print_info "Deployment completed successfully! 🎉"

