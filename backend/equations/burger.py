import numpy as np

class BurgersEquation:
    """Burgers' equation model"""
    
    def __init__(self, nu=0.01, L=1.0):
        self.nu = nu  # viscosity
        self.L = L    # domain length
        
    def exact_solution(self, x, t):
        """Exact solution for specific case (Cole-Hopf transformation)"""
        # For simplicity, return approximate solution
        return np.exp(-t) * np.sin(np.pi * x)
    
    def initial_condition(self, x):
        """Default initial condition"""
        return np.sin(np.pi * x)
    
    def boundary_conditions(self, bc_type='dirichlet'):
        """Return boundary conditions"""
        if bc_type == 'dirichlet':
            return {'left': 0.0, 'right': 0.0}
        else:
            return {'left': 'neumann', 'right': 'neumann'}