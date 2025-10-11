#!/usr/bin/env python3
"""
Startup script for the Vibe Fashion API server
"""

import uvicorn
from settings import API_HOST, API_PORT, DEBUG

if __name__ == "__main__":
    print("Starting Vibe Fashion API server...")
    print(f"Host: {API_HOST}")
    print(f"Port: {API_PORT}")
    print(f"Debug: {DEBUG}")
    print("=" * 50)

    uvicorn.run(
        "api:app",
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG,
        log_level="info" if not DEBUG else "debug",
    )
