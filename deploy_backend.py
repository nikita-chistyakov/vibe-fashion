#!/usr/bin/env python3
"""
Backend deployment helper script
"""

import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check if uv is available
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        print("✅ uv is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ uv not found. Please install uv first: https://docs.astral.sh/uv/getting-started/installation/")
        return False
    
    return True

def create_env_file():
    """Create .env file for local development"""
    env_path = Path("services/backend/.env")
    
    if env_path.exists():
        print("✅ .env file already exists")
        return
    
    print("📝 Creating .env file for local development...")
    
    env_content = """# Vibe Fashion Backend Environment Variables
# Copy this file and fill in your actual values

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Google Cloud Configuration (get from https://aistudio.google.com/)
GOOGLE_API=your_google_api_key_here

# Ollama Configuration
OLLAMA_API_BASE=https://ollama-153939933605.europe-west1.run.app
GEMMA_MODEL_NAME=gemma3:12b

# Image Processing Configuration
MAX_IMAGE_SIZE=1024,1024
ALLOWED_IMAGE_FORMATS=JPEG,PNG,WEBP
"""
    
    with open(env_path, "w") as f:
        f.write(env_content)
    
    print(f"✅ Created {env_path}")
    print("⚠️  Please edit the .env file and add your Google API key!")

def show_deployment_options():
    """Show deployment options"""
    print("\n🚀 Backend Deployment Options:")
    print("=" * 50)
    
    print("\n1. 🚄 Railway (Recommended - Easiest)")
    print("   - Go to https://railway.app")
    print("   - Connect your GitHub repo")
    print("   - Railway will auto-detect configuration")
    print("   - Set environment variables in dashboard")
    print("   - Deploy!")
    
    print("\n2. 🎨 Render (Free Tier)")
    print("   - Go to https://render.com")
    print("   - Connect your GitHub repo")
    print("   - Create new Web Service")
    print("   - Use the settings from render.yaml")
    print("   - Set environment variables")
    print("   - Deploy!")
    
    print("\n3. ☁️ Google Cloud Run")
    print("   - Install Google Cloud CLI")
    print("   - Run: gcloud builds submit --tag gcr.io/PROJECT/vibe-fashion")
    print("   - Run: gcloud run deploy --image gcr.io/PROJECT/vibe-fashion")
    
    print("\n4. 🐳 Docker (Any Platform)")
    print("   - Build: docker build -t vibe-fashion-backend services/backend/")
    print("   - Run: docker run -p 8000:8000 vibe-fashion-backend")
    
    print("\n📋 Required Environment Variables:")
    print("   - GOOGLE_API: Your Google API key")
    print("   - OLLAMA_API_BASE: https://ollama-153939933605.europe-west1.run.app")
    print("   - GEMMA_MODEL_NAME: gemma3:12b")

def main():
    """Main deployment helper"""
    print("🚀 Vibe Fashion Backend Deployment Helper")
    print("=" * 50)
    
    if not check_requirements():
        sys.exit(1)
    
    create_env_file()
    show_deployment_options()
    
    print("\n✅ Setup complete!")
    print("\n📖 For detailed instructions, see DEPLOY_BACKEND.md")
    print("\n🎯 Next steps:")
    print("1. Choose a deployment platform")
    print("2. Set up your Google API key")
    print("3. Deploy your backend")
    print("4. Update Streamlit with the new backend URL")

if __name__ == "__main__":
    main()
