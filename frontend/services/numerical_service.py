"""
Service for numerical solution operations
"""

import numpy as np
import time

class NumericalService:
    def __init__(self):
        self.solver = None
        self._load_solver()
    
    def _load_solver(self):
        """Load the numerical solver from backend"""
        try:
            from backend.solvers.finite_difference import FiniteDifferenceSolver
            self.solver = FiniteDifferenceSolver
            self.available = True
        except ImportError:
            self.available = False
            self.solver = self._create_fallback_solver()
    
    def _create_fallback_solver(self):
        """Create a fallback solver if backend not available"""
        class FallbackNumericalSolver:
            @staticmethod
            def solve(alpha=0.01, nx=100, nt=100, T=1.0, **kwargs):
                start = time.time()
                dx = 1.0 / (nx - 1)
                dt = T / (nt - 1)
                x = np.linspace(0, 1, nx)
                t = np.linspace(0, T, nt)
                u = np.zeros((nt, nx))
                u[0, :] = np.sin(np.pi * x)
                r = alpha * dt / (dx**2)
                
                for n in range(nt - 1):
                    for i in range(1, nx - 1):
                        u[n+1, i] = u[n, i] + r * (u[n, i+1] - 2*u[n, i] + u[n, i-1])
                    u[n+1, 0] = 0
                    u[n+1, -1] = 0
                
                return u, x, t, time.time() - start
        
        return FallbackNumericalSolver
    
    def compute_solution(self, parameters):
        """
        Compute numerical solution with given parameters
        
        Args:
            parameters: dict with keys: alpha, nx, nt, T, ic_type, bc_type
        
        Returns:
            dict with solution data or error
        """
        if not self.available:
            return {
                'success': False,
                'error': 'Numerical solver not available',
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
                    'type': 'numerical'
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
        """Validate numerical solver parameters"""
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
        
        # Check CFL condition for stability
        if all(k in parameters for k in ['alpha', 'nx', 'nt', 'T']):
            dx = 1.0 / (parameters['nx'] - 1)
            dt = parameters['T'] / (parameters['nt'] - 1)
            cfl = parameters['alpha'] * dt / (dx**2)
            if cfl > 0.5:
                errors.append(f"CFL condition violated: {cfl:.3f} > 0.5 (may be unstable)")
        
        return errors
