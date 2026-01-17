"""
Controller for managing simulations
"""

import streamlit as st
from frontend.services.analytical_service import AnalyticalService
from frontend.services.numerical_service import NumericalService
from frontend.services.validation_service import ValidationService
from frontend.state.session import (
    store_analytical_solution, store_numerical_solution,
    get_solution_data
)

class SimulationController:
    def __init__(self):
        self.analytical_service = AnalyticalService()
        self.numerical_service = NumericalService()
        self.validation_service = ValidationService()
    
    def run_analytical_simulation(self, sidebar_data):
        """Run analytical simulation with validation"""
        # Validate parameters
        errors = self.validation_service.validate_all_parameters(
            sidebar_data['alpha'], sidebar_data['T'],
            sidebar_data['ic_type'], sidebar_data['bc_type'],
            sidebar_data['nx_analytical'], sidebar_data['nt_analytical'],
            sidebar_data['nx_numerical'], sidebar_data['nt_numerical']
        )
        
        if errors:
            for error in errors:
                st.error(f"Validation Error: {error}")
            return
        
        # Prepare parameters
        params = {
            'alpha': sidebar_data['alpha'],
            'T': sidebar_data['T'],
            'ic_type': sidebar_data['ic_type'],
            'bc_type': sidebar_data['bc_type'],
            'nx': sidebar_data['nx_analytical'],
            'nt': sidebar_data['nt_analytical']
        }
        
        # Run simulation
        result = self.analytical_service.compute_solution(params)
        
        if result['success']:
            # Store in session state
            data = result['data']
            store_analytical_solution(
                data['u'], data['x'], data['t'],
                data['computation_time'], data['parameters']
            )
            st.success(f"✅ Analytical solution computed in {data['computation_time']:.6f}s")
        else:
            st.error(f"❌ Analytical simulation failed: {result['error']}")
    
    def run_numerical_simulation(self, sidebar_data):
        """Run numerical simulation with validation"""
        # Validate parameters
        errors = self.validation_service.validate_all_parameters(
            sidebar_data['alpha'], sidebar_data['T'],
            sidebar_data['ic_type'], sidebar_data['bc_type'],
            sidebar_data['nx_analytical'], sidebar_data['nt_analytical'],
            sidebar_data['nx_numerical'], sidebar_data['nt_numerical']
        )
        
        if errors:
            for error in errors:
                st.error(f"Validation Error: {error}")
            return
        
        # Prepare parameters
        params = {
            'alpha': sidebar_data['alpha'],
            'T': sidebar_data['T'],
            'ic_type': sidebar_data['ic_type'],
            'bc_type': sidebar_data['bc_type'],
            'nx': sidebar_data['nx_numerical'],
            'nt': sidebar_data['nt_numerical']
        }
        
        # Additional numerical validation
        numerical_errors = self.numerical_service.validate_parameters(params)
        if numerical_errors:
            for error in numerical_errors:
                st.warning(f"Numerical Warning: {error}")
        
        # Run simulation
        result = self.numerical_service.compute_solution(params)
        
        if result['success']:
            # Store in session state
            data = result['data']
            store_numerical_solution(
                data['u'], data['x'], data['t'],
                data['computation_time'], data['parameters']
            )
            st.success(f"✅ Numerical solution computed in {data['computation_time']:.6f}s")
        else:
            st.error(f"❌ Numerical simulation failed: {result['error']}")
    
    def get_simulation_status(self):
        """Get current simulation status"""
        analytical_data = get_solution_data('analytical')
        numerical_data = get_solution_data('numerical')
        
        status = {
            'analytical_available': analytical_data is not None,
            'numerical_available': numerical_data is not None,
            'both_available': analytical_data is not None and numerical_data is not None
        }
        
        return status
