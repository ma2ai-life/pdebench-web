"""
Sidebar configuration and controls
"""

import streamlit as st

def create_sidebar():
    """Create the sidebar with all controls"""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Physical Parameters
        st.subheader("Physical Parameters")
        alpha = st.slider(
            "Thermal Diffusivity (α)",
            0.001, 0.1, 0.01, 0.001,
            help="Controls how fast heat spreads"
        )
        
        T = st.slider(
            "Final Time (T)",
            0.1, 5.0, 1.0, 0.1,
            help="Simulation end time"
        )
        
        # Conditions
        st.subheader("Conditions")
        ic_type = st.selectbox(
            "Initial Condition",
            ["sinusoidal", "gaussian", "step"],
            help="Initial temperature distribution"
        )
        
        bc_type = st.selectbox(
            "Boundary Condition",
            ["dirichlet", "neumann", "mixed"],
            help="Boundary conditions"
        )
        
        # Grid Parameters
        st.subheader("Grid Parameters")
        
        st.markdown("**Analytical Grid:**")
        col1, col2 = st.columns(2)
        with col1:
            nx_analytical = st.slider("A-Spatial", 20, 200, 50, 10,
                                    help="Grid points for analytical", key="nx_a")
        with col2:
            nt_analytical = st.slider("A-Time", 20, 200, 50, 10,
                                    help="Time steps for analytical", key="nt_a")
        
        st.markdown("**Numerical Grid:**")
        col1, col2 = st.columns(2)
        with col1:
            nx_numerical = st.slider("N-Spatial", 20, 200, 50, 10,
                                   help="Grid points for numerical", key="nx_n")
        with col2:
            nt_numerical = st.slider("N-Time", 20, 200, 50, 10,
                                   help="Time steps for numerical", key="nt_n")
        
        # Run buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            run_analytical = st.button("🔍 Run Analytical", use_container_width=True,
                                      help="Run or update analytical solution")
        with col2:
            run_numerical = st.button("🧮 Run Numerical", use_container_width=True, type="primary",
                                     help="Run or update numerical solution")
        
        # Clear buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            clear_analytical = st.button("🗑️ Clear Analytical", use_container_width=True)
        with col2:
            clear_numerical = st.button("🗑️ Clear Numerical", use_container_width=True)
        
        clear_all = st.button("🔄 Clear All", use_container_width=True)
    
    return {
        'alpha': alpha,
        'T': T,
        'ic_type': ic_type,
        'bc_type': bc_type,
        'nx_analytical': nx_analytical,
        'nt_analytical': nt_analytical,
        'nx_numerical': nx_numerical,
        'nt_numerical': nt_numerical,
        'run_analytical': run_analytical,
        'run_numerical': run_numerical,
        'clear_analytical': clear_analytical,
        'clear_numerical': clear_numerical,
        'clear_all': clear_all
    }
