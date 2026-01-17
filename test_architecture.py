#!/usr/bin/env python
"""Test the new Controller-Service-View architecture"""

import sys
import os

print("Testing PDEBench Controller-Service-View Architecture...\n")

# Test Service Layer
try:
    from frontend.services.analytical_service import AnalyticalService
    print("✅ frontend.services.analytical_service")
    
    from frontend.services.numerical_service import NumericalService
    print("✅ frontend.services.numerical_service")
    
    from frontend.services.validation_service import ValidationService
    print("✅ frontend.services.validation_service")
    
    # Test Controller Layer
    from frontend.controllers.simulation_controller import SimulationController
    print("✅ frontend.controllers.simulation_controller")
    
    from frontend.controllers.comparison_controller import ComparisonController
    print("✅ frontend.controllers.comparison_controller")
    
    # Test View Layer
    from frontend.views.solution_view import SolutionView
    print("✅ frontend.views.solution_view")
    
    from frontend.views.comparison_view import ComparisonView
    print("✅ frontend.views.comparison_view")
    
    from frontend.views.dashboard_view import DashboardView
    print("✅ frontend.views.dashboard_view")
    
    print("\n🎉 All architecture layers imported successfully!")
    
    # Test service instantiation
    print("\nTesting service instantiation...")
    analytical_service = AnalyticalService()
    print(f"✅ AnalyticalService: available={analytical_service.available}")
    
    numerical_service = NumericalService()
    print(f"✅ NumericalService: available={numerical_service.available}")
    
    # Test controller instantiation
    simulation_controller = SimulationController()
    print("✅ SimulationController instantiated")
    
    comparison_controller = ComparisonController()
    print("✅ ComparisonController instantiated")
    
    print("\n🎉 Architecture test PASSED!")
    
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    
    # Check directory structure
    print("\nChecking directory structure...")
    layers = ['services', 'controllers', 'views']
    
    for layer in layers:
        dir_path = f"frontend/{layer}"
        if os.path.exists(dir_path):
            # List files in directory
            files = [f for f in os.listdir(dir_path) if f.endswith('.py') and f != '__init__.py']
            if files:
                print(f"✅ {dir_path}/ contains: {', '.join(files)}")
            else:
                print(f"❌ {dir_path}/ is empty")
        else:
            print(f"❌ {dir_path}/ missing")
    
    sys.exit(1)

print("\n✅ Architecture is ready!")
