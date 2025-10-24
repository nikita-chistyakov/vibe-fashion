#!/usr/bin/env python3
"""
Setup script for Vibe Fashion Streamlit frontend
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def main():
    """Setup the Streamlit environment"""
    
    print("🚀 Setting up Vibe Fashion Streamlit Frontend")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("streamlit_app.py").exists():
        print("❌ Error: streamlit_app.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    
    # Check if uv is available
    if run_command("which uv", "Checking for uv"):
        print("🔧 Using uv to install dependencies...")
        if not run_command("uv add streamlit requests pillow", "Installing Streamlit dependencies with uv"):
            print("⚠️  uv installation failed, trying pip...")
            run_command("pip install streamlit requests pillow", "Installing Streamlit dependencies with pip")
    else:
        print("🔧 Using pip to install dependencies...")
        if not run_command("pip install -r requirements.txt", "Installing dependencies from requirements.txt"):
            print("❌ Failed to install dependencies")
            sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start your FastAPI backend: cd services/backend && python main.py")
    print("2. Start the Streamlit frontend: python run_streamlit.py")
    print("3. Open your browser to http://localhost:8501")
    print("\n💡 Tips:")
    print("- Make sure your backend is running on http://localhost:8000")
    print("- You can change the backend URL in the Streamlit sidebar")
    print("- Upload clear images for best results")

if __name__ == "__main__":
    main()
