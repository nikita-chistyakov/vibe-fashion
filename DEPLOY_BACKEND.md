# 🚀 Deploy Vibe Fashion Backend

This guide shows you how to deploy your FastAPI backend to various cloud platforms.

## 🎯 Quick Deploy Options

### Option 1: Railway (Recommended - Easiest)

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect your GitHub** repository
3. **Create new project** from GitHub repo
4. **Railway will auto-detect** the configuration from `railway.json`
5. **Set environment variables** in Railway dashboard:
   - `GOOGLE_API` - Your Google API key
   - `OLLAMA_API_BASE` - https://ollama-153939933605.europe-west1.run.app
   - `GEMMA_MODEL_NAME` - gemma3:12b
6. **Deploy!** Railway will give you a URL like `https://your-app.railway.app`

### Option 2: Render (Free Tier Available)

1. **Sign up** at [render.com](https://render.com)
2. **Connect your GitHub** repository
3. **Create new Web Service**
4. **Use these settings**:
   - Build Command: `cd services/backend && uv sync`
   - Start Command: `cd services/backend && uv run python main.py`
   - Environment: Python 3
5. **Set environment variables** in Render dashboard
6. **Deploy!** Render will give you a URL like `https://your-app.onrender.com`

### Option 3: Google Cloud Run

1. **Install Google Cloud CLI**
2. **Run these commands**:
   ```bash
   # Build and push to Google Container Registry
   cd services/backend
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/vibe-fashion-backend
   
   # Deploy to Cloud Run
   gcloud run deploy vibe-fashion-backend \
     --image gcr.io/YOUR_PROJECT_ID/vibe-fashion-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

## 🔧 Environment Variables Needed

Set these in your deployment platform:

```bash
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
GOOGLE_API=your_google_api_key_here
OLLAMA_API_BASE=https://ollama-153939933605.europe-west1.run.app
GEMMA_MODEL_NAME=gemma3:12b
```

## 📱 Update Streamlit Frontend

After deploying your backend, update the Streamlit app to use the new backend URL:

1. **In Streamlit sidebar**, change the backend URL from `http://localhost:8000` to your deployed URL
2. **Or update the default** in `streamlit_app.py`:

```python
# Change this line in streamlit_app.py
backend_url = st.text_input(
    "Backend URL",
    value="https://your-deployed-backend-url.com",  # Your deployed URL here
    help="URL of your FastAPI backend server"
)
```

## 🧪 Test Your Deployment

1. **Check backend health**: Visit `https://your-backend-url.com/`
2. **Should return**: `{"message":"Vibe Fashion API is running!","status":"healthy"}`
3. **Test Streamlit**: Upload an image and make a request
4. **Check logs** in your deployment platform for any errors

## 🚨 Troubleshooting

### Common Issues:

1. **"Could not connect to backend"**
   - Check if backend URL is correct
   - Verify backend is running (visit the URL directly)
   - Check CORS settings in backend

2. **"API key not valid"**
   - Set `GOOGLE_API` environment variable
   - Get API key from [Google AI Studio](https://aistudio.google.com/)

3. **"Ollama API failed"**
   - This is expected - the fallback system will handle it
   - You'll get placeholder images instead

4. **Backend timeout**
   - Increase timeout in deployment settings
   - Check if all dependencies are installed

## 💡 Pro Tips

- **Railway** is the easiest for beginners
- **Render** has a generous free tier
- **Google Cloud Run** scales automatically
- Always test locally first
- Check deployment logs for errors

## 🔄 Continuous Deployment

All platforms support automatic deployment:
- Push to `main` branch → Auto-deploy
- Set up environment variables once
- Monitor logs for issues

Choose the platform that works best for you! 🚀
