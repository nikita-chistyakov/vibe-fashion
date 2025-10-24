#!/usr/bin/env python3
"""
Test script for Vibe Fashion application
"""

import requests
import time
import subprocess
import sys
from pathlib import Path

def test_backend():
    """Test if backend is working"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_frontend():
    """Test if frontend is working"""
    try:
        response = requests.get("http://localhost:8501/", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running and accessible")
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend is not running")
        return False
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def test_api_endpoint():
    """Test the fashion workflow API endpoint"""
    try:
        # Test with a simple request
        test_data = {
            "base64_image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",  # 1x1 pixel
            "user_input": "casual outfit for work"
        }
        
        response = requests.post("http://localhost:8000/fashion-workflow", 
                               json=test_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ API endpoint is working")
                print(f"   Generated {len(result.get('images', []))} images")
                return True
            else:
                print(f"❌ API returned error: {result.get('error_message')}")
                return False
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Vibe Fashion Application")
    print("=" * 50)
    
    # Test backend
    print("\n1. Testing Backend...")
    backend_ok = test_backend()
    
    # Test frontend
    print("\n2. Testing Frontend...")
    frontend_ok = test_frontend()
    
    # Test API if backend is running
    if backend_ok:
        print("\n3. Testing API Endpoint...")
        api_ok = test_api_endpoint()
    else:
        print("\n3. Skipping API test (backend not running)")
        api_ok = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Backend: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"   Frontend: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    print(f"   API: {'✅ PASS' if api_ok else '❌ FAIL'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 Application is working correctly!")
        print("   🌐 Frontend: http://localhost:8501")
        print("   🔧 Backend: http://localhost:8000")
    else:
        print("\n⚠️  Some components are not working.")
        print("   Try running: python start_app.py")

if __name__ == "__main__":
    main()
