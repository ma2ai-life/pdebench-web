import numpy as np
import time

class FiniteDifferenceSolver:
    @staticmethod
    def solve(alpha=0.01, nx=100, nt=100, T=1.0, ic_type="sinusoidal", bc_type="dirichlet"):
        """Finite Difference solver for Heat Equation using FTCS scheme"""
        start_time = time.time()
        
        dx = 1.0 / (nx - 1)
        dt = T / (nt - 1)
        x = np.linspace(0, 1, nx)
        t = np.linspace(0, T, nt)
        u = np.zeros((nt, nx))
        
        # Initial condition
        if ic_type == "sinusoidal":
            u[0, :] = np.sin(np.pi * x)
        elif ic_type == "gaussian":
            u[0, :] = np.exp(-100 * (x - 0.5)**2)
        elif ic_type == "step":
            u[0, :] = np.where(x < 0.5, 1.0, 0.0)
        
        # FTCS scheme
        r = alpha * dt / (dx**2)
        
        for n in range(nt - 1):
            for i in range(1, nx - 1):
                u[n+1, i] = u[n, i] + r * (u[n, i+1] - 2*u[n, i] + u[n, i-1])
            
            # Boundary conditions
            if bc_type == "dirichlet":
                u[n+1, 0] = 0
                u[n+1, -1] = 0
            elif bc_type == "neumann":
                u[n+1, 0] = u[n+1, 1]
                u[n+1, -1] = u[n+1, -2]
            elif bc_type == "mixed":
                u[n+1, 0] = 0
                u[n+1, -1] = u[n+1, -2]
        
        computation_time = time.time() - start_time
        return u, x, t, computation_time
