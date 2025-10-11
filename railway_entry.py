#!/usr/bin/env python3
"""
Loteca X-Ray - Main Application Entry Point
Railway deployment entry point - Baseado na experiência do loteriasinteligente.com.br
"""

import sys
import os
import logging
import traceback

# Configurar logging como na experiência anterior
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

# Change to backend directory
os.chdir(backend_path)

# Import and run the main Flask app
try:
    from app import create_app
    
    app = create_app()
    
    # Configurações para Railway (baseado na experiência anterior)
    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        logger.info(f"Starting Loteca X-Ray on port {port}")
        app.run(host="0.0.0.0", port=port, debug=False)
        
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    logger.error(f"Current directory: {os.getcwd()}")
    logger.error(f"Backend path: {backend_path}")
    logger.error(f"Files in backend: {os.listdir(backend_path) if os.path.exists(backend_path) else 'Not found'}")
    sys.exit(1)
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)

