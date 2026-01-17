#!/usr/bin/env python
"""
Final test of all imports
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("Testing all critical imports...\n")

# Test 1: Core imports
print("1. Testing core imports:")
try:
    from core.equations.heat_equation import HeatEquation
    print("   ✅ core.equations.heat_equation")
except ImportError as e:
    print(f"   ❌ core.equations.heat_equation: {e}")

try:
    from core.solvers.analytical import AnalyticalSolver
    print("   ✅ core.solvers.analytical")
except ImportError as e:
    print(f"   ❌ core.solvers.analytical: {e}")

try:
    from core.solvers.finite_difference import FiniteDifferenceSolver
    print("   ✅ core.solvers.finite_difference")
except ImportError as e:
    print(f"   ❌ core.solvers.finite_difference: {e}")

try:
    from core.solvers.comparison import compare_solutions
    print("   ✅ core.solvers.comparison")
except ImportError as e:
    print(f"   ❌ core.solvers.comparison: {e}")

# Test 2: Streamlit imports
print("\n2. Testing streamlit imports:")
try:
    from interfaces.streamlit.controllers.simulation_controller import SimulationController
    print("   ✅ interfaces.streamlit.controllers.simulation_controller")
except ImportError as e:
    print(f"   ❌ interfaces.streamlit.controllers.simulation_controller: {e}")

try:
    from interfaces.streamlit.controllers.comparison_controller import ComparisonController
    print("   ✅ interfaces.streamlit.controllers.comparison_controller")
except ImportError as e:
    print(f"   ❌ interfaces.streamlit.controllers.comparison_controller: {e}")

try:
    from interfaces.streamlit.views.dashboard_view import DashboardView
    print("   ✅ interfaces.streamlit.views.dashboard_view")
except ImportError as e:
    print(f"   ❌ interfaces.streamlit.views.dashboard_view: {e}")

# Test 3: Instantiate controllers
print("\n3. Testing controller instantiation:")
try:
    simulation_controller = SimulationController()
    print("   ✅ SimulationController instantiated")
    
    # Check if services are available
    print(f"   ✅ Analytical service: {simulation_controller.analytical_service.available}")
    print(f"   ✅ Numerical service: {simulation_controller.numerical_service.available}")
except Exception as e:
    print(f"   ❌ Controller instantiation failed: {e}")

print("\n✅ All tests completed!")
print("\nTo run the app:")
print("  python -m streamlit run interfaces/streamlit/app.py")
