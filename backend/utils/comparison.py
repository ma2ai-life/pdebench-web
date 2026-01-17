"""
Comparison utilities for handling different grid sizes
"""

import numpy as np

def interpolate_to_common_grid(u1, x1, u2, x2):
    """Interpolate both solutions to a common fine grid"""
    # Create common fine grid (use the finer resolution)
    common_nx = max(len(x1), len(x2))
    common_x = np.linspace(0, 1, common_nx)
    
    # Interpolate both solutions
    u1_interp = np.interp(common_x, x1, u1)
    u2_interp = np.interp(common_x, x2, u2)
    
    return u1_interp, u2_interp, common_x

def compare_solutions(analytical_data, numerical_data):
    """
    Compare analytical and numerical solutions safely
    
    Returns:
        error: array of absolute errors
        common_x: common grid positions
        grids_match: boolean indicating if original grids matched
    """
    if analytical_data is None or numerical_data is None:
        return None, None, None
    
    # Extract data
    u_analytical = analytical_data['u'][-1, :]
    x_analytical = analytical_data['x']
    u_numerical = numerical_data['u'][-1, :]
    x_numerical = numerical_data['x']
    
    # Check if grids match
    grids_match = (len(x_analytical) == len(x_numerical) and 
                   np.allclose(x_analytical, x_numerical))
    
    if grids_match:
        error = np.abs(u_numerical - u_analytical)
        return error, x_analytical, True
    else:
        # Interpolate to common grid
        u_analytical_interp, u_numerical_interp, common_x = interpolate_to_common_grid(
            u_analytical, x_analytical, u_numerical, x_numerical
        )
        error = np.abs(u_numerical_interp - u_analytical_interp)
        return error, common_x, False
