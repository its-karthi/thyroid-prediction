import sys
import os

# Add parent directory to path to import app module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app from the parent directory
from app import app

# Vercel expects the app to be exported as 'app'
# The app is already configured with routes in app.py
__all__ = ['app']
