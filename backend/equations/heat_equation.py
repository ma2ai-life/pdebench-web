import numpy as np

class HeatEquation:
    """1D Heat Equation: u_t = α * u_xx"""
    
    def __init__(self, alpha=0.01, L=1.0):
        self.alpha = alpha  # Thermal diffusivity
        self.L = L          # Domain length [0, L]
    
    def analytical_solution_dirichlet(self, x, t, n_terms=20):
        """
        Analytical solution for Dirichlet BC:
        u(0,t) = u(L,t) = 0
        u(x,0) = sin(πx/L)
        """
        solution = np.zeros_like(x)
        for n in range(1, n_terms + 1):
            λ_n = (n * np.pi / self.L) ** 2
            # Fourier coefficient for sin(πx/L) initial condition
            if n == 1:
                B_n = 1.0
            else:
                B_n = 0.0
            solution += B_n * np.sin(n * np.pi * x / self.L) * np.exp(-self.alpha * λ_n * t)
        return solution
    
    def analytical_solution_general(self, x, t, initial_func, n_terms=50):
        """
        General analytical solution for arbitrary initial condition
        u(x,0) = initial_func(x)
        """
        solution = np.zeros_like(x)
        for n in range(1, n_terms + 1):
            λ_n = (n * np.pi / self.L) ** 2
            # Compute Fourier coefficient B_n
            B_n = (2/self.L) * np.trapz(
                initial_func(x) * np.sin(n * np.pi * x / self.L), x
            )
            solution += B_n * np.sin(n * np.pi * x / self.L) * np.exp(-self.alpha * λ_n * t)
        return solution
    
    def get_equation_details(self):
        """Return mathematical details of the equation"""
        return {
            "pde": r"\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}",
            "description": "1D Heat/Diffusion Equation",
            "parameters": {
                "α": "thermal diffusivity",
                "u(x,t)": "temperature distribution"
            },
            "common_ics": {
                "sinusoidal": r"u(x,0) = \sin(\pi x / L)",
                "gaussian": r"u(x,0) = e^{-100(x - L/2)^2}",
                "step": r"u(x,0) = \begin{cases} 1 & x < L/2 \\ 0 & x \geq L/2 \end{cases}"
            },
            "common_bcs": {
                "dirichlet": r"u(0,t) = u(L,t) = 0",
                "neumann": r"\frac{\partial u}{\partial x}(0,t) = \frac{\partial u}{\partial x}(L,t) = 0",
                "mixed": r"u(0,t) = 0, \frac{\partial u}{\partial x}(L,t) = 0"
            }
        }
