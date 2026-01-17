import numpy as np

class AnalyticalSolver:
    @staticmethod
    def solve(alpha=0.01, nx=100, nt=100, T=1.0, ic_type="sinusoidal", bc_type="dirichlet"):
        """Simple analytical solution for Heat Equation: u(x,t) = sin(πx) * exp(-απ²t)"""
        x = np.linspace(0, 1, nx)
        t = np.linspace(0, T, nt)
        u = np.zeros((nt, nx))
        
        for i, time in enumerate(t):
            u[i, :] = np.sin(np.pi * x) * np.exp(-alpha * (np.pi**2) * time)
        
        return u, x, t
