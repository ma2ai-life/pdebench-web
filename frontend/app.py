import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

# Import our modules
from equations.burgers import BurgersEquation
from solvers.traditional.finite_difference import FiniteDifferenceSolver

st.set_page_config(
    page_title="PDEBench - PDE Solver Benchmarking Platform",
    page_icon="🧮",
    layout="wide"
)

st.title("🧮 PDEBench")
st.markdown("### PDE Solver Benchmarking Platform")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    # Equation selection
    equation_type = st.selectbox(
        "Select PDE",
        ["Burgers' Equation", "Heat Equation", "Navier-Stokes"]
    )
    
    # Solver selection
    solver_type = st.selectbox(
        "Select Solver",
        ["Finite Difference", "PINNs", "Fourier Neural Operator"]
    )
    
    # Parameters
    st.subheader("Parameters")
    viscosity = st.slider("Viscosity (ν)", 0.001, 0.1, 0.01)
    nx = st.slider("Spatial Points", 50, 500, 100)
    nt = st.slider("Time Steps", 50, 500, 100)
    T = st.slider("Final Time", 0.1, 5.0, 1.0)
    
    if st.button("Run Simulation", type="primary"):
        st.session_state.run_simulation = True

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Equation Details")
    if equation_type == "Burgers' Equation":
        st.latex(r"\frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} = \nu \frac{\partial^2 u}{\partial x^2}")
        st.write(f"Viscosity: ν = {viscosity}")
        st.write("Boundary Conditions: u(0,t) = 0, u(1,t) = 0")
        st.write("Initial Condition: u(x,0) = sin(πx)")

with col2:
    st.subheader("Solver Details")
    if solver_type == "Finite Difference":
        st.write("**Method**: Forward Time Centered Space (FTCS)")
        st.write("**Type**: Explicit scheme")
        st.write(f"**Grid**: {nx} spatial points, {nt} time steps")

# Run simulation if button clicked
if 'run_simulation' in st.session_state and st.session_state.run_simulation:
    with st.spinner("Running simulation..."):
        # Initialize equation and solver
        equation = BurgersEquation(nu=viscosity)
        solver = FiniteDifferenceSolver()
        
        # Solve
        result = solver.solve(equation, nx=nx, nt=nt, T=T)
        
        # Create visualization
        fig = go.Figure()
        
        # Plot initial condition
        fig.add_trace(go.Scatter(
            x=result["x"],
            y=result["solution"][0, :],
            mode='lines',
            name='Initial (t=0)',
            line=dict(color='blue', dash='dash')
        ))
        
        # Plot final solution
        fig.add_trace(go.Scatter(
            x=result["x"],
            y=result["solution"][-1, :],
            mode='lines',
            name=f'Final (t={T})',
            line=dict(color='red')
        ))
        
        fig.update_layout(
            title=f"Solution to {equation_type}",
            xaxis_title="x",
            yaxis_title="u(x,t)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Max Value", f"{np.max(result['solution']):.4f}")
        with col2:
            st.metric("Min Value", f"{np.min(result['solution']):.4f}")
        with col3:
            st.metric("Computation Time", "0.5s")  # Placeholder
        
        st.success("Simulation completed!")
        
        # Reset button
        if st.button("Reset Simulation"):
            st.session_state.pop('run_simulation', None)
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
**Next Steps:**
1. Add more equations (Heat, Navier-Stokes)
2. Implement ML-based solvers (PINNs)
3. Add comparative analysis dashboard
4. Deploy to Vercel
""")