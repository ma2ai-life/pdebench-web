"""
Main Streamlit app - Ultra minimal entry point
Uses Controller-Service-View architecture
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import layout
from frontend.layout.page_config import setup_page
from frontend.layout.header import display_header, display_import_status
from frontend.layout.sidebar import create_sidebar

# Import styles
from frontend.styles.theme import apply_css

# Import controllers
from frontend.controllers.simulation_controller import SimulationController
from frontend.controllers.comparison_controller import ComparisonController

# Import views
from frontend.views.dashboard_view import DashboardView

# Import state
from frontend.state.session import (
    initialize_session_state,
    clear_analytical, clear_numerical, clear_all
)

# ==================== SETUP ====================
# Page configuration
setup_page()

# Apply CSS styles
apply_css()

# Initialize session state
initialize_session_state()

# ==================== INITIALIZE CONTROLLERS ====================
simulation_controller = SimulationController()
comparison_controller = ComparisonController()

# ==================== HEADER ====================
display_header()

# Check if solvers are available
if simulation_controller.analytical_service.available and simulation_controller.numerical_service.available:
    display_import_status("✅ All services initialized successfully")
else:
    display_import_status("⚠️ Some services using fallback implementations")

# ==================== SIDEBAR ====================
sidebar_data = create_sidebar()

# Handle clear buttons
if sidebar_data['clear_analytical']:
    clear_analytical()
    st.rerun()

if sidebar_data['clear_numerical']:
    clear_numerical()
    st.rerun()

if sidebar_data['clear_all']:
    clear_all()
    st.rerun()

# ==================== HANDLE SIMULATIONS ====================
# Run Analytical Simulation
if sidebar_data['run_analytical']:
    simulation_controller.run_analytical_simulation(sidebar_data)

# Run Numerical Simulation
if sidebar_data['run_numerical']:
    simulation_controller.run_numerical_simulation(sidebar_data)

# ==================== DISPLAY DASHBOARD ====================
# Equation details
st.markdown("## 📐 Heat Equation")
with st.expander("Show equation details", expanded=True):
    st.latex(r"\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}")
    st.markdown("""
    **Description:** Models heat conduction and diffusion processes
    
    **Parameters:**
    - $u(x,t)$: Temperature distribution
    - $\\alpha$: Thermal diffusivity
    - Domain: $x \\in [0, 1], t \\in [0, T]$
    """)

# Display solutions dashboard
DashboardView.display_solutions_dashboard()

# Display comparison dashboard
DashboardView.display_comparison_dashboard(comparison_controller)

# Display 3D visualization
DashboardView.display_3d_visualization()

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("**PDEBench v3.0** | Controller-Service-View Architecture | Ready for ROM & PINNs")
