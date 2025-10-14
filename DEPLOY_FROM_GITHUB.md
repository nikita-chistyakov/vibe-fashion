# 🌐 Deploy Vibe Fashion from GitHub via Google Cloud Console

This guide shows you how to deploy your application directly from your GitHub repository using the Google Cloud Console web interface - no command line needed!

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be pushed to GitHub
2. **Google Cloud Account**: Sign up at [cloud.google.com](https://cloud.google.com)
3. **Billing Enabled**: Enable billing for your Google Cloud project

## 🚀 Step-by-Step Deployment

### Part 1: Enable Required APIs

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select or create a project
3. Go to **APIs & Services** → **Library**
4. Search and enable these APIs:
   - **Cloud Run API**
   - **Cloud Build API**
   - **Artifact Registry API**

### Part 2: Connect GitHub Repository

#### First Time Setup:

1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Click **"Create Service"**
3. Select **"Continuously deploy from a repository (source or function)"**
4. Click **"Set up with Cloud Build"**
5. Click **"Manage Connected Repositories"**
6. Click **"Connect Repository"**
7. Select **"GitHub"**
8. Authorize Google Cloud Build to access your GitHub
9. Select your repository: `vibe-fashion` (or your repo name)
10. Click **"Next"**

### Part 3: Deploy Backend Service

1. After connecting your repository, configure the build:

   **Build Configuration:**
   - **Branch**: `main` (or your default branch)
   - **Build Type**: `Dockerfile`
   - **Source location**: `/services/backend/dockerfile`
   
2. Click **"Save"** and then **"Create"**

3. Configure the service:

   **Service Settings:**
   - **Service name**: `vibe-fashion-backend`
   - **Region**: `europe-west1` (or your preferred region)
   - **Authentication**: Select "Allow unauthenticated invocations" (for testing)
   
4. Click **"Container, Networking, Security"** to expand advanced settings:

   **Container tab:**
   - **Memory**: `2 GiB`
   - **CPU**: `2`
   - **Request timeout**: `300` seconds
   - **Container port**: `8000`
   
   **Variables & Secrets tab:** Click "+ ADD VARIABLE" and add:
   ```
   DEBUG=False
   GOOGLE_GENAI_USE_VERTEXAI=True
   GOOGLE_CLOUD_LOCATION=europe-west1
   OLLAMA_API_BASE=https://ollama-153939933605.europe-west1.run.app
   GEMMA_MODEL_NAME=gemma3:12b
   ```
   
   **Autoscaling tab:**
   - **Minimum instances**: `0`
   - **Maximum instances**: `10`

5. Click **"Create"** and wait for deployment (5-10 minutes)

6. **Copy the Backend URL** displayed after deployment (you'll need it for the frontend)
   - Example: `https://vibe-fashion-backend-xxxxx-ew.a.run.app`

### Part 4: Deploy Frontend Service

1. Go back to [Cloud Run Console](https://console.cloud.google.com/run)
2. Click **"Create Service"**
3. Select **"Continuously deploy from a repository"**
4. Click **"Set up with Cloud Build"**

5. **Repository Configuration:**
   - Select your already connected repository
   - **Branch**: `main`
   - **Build Type**: `Dockerfile`
   - **Source location**: `/frontend/Dockerfile`
   
6. Click **"Save"** and then **"Create"**

7. Configure the service:

   **Service Settings:**
   - **Service name**: `vibe-fashion-frontend`
   - **Region**: `europe-west1` (same as backend)
   - **Authentication**: "Allow unauthenticated invocations"
   
8. Click **"Container, Networking, Security"**:

   **Container tab:**
   - **Memory**: `1 GiB`
   - **CPU**: `1`
   - **Request timeout**: `60` seconds
   - **Container port**: `3000`
   
   **Variables & Secrets tab:** Click "+ ADD VARIABLE" and add:
   ```
   NEXT_PUBLIC_API_URL=<YOUR_BACKEND_URL_FROM_STEP_3.6>
   ```
   Replace `<YOUR_BACKEND_URL_FROM_STEP_3.6>` with your actual backend URL
   
   **Autoscaling tab:**
   - **Minimum instances**: `0`
   - **Maximum instances**: `10`

9. Click **"Create"** and wait for deployment (5-10 minutes)

10. **Your app is live!** Click on the Frontend URL to access your application

## 🔄 Enable Continuous Deployment

Good news! Continuous deployment is already enabled. When you push to your GitHub repository:

1. Cloud Build automatically detects the push
2. Builds a new container image
3. Deploys the new version to Cloud Run
4. Your app updates with zero downtime!

### Configure Deployment Triggers

To customize when deployments happen:

1. Go to [Cloud Build Triggers](https://console.cloud.google.com/cloud-build/triggers)
2. Find your triggers (created automatically):
   - `vibe-fashion-backend-trigger`
   - `vibe-fashion-frontend-trigger`
3. Click on a trigger to edit
4. Customize:
   - **Branch pattern**: Which branches trigger deployment
   - **Included files**: Only deploy when specific files change
   - **Ignored files**: Skip deployment for certain file changes

**Example - Only deploy backend when backend files change:**
```
Included files filter: services/backend/**
```

**Example - Ignore README changes:**
```
Ignored files filter: README.md, docs/**
```

## 🔐 Managing Secrets

For sensitive data like API keys:

1. Go to [Secret Manager](https://console.cloud.google.com/security/secret-manager)
2. Click **"Create Secret"**
3. Enter:
   - **Name**: `google-api-key` (or any name)
   - **Secret value**: Your actual API key
4. Click **"Create Secret"**

5. Add secret to your Cloud Run service:
   - Go to your service in Cloud Run Console
   - Click **"Edit & Deploy New Revision"**
   - Go to **"Variables & Secrets"** tab
   - Click **"Reference a Secret"**
   - Select your secret
   - Set **Environment variable name**: `GOOGLE_API`
   - Click **"Done"** and **"Deploy"**

## 📊 Monitoring & Logs

### View Logs:

1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Click on your service
3. Click the **"Logs"** tab
4. View real-time logs and errors

### Set Up Alerts:

1. Click **"Metrics"** tab
2. Click **"Create Alert"**
3. Configure conditions (e.g., error rate, latency)
4. Add notification channels (email, SMS)

## 🛠️ Managing Your Deployment

### Update Environment Variables:

1. Go to your service in Cloud Run Console
2. Click **"Edit & Deploy New Revision"**
3. Go to **"Variables & Secrets"** tab
4. Update variables
5. Click **"Deploy"**

### Scale Your Service:

1. Click **"Edit & Deploy New Revision"**
2. Go to **"Autoscaling"** tab
3. Adjust:
   - Minimum instances (set to 1+ to reduce cold starts)
   - Maximum instances (control costs)
4. Click **"Deploy"**

### View Revisions:

1. Click **"Revisions"** tab
2. See all deployed versions
3. Roll back by routing traffic to a previous revision

### Custom Domain:

1. Click **"Manage Custom Domains"**
2. Click **"Add Mapping"**
3. Select your service
4. Enter your domain name
5. Verify domain ownership
6. Update DNS records as instructed

## 🎯 Quick Actions

### Temporarily Disable a Service:
1. Go to service → **Revisions**
2. Click **"Manage Traffic"**
3. Set traffic to **0%** for all revisions

### Delete a Service:
1. Go to service page
2. Click **"Delete"**
3. Confirm deletion

### Download Container Image:
1. Go to [Artifact Registry](https://console.cloud.google.com/artifacts)
2. Find your image
3. Click to view details
4. Use the pull command shown

## 💰 Cost Management

### Set Budget Alerts:

1. Go to [Billing](https://console.cloud.google.com/billing)
2. Click **"Budgets & alerts"**
3. Click **"Create Budget"**
4. Set your monthly budget
5. Configure alert thresholds (e.g., 50%, 90%, 100%)
6. Add email notifications

### View Costs:

1. Go to [Billing Reports](https://console.cloud.google.com/billing/reports)
2. Filter by:
   - Service: Cloud Run
   - Project: Your project
   - Time range: Custom

## 🐛 Troubleshooting

### Build Fails

**Check Build Logs:**
1. Go to [Cloud Build History](https://console.cloud.google.com/cloud-build/builds)
2. Click on the failed build
3. Review error messages
4. Common issues:
   - Missing files (check Dockerfile paths)
   - Build timeout (increase in trigger settings)
   - Missing dependencies (check package files)

### Service Not Responding

**Check Service Status:**
1. Go to service in Cloud Run Console
2. Check **"Metrics"** tab for errors
3. Check **"Logs"** tab for error messages
4. Verify environment variables are set correctly

### CORS Errors

1. Update your backend's `api.py` CORS settings
2. Add your frontend URL to allowed origins
3. Redeploy the backend service

## 📱 Mobile-Friendly Console

You can manage your deployments from your phone:
1. Install **Google Cloud Console** app (iOS/Android)
2. View logs, metrics, and service status
3. Update environment variables
4. Roll back deployments

## 🎓 Video Tutorials

Google Cloud official tutorials:
- [Deploy from GitHub](https://cloud.google.com/run/docs/continuous-deployment-with-cloud-build)
- [Cloud Run Quickstart](https://www.youtube.com/watch?v=nhwYc4StHIc)

## ✅ Deployment Checklist

- [ ] GitHub repository is public or Cloud Build has access
- [ ] Dockerfile paths are correct
- [ ] Environment variables are set
- [ ] Backend deployed successfully
- [ ] Backend URL copied
- [ ] Frontend deployed with backend URL
- [ ] Frontend accessible in browser
- [ ] Continuous deployment tested (make a commit and verify)
- [ ] Monitoring and alerts configured
- [ ] Budget alerts set up

## 🆘 Need Help?

If you encounter issues:

1. **Check Build Logs**: [Cloud Build History](https://console.cloud.google.com/cloud-build/builds)
2. **Check Service Logs**: Cloud Run → Your Service → Logs tab
3. **Check Status**: Cloud Run → Your Service → Overview
4. **Community Help**: [Stack Overflow - google-cloud-run](https://stackoverflow.com/questions/tagged/google-cloud-run)

## 🎉 Success!

Your application should now be:
- ✅ Deployed from GitHub
- ✅ Automatically updating on new commits
- ✅ Scaling based on traffic
- ✅ Accessible via HTTPS URLs
- ✅ Monitored with logging

---

**Next Steps:**
- Set up a custom domain
- Configure secrets for API keys
- Set up monitoring alerts
- Optimize costs by adjusting autoscaling

Happy deploying! 🚀

