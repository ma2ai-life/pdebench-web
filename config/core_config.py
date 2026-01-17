"""
Core configuration for PDEBench
"""

# Available equations
EQUATIONS = {
    'heat': {
        'name': 'Heat Equation',
        'module': 'core.equations.heat_equation',
        'class': 'HeatEquation',
        'icon': '🔥',
        'description': 'u_t = α u_xx',
        'parameters': ['alpha', 'T', 'L'],
        'supported_solvers': ['analytical', 'finite_difference', 'rom']
    }
    # More equations will be added here
}

# Available solvers
SOLVERS = {
    'analytical': {
        'name': 'Analytical',
        'module': 'core.solvers.analytical',
        'class': 'AnalyticalSolver',
        'description': 'Exact solution (when available)'
    },
    'finite_difference': {
        'name': 'Finite Difference',
        'module': 'core.solvers.finite_difference',
        'class': 'FiniteDifferenceSolver',
        'description': 'Traditional numerical method'
    }
    # ROM, PINNs, etc. will be added here
}

# Default parameters
DEFAULT_PARAMETERS = {
    'heat': {
        'alpha': 0.01,
        'T': 1.0,
        'L': 1.0,
        'nx': 100,
        'nt': 100,
        'ic_type': 'sinusoidal',
        'bc_type': 'dirichlet'
    }
}
