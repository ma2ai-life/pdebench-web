import numpy as np
import time

class AnalyticalSolver:
    @staticmethod
    def solve(alpha=0.01, nx=100, nt=100, T=1.0, ic_type="sinusoidal", bc_type="dirichlet"):
        """
        Simple analytical solution for Heat Equation: u(x,t) = sin(πx) * exp(-απ²t)
        Returns: u, x, t, computation_time
        """
        start_time = time.time()
        
        x = np.linspace(0, 1, nx)
        t = np.linspace(0, T, nt)
        u = np.zeros((nt, nx))
        
        # Choose initial condition
        if ic_type == "sinusoidal":
            initial = np.sin(np.pi * x)
        elif ic_type == "gaussian":
            initial = np.exp(-100 * (x - 0.5)**2)
        elif ic_type == "step":
            initial = np.where(x < 0.5, 1.0, 0.0)
        else:
            initial = np.sin(np.pi * x)
        
        # Analytical solution for each time step
        for i, time_val in enumerate(t):
            if ic_type == "sinusoidal":
                # Exact solution for sin(πx) initial condition
                u[i, :] = initial * np.exp(-alpha * (np.pi**2) * time_val)
            else:
                # Approximate for other ICs (simplified)
                u[i, :] = initial * np.exp(-alpha * (np.pi**2) * time_val)
        
        computation_time = time.time() - start_time
        
        return u, x, t, computation_time
    
    @staticmethod
    def get_solution_info():
        """Return information about the analytical solution"""
        return {
            "method": "Analytical (Separation of Variables)",
            "solution": r"u(x,t) = \sin(\pi x) e^{-\alpha \pi^2 t}",
            "assumptions": "Dirichlet BC, sinusoidal initial condition",
            "accuracy": "Exact (within machine precision)"
        }
