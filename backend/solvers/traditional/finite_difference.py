import numpy as np

class FiniteDifferenceSolver:
    """Finite Difference solver for demonstration"""
    
    @staticmethod
    def solve_burgers(nu=0.01, nx=100, nt=100, T=1.0):
        """Solve 1D Burgers equation using explicit finite difference"""
        dx = 1.0 / (nx - 1)
        dt = T / (nt - 1)
        
        # Grid
        x = np.linspace(0, 1, nx)
        t = np.linspace(0, T, nt)
        
        # Initialize solution
        u = np.zeros((nt, nx))
        u[0, :] = np.sin(np.pi * x)  # Initial condition
        
        # Time stepping
        for n in range(nt - 1):
            # Interior points
            for i in range(1, nx - 1):
                u_x = (u[n, i+1] - u[n, i-1]) / (2 * dx)
                u_xx = (u[n, i+1] - 2*u[n, i] + u[n, i-1]) / (dx**2)
                u[n+1, i] = u[n, i] - dt * u[n, i] * u_x + nu * dt * u_xx
            
            # Boundary conditions (Dirichlet)
            u[n+1, 0] = 0
            u[n+1, -1] = 0
        
        return u, x, t
    
    @staticmethod
    def solve_heat(alpha=0.01, nx=100, nt=100, T=1.0):
        """Solve 1D Heat equation: u_t = alpha * u_xx"""
        dx = 1.0 / (nx - 1)
        dt = T / (nt - 1)
        
        x = np.linspace(0, 1, nx)
        t = np.linspace(0, T, nt)
        u = np.zeros((nt, nx))
        
        # Initial condition: Gaussian
        u[0, :] = np.exp(-100 * (x - 0.5)**2)
        
        # FTCS scheme
        r = alpha * dt / (dx**2)
        
        for n in range(nt - 1):
            for i in range(1, nx - 1):
                u[n+1, i] = u[n, i] + r * (u[n, i+1] - 2*u[n, i] + u[n, i-1])
            
            # Neumann boundary: du/dx = 0 at boundaries
            u[n+1, 0] = u[n+1, 1]
            u[n+1, -1] = u[n+1, -2]
        
        return u, x, t