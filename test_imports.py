#!/usr/bin/env python
"""Test that all imports work correctly"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    from backend.equations.heat_equation import HeatEquation
    print("✅ HeatEquation imported successfully")
    
    from backend.solvers.analytical import AnalyticalSolver
    print("✅ AnalyticalSolver imported successfully")
    
    from backend.solvers.finite_difference import FiniteDifferenceSolver
    print("✅ FiniteDifferenceSolver imported successfully")
    
    # Test instantiation
    eq = HeatEquation(alpha=0.01)
    print(f"✅ HeatEquation instantiated: α={eq.alpha}")
    
    # Test analytical solver
    u, x, t = AnalyticalSolver.solve(alpha=0.01, nx=10, nt=5, T=1.0)
    print(f"✅ AnalyticalSolver works: u.shape={u.shape}")
    
    # Test finite difference solver
    u, x, t, time = FiniteDifferenceSolver.solve(alpha=0.01, nx=10, nt=5, T=1.0)
    print(f"✅ FiniteDifferenceSolver works: computed in {time:.4f}s")
    
    print("\n🎉 All imports and basic functionality work!")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
