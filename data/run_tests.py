#!/usr/bin/env python3
"""
Quick test runner for Vibe Fashion backend with Ollama
"""

import subprocess
import sys
import time


def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False


def main():
    """Main test runner"""
    print("🚀 Vibe Fashion Backend Test Runner")
    print("=" * 50)

    # Test 1: Run the Python test script
    print("\n📋 Running comprehensive tests...")
    success = run_command("python test_backend_ollama.py", "Backend tests")

    if success:
        print("\n🎉 All tests completed successfully!")
        print("\n💡 Next steps:")
        print(
            "   1. Start the backend server: cd services/backend && python start_server.py"
        )
        print("   2. Run the Jupyter notebook: jupyter notebook test_ollama.ipynb")
        print("   3. Test the API endpoints manually")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure Ollama service is running on Google Cloud")
        print("   2. Check network connectivity")
        print("   3. Verify model availability")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
