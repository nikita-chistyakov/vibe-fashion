#!/usr/bin/env python3
"""
Streamlit app runner for Vibe Fashion
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run the Streamlit app"""
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    streamlit_app_path = script_dir / "streamlit_app.py"
    
    # Check if the streamlit app exists
    if not streamlit_app_path.exists():
        print(f"Error: streamlit_app.py not found at {streamlit_app_path}")
        sys.exit(1)
    
    print("🚀 Starting Vibe Fashion Streamlit App...")
    print("=" * 50)
    print("📱 Frontend: Streamlit will be available at http://localhost:8501")
    print("🔧 Backend: Make sure your FastAPI backend is running at http://localhost:8000")
    print("=" * 50)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(streamlit_app_path),
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
