#!/usr/bin/env python3
"""
Clean up any processes using ports 8000 and 8501
"""

import subprocess
import sys

def kill_processes_on_port(port):
    """Kill processes using a specific port"""
    try:
        # Find processes using the port
        result = subprocess.run(['lsof', '-ti', f':{port}'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            print(f"🔍 Found processes on port {port}: {pids}")
            
            for pid in pids:
                if pid.strip():
                    try:
                        subprocess.run(['kill', '-9', pid.strip()], check=True)
                        print(f"✅ Killed process {pid} on port {port}")
                    except subprocess.CalledProcessError:
                        print(f"⚠️  Could not kill process {pid} (may already be dead)")
        else:
            print(f"✅ Port {port} is free")
            
    except Exception as e:
        print(f"❌ Error checking port {port}: {e}")

def main():
    """Clean up ports 8000 and 8501"""
    print("🧹 Cleaning up ports...")
    
    # Clean up backend port
    kill_processes_on_port(8000)
    
    # Clean up frontend port  
    kill_processes_on_port(8501)
    
    print("✅ Port cleanup complete")

if __name__ == "__main__":
    main()
