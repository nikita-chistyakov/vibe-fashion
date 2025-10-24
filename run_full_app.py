#!/usr/bin/env python3
"""
Unified runner for Vibe Fashion Streamlit app with backend
"""

import subprocess
import sys
import time
import threading
import requests
import os
from pathlib import Path
import signal

class AppRunner:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.backend_ready = False
        
    def check_backend_health(self):
        """Check if backend is running and healthy"""
        try:
            response = requests.get("http://localhost:8000/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def wait_for_backend(self, timeout=30):
        """Wait for backend to be ready"""
        print("⏳ Waiting for backend to start...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.check_backend_health():
                print("✅ Backend is ready!")
                self.backend_ready = True
                return True
            time.sleep(1)
        
        print("❌ Backend failed to start within timeout")
        return False
    
    def start_backend(self):
        """Start the backend server"""
        print("🚀 Starting backend server...")
        
        backend_dir = Path(__file__).parent / "services" / "backend"
        
        try:
            # Start backend with uv
            self.backend_process = subprocess.Popen(
                ['uv', 'run', 'python', 'main.py'],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for backend to be ready
            if self.wait_for_backend():
                return True
            else:
                self.stop_backend()
                return False
                
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False
    
    def start_frontend(self):
        """Start the Streamlit frontend"""
        print("🚀 Starting Streamlit frontend...")
        
        # Find an available port
        import socket
        def find_free_port():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', 0))
                s.listen(1)
                port = s.getsockname()[1]
            return port
        
        # Try default port first, then find a free one
        for port in [8501, find_free_port()]:
            try:
                self.frontend_process = subprocess.Popen(
                    [sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py',
                     '--server.port', str(port), '--server.address', '0.0.0.0'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Give it a moment to start
                time.sleep(2)
                
                # Check if it's still running
                if self.frontend_process.poll() is None:
                    print(f"✅ Frontend started on port {port}")
                    return True
                else:
                    stdout, stderr = self.frontend_process.communicate()
                    if "Port" in stderr and "already in use" in stderr:
                        print(f"⚠️  Port {port} in use, trying next port...")
                        continue
                    else:
                        print(f"❌ Frontend failed: {stderr}")
                        return False
                        
            except Exception as e:
                print(f"❌ Failed to start frontend on port {port}: {e}")
                continue
        
        print("❌ Could not find an available port for frontend")
        return False
    
    def stop_backend(self):
        """Stop the backend server"""
        if self.backend_process:
            print("🛑 Stopping backend server...")
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
            self.backend_process = None
    
    def stop_frontend(self):
        """Stop the frontend server"""
        if self.frontend_process:
            print("🛑 Stopping frontend server...")
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
            self.frontend_process = None
    
    def cleanup(self):
        """Clean up all processes"""
        self.stop_backend()
        self.stop_frontend()
    
    def run(self):
        """Run the complete application"""
        print("🎯 Starting Vibe Fashion Application")
        print("=" * 50)
        
        # Setup signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            print("\n🛑 Shutting down...")
            self.cleanup()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            # Start backend
            if not self.start_backend():
                print("❌ Failed to start backend. Exiting.")
                return False
            
            # Start frontend
            if not self.start_frontend():
                print("❌ Failed to start frontend. Exiting.")
                self.stop_backend()
                return False
            
            print("\n✅ Application is running!")
            print("🌐 Frontend: http://localhost:8501")
            print("🔧 Backend: http://localhost:8000")
            print("\nPress Ctrl+C to stop the application")
            
            # Monitor processes
            while True:
                # Check if backend is still running
                if self.backend_process and self.backend_process.poll() is not None:
                    print("❌ Backend process died unexpectedly")
                    break
                
                # Check if frontend is still running
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("❌ Frontend process died unexpectedly")
                    break
                
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n👋 Shutting down application...")
        finally:
            self.cleanup()

def main():
    """Main function"""
    runner = AppRunner()
    runner.run()

if __name__ == "__main__":
    main()
