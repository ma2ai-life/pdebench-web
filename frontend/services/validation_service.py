"""
Service for parameter validation
"""

class ValidationService:
    @staticmethod
    def validate_physical_parameters(alpha, T):
        """Validate physical parameters"""
        errors = []
        
        if alpha <= 0:
            errors.append("Thermal diffusivity (α) must be positive")
        elif alpha > 1:
            errors.append("Thermal diffusivity (α) is unusually large")
        
        if T <= 0:
            errors.append("Final time (T) must be positive")
        elif T > 100:
            errors.append("Final time (T) is unusually large")
        
        return errors
    
    @staticmethod
    def validate_grid_parameters(nx, nt):
        """Validate grid parameters"""
        errors = []
        
        if nx < 2:
            errors.append("Spatial points must be at least 2")
        elif nx > 10000:
            errors.append("Spatial points too large (max 10000)")
        
        if nt < 2:
            errors.append("Time steps must be at least 2")
        elif nt > 10000:
            errors.append("Time steps too large (max 10000)")
        
        return errors
    
    @staticmethod
    def validate_conditions(ic_type, bc_type):
        """Validate initial and boundary conditions"""
        errors = []
        
        valid_ic_types = ["sinusoidal", "gaussian", "step"]
        if ic_type not in valid_ic_types:
            errors.append(f"Invalid initial condition type. Must be one of: {valid_ic_types}")
        
        valid_bc_types = ["dirichlet", "neumann", "mixed"]
        if bc_type not in valid_bc_types:
            errors.append(f"Invalid boundary condition type. Must be one of: {valid_bc_types}")
        
        return errors
    
    @staticmethod
    def validate_all_parameters(alpha, T, ic_type, bc_type, nx_analytical, nt_analytical, nx_numerical, nt_numerical):
        """Validate all parameters"""
        errors = []
        
        errors.extend(ValidationService.validate_physical_parameters(alpha, T))
        errors.extend(ValidationService.validate_conditions(ic_type, bc_type))
        errors.extend(ValidationService.validate_grid_parameters(nx_analytical, nt_analytical))
        errors.extend(ValidationService.validate_grid_parameters(nx_numerical, nt_numerical))
        
        return errors
