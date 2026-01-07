# frontend/solver_bridge.py
import sys
import os
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try to import from backend
    from backend.solvers.traditional.finite_difference import FiniteDifferenceSolver
    print("✅ Imported solver from backend")
except ImportError:
    # Fallback to inline implementation
    print("⚠️ Using inline solver as fallback")
    
    class FiniteDifferenceSolver:
        @staticmethod
        def solve_burgers(nu=0.01, nx=100, nt=100, T=1.0):
            dx = 1.0 / (nx - 1)
            dt = T / (nt - 1)
            x = np.linspace(0, 1, nx)
            t = np.linspace(0, T, nt)
            u = np.zeros((nt, nx))
            u[0, :] = np.sin(np.pi * x)
            
            for n in range(nt - 1):
                for i in range(1, nx - 1):
                    u_x = (u[n, i+1] - u[n, i-1]) / (2 * dx)
                    u_xx = (u[n, i+1] - 2*u[n, i] + u[n, i-1]) / (dx**2)
                    u[n+1, i] = u[n, i] - dt * u[n, i] * u_x + nu * dt * u_xx
                u[n+1, 0] = 0
                u[n+1, -1] = 0
            
            return u, x, t
        
        @staticmethod
        def solve_heat(alpha=0.01, nx=100, nt=100, T=1.0):
            dx = 1.0 / (nx - 1)
            dt = T / (nt - 1)
            x = np.linspace(0, 1, nx)
            t = np.linspace(0, T, nt)
            u = np.zeros((nt, nx))
            u[0, :] = np.exp(-100 * (x - 0.5)**2)
            r = alpha * dt / (dx**2)
            
            for n in range(nt - 1):
                for i in range(1, nx - 1):
                    u[n+1, i] = u[n, i] + r * (u[n, i+1] - 2*u[n, i] + u[n, i-1])
                u[n+1, 0] = u[n+1, 1]
                u[n+1, -1] = u[n+1, -2]
            
            return u, x, t