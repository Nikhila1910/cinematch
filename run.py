#!/usr/bin/env python3
"""
Run script for CineMatch application
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    app.run(debug=True)