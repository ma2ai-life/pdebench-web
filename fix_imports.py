#!/usr/bin/env python
"""
Fix import paths in all Python files after migration
"""

import os
import re

def fix_imports_in_file(filepath):
    """Fix import paths in a single file"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Fix relative imports
    patterns = [
        # Fix frontend imports
        (r'from frontend\.', 'from interfaces.streamlit.'),
        (r'from frontend import', 'from interfaces.streamlit import'),
        
        # Fix backend imports  
        (r'from backend\.', 'from core.'),
        (r'from backend import', 'from core import'),
        
        # Fix specific module imports
        (r'from layout\.', 'from interfaces.streamlit.layout.'),
        (r'from components\.', 'from interfaces.streamlit.components.'),
        (r'from styles\.', 'from interfaces.streamlit.styles.'),
        (r'from state\.', 'from interfaces.streamlit.state.'),
        (r'from controllers\.', 'from interfaces.streamlit.controllers.'),
        (r'from services\.', 'from interfaces.streamlit.services.'),
        (r'from views\.', 'from interfaces.streamlit.views.'),
        
        # Fix equations imports
        (r'from equations\.', 'from core.equations.'),
        (r'from solvers\.', 'from core.solvers.'),
        (r'from utils\.', 'from core.solvers.'),  # utils moved to solvers
    ]
    
    original_content = content
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    print("Fixing import paths in all Python files...")
    
    # Directories to process
    directories = [
        'interfaces/streamlit',
        'core'
    ]
    
    fixed_count = 0
    for directory in directories:
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.py'):
                        filepath = os.path.join(root, file)
                        if fix_imports_in_file(filepath):
                            print(f"✅ Fixed: {filepath}")
                            fixed_count += 1
    
    print(f"\n✅ Fixed imports in {fixed_count} files")
    
    # Create __init__.py files if missing
    print("\nEnsuring all __init__.py files exist...")
    
    required_dirs = [
        'interfaces',
        'interfaces/streamlit', 
        'interfaces/streamlit/layout',
        'interfaces/streamlit/components',
        'interfaces/streamlit/styles',
        'interfaces/streamlit/state',
        'interfaces/streamlit/controllers',
        'interfaces/streamlit/services',
        'interfaces/streamlit/views',
        'core',
        'core/equations',
        'core/solvers'
    ]
    
    for dir_path in required_dirs:
        init_file = os.path.join(dir_path, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# Auto-generated __init__.py\n')
            print(f"✅ Created: {init_file}")

if __name__ == '__main__':
    main()
