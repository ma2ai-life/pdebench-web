import numpy as np

class HeatEquation:
    """1D Heat Equation: u_t = α * u_xx"""
    
    def __init__(self, alpha=0.01, L=1.0):
        self.alpha = alpha  # Thermal diffusivity
        self.L = L          # Domain length [0, L]
    
    def analytical_solution(self, x, t, n_terms=50):
        """
        Analytical solution for:
        u_t = α * u_xx, 0 < x < L, t > 0
        u(0,t) = u(L,t) = 0 (Dirichlet)
        u(x,0) = sin(πx/L) (Initial condition)
        """
        solution = np.zeros_like(x)
        for n in range(1, n_terms + 1):
            λ_n = (n * np.pi / self.L) ** 2
            solution += (2 / (n * np.pi)) * (1 - (-1)**n) * \
                       np.sin(n * np.pi * x / self.L) * \
                       np.exp(-self.alpha * λ_n * t)
        return solution
    
    def initial_condition(self, x, ic_type="sinusoidal"):
        """Different initial conditions"""
        if ic_type == "sinusoidal":
            return np.sin(np.pi * x / self.L)
        elif ic_type == "gaussian":
            return np.exp(-100 * (x - self.L/2)**2)
        elif ic_type == "step":
            return np.where(x < self.L/2, 1.0, 0.0)
        else:
            return np.sin(np.pi * x / self.L)
    
    def boundary_conditions(self, bc_type="dirichlet"):
        """Return boundary condition functions"""
        if bc_type == "dirichlet":
            return {"left": 0.0, "right": 0.0}
        elif bc_type == "neumann":
            return {"left": "zero_flux", "right": "zero_flux"}
        elif bc_type == "mixed":
            return {"left": 0.0, "right": "zero_flux"}
        else:
            return {"left": 0.0, "right": 0.0}