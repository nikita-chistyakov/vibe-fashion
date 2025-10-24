#!/usr/bin/env python3
"""
Simple startup script for Vibe Fashion Streamlit app
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Start the Vibe Fashion application"""
    
    print("🎯 Vibe Fashion - AI Fashion Assistant")
    print("=" * 50)
    
    # Check if we're in the right directory
    project_root = Path(__file__).parent
    backend_dir = project_root / "services" / "backend"
    
    if not backend_dir.exists():
        print("❌ Backend directory not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Clean up any existing processes
    print("🧹 Cleaning up ports...")
    try:
        subprocess.run([sys.executable, "cleanup_ports.py"], check=True)
    except subprocess.CalledProcessError:
        print("⚠️  Could not clean up ports (this is usually fine)")
    
    # Check if .env file exists in backend
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("⚠️  No .env file found. Creating default configuration...")
        try:
            # Run the environment setup
            subprocess.run([sys.executable, "setup_environment.py"], check=True)
            print("✅ Environment configured")
        except subprocess.CalledProcessError:
            print("❌ Failed to setup environment. Please run setup_environment.py manually.")
            sys.exit(1)
    
    print("\n🚀 Starting application...")
    print("📱 Frontend will be available at: http://localhost:8501")
    print("🔧 Backend will be available at: http://localhost:8000")
    print("\nPress Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        # Run the full app
        subprocess.run([sys.executable, "run_full_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Application failed to start: {e}")
        print("\n💡 Try running the test script to diagnose issues:")
        print("   python test_app.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
