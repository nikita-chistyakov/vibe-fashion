#!/usr/bin/env python3
"""
Test script for Vibe Fashion backend with Ollama Gemma 3B:12B on Google Cloud
"""

import asyncio
import base64
import io
import json
import os
import requests
from pathlib import Path
from PIL import Image
import time

# Configuration
OLLAMA_BASE_URL = "https://ollama-153939933605.europe-west1.run.app"
BACKEND_URL = "http://localhost:8000"  # Local backend
MODEL_NAME = "gemma3:12b"  # Updated to use 12B model


def create_test_image():
    """Create a simple test image for testing"""
    # Create a simple fashion-related test image
    img = Image.new("RGB", (300, 400), color="lightblue")

    # Add some simple shapes to make it look like clothing
    from PIL import ImageDraw

    draw = ImageDraw.Draw(img)

    # Draw a simple shirt shape
    draw.rectangle([100, 50, 200, 200], fill="white", outline="black", width=2)
    draw.rectangle([80, 180, 220, 300], fill="navy", outline="black", width=2)

    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes.getvalue()


def test_ollama_connection():
    """Test connection to Ollama service"""
    print("🔍 Testing Ollama connection...")

    try:
        # Test if Ollama service is accessible
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Ollama service is accessible")
            print(
                f"📋 Available models: {[model['name'] for model in models.get('models', [])]}"
            )
            return True
        else:
            print(f"❌ Ollama service returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to Ollama service: {e}")
        return False


def test_ollama_chat():
    """Test direct chat with Ollama"""
    print("\n🤖 Testing direct Ollama chat...")

    try:
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": "Hello! Can you help me with fashion advice?",
                }
            ],
            "stream": False,
        }

        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat", json=payload, timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Ollama chat successful")
            print(
                f"💬 Response: {result.get('message', {}).get('content', 'No content')[:100]}..."
            )
            return True
        else:
            print(f"❌ Ollama chat failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama chat request failed: {e}")
        return False


def test_backend_health():
    """Test backend health endpoint"""
    print("\n🏥 Testing backend health...")

    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Backend is healthy: {result}")
            return True
        else:
            print(f"❌ Backend health check failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend health check failed: {e}")
        return False


def test_backend_chat():
    """Test backend chat endpoint with image"""
    print("\n💬 Testing backend chat endpoint...")

    try:
        # Create test image
        test_image = create_test_image()

        # Prepare form data
        files = {"image": ("test_fashion.png", test_image, "image/png")}
        data = {
            "text": "What do you think about this outfit? Can you suggest some improvements?"
        }

        response = requests.post(
            f"{BACKEND_URL}/chat", files=files, data=data, timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Backend chat successful")
            print(f"💬 Response text: {result.get('text', 'No text')[:200]}...")
            print(f"🖼️  Images returned: {len(result.get('images', []))}")
            print(f"✅ Success: {result.get('success', False)}")
            return True
        else:
            print(f"❌ Backend chat failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Backend chat request failed: {e}")
        return False


def update_backend_config():
    """Update backend configuration for Ollama"""
    print("\n⚙️  Updating backend configuration...")

    # Update the fashion agent to use the correct Ollama endpoint and model
    fashion_agent_path = Path("services/backend/core/fashion_agent.py")

    if fashion_agent_path.exists():
        # Read current content
        with open(fashion_agent_path, "r") as f:
            content = f.read()

        # Update the configuration
        updated_content = content.replace(
            'api_base = os.getenv("OLLAMA_API_BASE", "http://localhost:10010")',
            f'api_base = os.getenv("OLLAMA_API_BASE", "{OLLAMA_BASE_URL}")',
        ).replace(
            'gemma_model_name = os.getenv("GEMMA_MODEL_NAME", "gemma3:4b")',
            f'gemma_model_name = os.getenv("GEMMA_MODEL_NAME", "{MODEL_NAME}")',
        )

        # Write updated content
        with open(fashion_agent_path, "w") as f:
            f.write(updated_content)

        print(f"✅ Updated fashion agent configuration")
        print(f"   - Ollama API Base: {OLLAMA_BASE_URL}")
        print(f"   - Model Name: {MODEL_NAME}")
        return True
    else:
        print(f"❌ Fashion agent file not found at {fashion_agent_path}")
        return False


def main():
    """Main test function"""
    print("🚀 Starting Vibe Fashion Backend Test with Ollama Gemma 3B:12B")
    print("=" * 60)

    # Test results
    results = {}

    # 1. Update configuration
    results["config_update"] = update_backend_config()

    # 2. Test Ollama connection
    results["ollama_connection"] = test_ollama_connection()

    # 3. Test Ollama chat
    results["ollama_chat"] = test_ollama_chat()

    # 4. Test backend health
    results["backend_health"] = test_backend_health()

    # 5. Test backend chat
    results["backend_chat"] = test_backend_chat()

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")

    total_tests = len(results)
    passed_tests = sum(results.values())

    print(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("🎉 All tests passed! Backend is ready to use.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

    return passed_tests == total_tests


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
