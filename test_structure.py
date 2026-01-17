#!/usr/bin/env python
"""Test the modular structure"""

import sys
import os

print("Testing PDEBench modular structure...\n")

# Test imports
try:
    from frontend.layout.page_config import setup_page
    print("✅ frontend.layout.page_config")
    
    from frontend.layout.header import display_header
    print("✅ frontend.layout.header")
    
    from frontend.layout.sidebar import create_sidebar
    print("✅ frontend.layout.sidebar")
    
    from frontend.styles.theme import apply_css
    print("✅ frontend.styles.theme")
    
    from frontend.components.plots import create_2d_plot
    print("✅ frontend.components.plots")
    
    from frontend.components.metrics import calculate_solution_metrics
    print("✅ frontend.components.metrics")
    
    from frontend.state.session import initialize_session_state
    print("✅ frontend.state.session")
    
    from backend.utils.comparison import compare_solutions
    print("✅ backend.utils.comparison")
    
    print("\n🎉 All modular imports successful!")
    
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nChecking directory structure...")
    
    # Check if directories exist
    dirs_to_check = [
        'frontend/layout',
        'frontend/styles', 
        'frontend/components',
        'frontend/state',
        'backend/utils'
    ]
    
    for dir_path in dirs_to_check:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/ exists")
        else:
            print(f"❌ {dir_path}/ missing")
    
    sys.exit(1)
