#!/usr/bin/env python3
"""
Loteca X-Ray - Main Application Entry Point
Railway deployment entry point
"""

import sys
import os

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

# Change to backend directory
os.chdir(backend_path)

# Import and run the main Flask app
try:
    from app import app
    
    if __name__ == '__main__':
        # Railway sets PORT environment variable
        port = int(os.environ.get('PORT', 5000))
        print(f"Starting Loteca X-Ray on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Backend path: {backend_path}")
    print(f"Files in backend: {os.listdir(backend_path) if os.path.exists(backend_path) else 'Not found'}")
    sys.exit(1)
