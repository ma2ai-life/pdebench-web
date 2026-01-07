import numpy as np

class FiniteDifferenceSolver:
    """Simple explicit finite difference solver for Burgers' equation"""
    
    def solve(self, equation, nx=100, nt=100, T=1.0):
        """
        Solve using FTCS scheme
        equation: BurgersEquation instance
        nx: number of spatial points
        nt: number of time steps
        T: final time
        """
        dx = 1.0 / (nx - 1)
        dt = T / (nt - 1)
        
        # Grid
        x = np.linspace(0, 1, nx)
        t = np.linspace(0, T, nt)
        
        # Initialize solution
        u = np.zeros((nt, nx))
        u[0, :] = equation.initial_condition(x)
        
        # Time stepping
        for n in range(0, nt-1):
            for i in range(1, nx-1):
                # FTCS scheme for Burgers
                u_xx = (u[n, i+1] - 2*u[n, i] + u[n, i-1]) / (dx**2)
                u_x = (u[n, i+1] - u[n, i-1]) / (2*dx)
                
                u[n+1, i] = u[n, i] - dt * u[n, i] * u_x + equation.nu * dt * u_xx
            
            # Boundary conditions
            u[n+1, 0] = equation.boundary_conditions()["left"]
            u[n+1, -1] = equation.boundary_conditions()["right"]
        
        return {
            "solution": u,
            "x": x,
            "t": t,
            "dx": dx,
            "dt": dt
        }