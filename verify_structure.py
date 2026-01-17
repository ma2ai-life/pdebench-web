#!/usr/bin/env python
"""
Verify the new structure is working
"""

import sys
import os

print("Verifying PDEBench structure...\n")

# Check project root
project_root = os.path.dirname(os.path.abspath(__file__))
print(f"Project root: {project_root}")

# Add to path
sys.path.insert(0, project_root)

# Test imports
try:
    print("\n1. Testing core imports...")
    from core.equations.heat_equation import HeatEquation
    print("   ✅ core.equations.heat_equation")
    
    from core.solvers.analytical import AnalyticalSolver
    print("   ✅ core.solvers.analytical")
    
    from core.solvers.finite_difference import FiniteDifferenceSolver
    print("   ✅ core.solvers.finite_difference")
    
    print("\n2. Testing streamlit imports...")
    from interfaces.streamlit.layout.page_config import setup_page
    print("   ✅ interfaces.streamlit.layout.page_config")
    
    from interfaces.streamlit.controllers.simulation_controller import SimulationController
    print("   ✅ interfaces.streamlit.controllers.simulation_controller")
    
    from interfaces.streamlit.views.dashboard_view import DashboardView
    print("   ✅ interfaces.streamlit.views.dashboard_view")
    
    print("\n3. Testing instantiation...")
    simulation_controller = SimulationController()
    print("   ✅ SimulationController instantiated")
    
    print("\n🎉 All imports successful! Structure is correct.")
    
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nCurrent Python path:")
    for p in sys.path:
        print(f"  {p}")
    
    print("\nChecking directory structure...")
    if not os.path.exists('interfaces'):
        print("❌ 'interfaces' directory missing")
    if not os.path.exists('core'):
        print("❌ 'core' directory missing")
    
    sys.exit(1)

print("\n✅ Structure verification PASSED!")
print("\nTo run the app:")
print("  cd interfaces/streamlit && streamlit run app.py")
print("\nOr from project root:")
print("  python -m streamlit run interfaces/streamlit/app.py")
