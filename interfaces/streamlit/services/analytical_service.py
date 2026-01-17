"""
Service for analytical solution operations
"""

import numpy as np
import time

class AnalyticalService:
    def __init__(self):
        self.solver = None
        self._load_solver()
    
    def _load_solver(self):
        """Load the analytical solver from backend"""
        try:
            from core.solvers.analytical import AnalyticalSolver
            self.solver = AnalyticalSolver
            self.available = True
        except ImportError:
            self.available = False
            self.solver = self._create_fallback_solver()
    
    def _create_fallback_solver(self):
        """Create a fallback solver if backend not available"""
        class FallbackAnalyticalSolver:
            @staticmethod
            def solve(alpha=0.01, nx=100, nt=100, T=1.0, **kwargs):
                start = time.time()
                x = np.linspace(0, 1, nx)
                t = np.linspace(0, T, nt)
                u = np.zeros((nt, nx))
                for i, time_val in enumerate(t):
                    u[i, :] = np.sin(np.pi * x) * np.exp(-alpha * (np.pi**2) * time_val)
                return u, x, t, time.time() - start
        
        return FallbackAnalyticalSolver
    
    def compute_solution(self, parameters):
        """
        Compute analytical solution with given parameters
        
        Args:
            parameters: dict with keys: alpha, nx, nt, T, ic_type, bc_type
        
        Returns:
            dict with solution data or error
        """
        if not self.available:
            return {
                'success': False,
                'error': 'Analytical solver not available',
                'data': None
            }
        
        try:
            u, x, t, comp_time = self.solver.solve(**parameters)
            
            return {
                'success': True,
                'data': {
                    'u': u,
                    'x': x,
                    't': t,
                    'computation_time': comp_time,
                    'parameters': parameters,
                    'type': 'analytical'
                },
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'data': None
            }
    
    def validate_parameters(self, parameters):
        """Validate analytical solver parameters"""
        errors = []
        
        if 'alpha' not in parameters:
            errors.append("Missing parameter: alpha")
        elif parameters['alpha'] <= 0:
            errors.append("Alpha must be positive")
        
        if 'nx' not in parameters:
            errors.append("Missing parameter: nx")
        elif parameters['nx'] < 2:
            errors.append("nx must be at least 2")
        
        if 'nt' not in parameters:
            errors.append("Missing parameter: nt")
        elif parameters['nt'] < 2:
            errors.append("nt must be at least 2")
        
        if 'T' not in parameters:
            errors.append("Missing parameter: T")
        elif parameters['T'] <= 0:
            errors.append("T must be positive")
        
        return errors
