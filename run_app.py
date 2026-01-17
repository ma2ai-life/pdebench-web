#!/usr/bin/env python
"""
Run the PDEBench app with proper path setup
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now run the Streamlit app
from interfaces.streamlit.app import main

if __name__ == '__main__':
    # This is a placeholder - Streamlit will be run via command line
    print("To run the app, use:")
    print("  streamlit run interfaces/streamlit/app.py")
    print("\nOr use the shortcut:")
    print("  python run_app.py")
