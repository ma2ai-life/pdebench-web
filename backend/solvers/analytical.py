import numpy as np
from backend.equations.heat_equation import HeatEquation

class AnalyticalSolver:
    """Solve Heat Equation analytically"""
    
    @staticmethod
    def solve(alpha=0.01, nx=100, nt=100, T=1.0, 
              ic_type="sinusoidal", bc_type="dirichlet"):
        """
        Solve 1D Heat equation analytically
        Returns: u, x, t
        """
        # Create equation
        equation = HeatEquation(alpha=alpha)
        
        # Spatial and temporal grids
        x = np.linspace(0, equation.L, nx)
        t = np.linspace(0, T, nt)
        
        # Initialize solution array
        u = np.zeros((nt, nx))
        
        # Fill solution at each time step
        for i, time in enumerate(t):
            u[i, :] = equation.analytical_solution(x, time)
        
        return u, x, t
    
    @staticmethod
    def get_solution_details():
        """Return mathematical form of analytical solution"""
        return {
            "equation": r"u_t = \alpha u_{xx}",
            "domain": r"0 < x < L, t > 0",
            "boundary_conditions": r"u(0,t) = u(L,t) = 0",
            "initial_condition": r"u(x,0) = \sin(\pi x / L)",
            "analytical_solution": r"u(x,t) = \sum_{n=1}^{\infty} \frac{2}{n\pi}(1 - (-1)^n) \sin\left(\frac{n\pi x}{L}\right) e^{-\alpha (n\pi/L)^2 t}"
        }