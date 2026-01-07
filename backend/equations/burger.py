import numpy as np

class BurgersEquation:
    """1D Burgers' Equation: u_t + u*u_x = nu*u_xx"""
    
    def __init__(self, nu=0.01):
        self.nu = nu  # viscosity coefficient
        
    def exact_solution(self, x, t):
        """Analytical solution for specific initial conditions"""
        # Simplified exact solution for testing
        return np.exp(-t) * np.sin(np.pi * x)
    
    def initial_condition(self, x):
        """Initial condition: u(x,0) = sin(pi*x)"""
        return np.sin(np.pi * x)
    
    def boundary_conditions(self):
        """Dirichlet BC: u(0,t)=0, u(1,t)=0"""
        return {"left": 0.0, "right": 0.0}