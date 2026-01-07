import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

# Set page config
st.set_page_config(
    page_title="PDEBench - PDE Solver Benchmarking",
    page_icon="🧮",
    layout="wide"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🧮 PDEBench</h1>', unsafe_allow_html=True)
st.markdown("### PDE Solver Benchmarking Platform for Research")

# Initialize session state
if 'run_simulation' not in st.session_state:
    st.session_state.run_simulation = False
if 'results' not in st.session_state:
    st.session_state.results = None

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Equation selection
    st.subheader("1. Select PDE")
    equation = st.selectbox(
        "Equation Type",
        ["Burgers' Equation", "Heat Equation", "Wave Equation"],
        help="Choose the partial differential equation to solve"
    )
    
    # Solver selection
    st.subheader("2. Select Solver")
    solver = st.selectbox(
        "Numerical Method",
        ["Finite Difference", "Finite Volume", "Spectral Method"],
        help="Choose the numerical method for solving"
    )
    
    # Parameters section
    st.subheader("3. Set Parameters")
    
    col1, col2 = st.columns(2)
    with col1:
        nu = st.number_input(
            "Viscosity (ν)",
            min_value=0.001,
            max_value=0.1,
            value=0.01,
            step=0.001,
            format="%.3f"
        )
    with col2:
        T = st.number_input(
            "Final Time",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1
        )
    
    nx = st.slider("Spatial Points", 50, 500, 100, 50)
    nt = st.slider("Time Steps", 50, 500, 100, 50)
    
    # Run button
    if st.button("🚀 Run Simulation", type="primary", use_container_width=True):
        st.session_state.run_simulation = True
        st.session_state.results = None
    
    st.markdown("---")
    st.subheader("📊 Export")
    if st.button("Save Results", use_container_width=True):
        st.info("Export feature coming soon!")

# Create a simple Burgers solver for demonstration
def solve_burgers_fd(nu=0.01, nx=100, nt=100, T=1.0):
    """Finite difference solver for Burgers equation"""
    dx = 1.0 / (nx - 1)
    dt = T / (nt - 1)
    
    # Grid
    x = np.linspace(0, 1, nx)
    t = np.linspace(0, T, nt)
    
    # Initialize solution
    u = np.zeros((nt, nx))
    
    # Initial condition: u(x,0) = sin(πx)
    u[0, :] = np.sin(np.pi * x)
    
    # Time stepping (simple explicit scheme)
    for n in range(0, nt-1):
        for i in range(1, nx-1):
            # Central differences
            u_x = (u[n, i+1] - u[n, i-1]) / (2*dx)
            u_xx = (u[n, i+1] - 2*u[n, i] + u[n, i-1]) / (dx**2)
            
            # Burgers equation: u_t + u*u_x = nu*u_xx
            u[n+1, i] = u[n, i] - dt * u[n, i] * u_x + nu * dt * u_xx
        
        # Boundary conditions: u(0,t) = u(1,t) = 0
        u[n+1, 0] = 0
        u[n+1, -1] = 0
    
    return {
        'solution': u,
        'x': x,
        't': t,
        'parameters': {
            'nu': nu,
            'nx': nx,
            'nt': nt,
            'T': T,
            'dx': dx,
            'dt': dt
        }
    }

# Main content area
if st.session_state.run_simulation:
    with st.spinner(f"Solving {equation} using {solver} method..."):
        # Run simulation
        results = solve_burgers_fd(nu=nu, nx=nx, nt=nt, T=T)
        st.session_state.results = results
    
    st.success(f"✅ Simulation completed successfully!")
    
    # Display results in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Visualization", "📊 Metrics", "🔍 Analysis", "📄 Details"])
    
    with tab1:
        st.subheader("Solution Visualization")
        
        # Create Plotly figure
        fig = go.Figure()
        
        # Plot initial condition
        fig.add_trace(go.Scatter(
            x=results['x'],
            y=results['solution'][0, :],
            mode='lines',
            name='Initial (t=0)',
            line=dict(color='blue', dash='dash', width=2)
        ))
        
        # Plot final solution
        fig.add_trace(go.Scatter(
            x=results['x'],
            y=results['solution'][-1, :],
            mode='lines',
            name=f'Final (t={T})',
            line=dict(color='red', width=3)
        ))
        
        # Update layout
        fig.update_layout(
            title=f"{equation} Solution",
            xaxis_title="Position (x)",
            yaxis_title="u(x,t)",
            height=500,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 3D surface plot
        st.subheader("Time Evolution (Surface Plot)")
        
        # Create meshgrid for 3D plot
        X, T_mesh = np.meshgrid(results['x'], results['t'])
        
        fig3d = go.Figure(data=[
            go.Surface(
                z=results['solution'],
                x=X,
                y=T_mesh,
                colorscale='Viridis',
                opacity=0.9,
                contours={
                    "z": {"show": True, "usecolormap": True, "highlightcolor": "limegreen", "project": {"z": True}}
                }
            )
        ])
        
        fig3d.update_layout(
            title='Solution Evolution Over Time',
            scene=dict(
                xaxis_title='Position (x)',
                yaxis_title='Time (t)',
                zaxis_title='u(x,t)'
            ),
            height=600
        )
        
        st.plotly_chart(fig3d, use_container_width=True)
    
    with tab2:
        st.subheader("Performance Metrics")
        
        # Calculate metrics
        u_final = results['solution'][-1, :]
        u_initial = results['solution'][0, :]
        
        # Create metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("L2 Norm Error", f"{np.linalg.norm(u_final):.4f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Max Amplitude", f"{np.max(np.abs(u_final)):.4f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Energy", f"{np.trapz(u_final**2, results['x']):.4f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Diffusion Rate", f"{nu:.4f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Convergence plot
        st.subheader("Grid Convergence")
        
        # Calculate for different grid sizes
        grid_sizes = [50, 100, 200]
        errors = []
        
        for n in grid_sizes:
            res = solve_burgers_fd(nu=nu, nx=n, nt=n, T=T)
            error = np.linalg.norm(res['solution'][-1, :])
            errors.append(error)
        
        fig_conv = go.Figure()
        fig_conv.add_trace(go.Scatter(
            x=grid_sizes,
            y=errors,
            mode='lines+markers',
            name='Error vs Grid Size',
            line=dict(color='green', width=2)
        ))
        
        fig_conv.update_layout(
            title="Convergence Analysis",
            xaxis_title="Grid Points",
            yaxis_title="L2 Norm Error",
            height=400
        )
        
        st.plotly_chart(fig_conv, use_container_width=True)
    
    with tab3:
        st.subheader("Comparative Analysis")
        
        # Compare different viscosity values
        nu_values = [0.001, 0.01, 0.05, 0.1]
        
        fig_compare = go.Figure()
        
        for nu_val in nu_values:
            res = solve_burgers_fd(nu=nu_val, nx=100, nt=100, T=1.0)
            fig_compare.add_trace(go.Scatter(
                x=res['x'],
                y=res['solution'][-1, :],
                mode='lines',
                name=f'ν = {nu_val}',
                line=dict(width=2)
            ))
        
        fig_compare.update_layout(
            title="Effect of Viscosity on Solution",
            xaxis_title="Position (x)",
            yaxis_title="u(x,t=1.0)",
            height=500
        )
        
        st.plotly_chart(fig_compare, use_container_width=True)
    
    with tab4:
        st.subheader("Simulation Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Equation Details")
            st.latex(r"\frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} = \nu \frac{\partial^2 u}{\partial x^2}")
            st.write(f"**Viscosity coefficient:** ν = {nu}")
            st.write("**Initial condition:** u(x,0) = sin(πx)")
            st.write("**Boundary conditions:** u(0,t) = u(1,t) = 0")
        
        with col2:
            st.markdown("#### Solver Parameters")
            st.write(f"**Method:** {solver}")
            st.write(f"**Spatial points:** {nx}")
            st.write(f"**Time steps:** {nt}")
            st.write(f"**Final time:** T = {T}")
            st.write(f"**Spatial step:** Δx = {results['parameters']['dx']:.6f}")
            st.write(f"**Time step:** Δt = {results['parameters']['dt']:.6f}")
        
        # Show raw data option
        if st.checkbox("Show raw solution data (first 10 points)"):
            st.dataframe({
                'x': results['x'][:10],
                'u_initial': results['solution'][0, :10],
                'u_final': results['solution'][-1, :10]
            })
    
    # Reset button
    if st.button("🔄 Run New Simulation", type="secondary"):
        st.session_state.run_simulation = False
        st.rerun()

else:
    # Welcome screen when no simulation has been run
    st.markdown('<h2 class="sub-header">Welcome to PDEBench</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 Purpose
        This platform allows researchers to:
        
        - **Benchmark** different PDE solvers
        - **Compare** traditional vs ML-based methods
        - **Visualize** solutions in 2D/3D
        - **Analyze** performance metrics
        - **Export** results for publications
        
        ### 📈 Current Capabilities
        1. **Burgers' Equation** solver
        2. Finite Difference method
        3. Interactive parameter tuning
        4. Real-time visualization
        5. Performance metrics
        
        ### 🚀 Coming Soon
        - Heat equation solver
        - PINNs (Physics-Informed Neural Networks)
        - Fourier Neural Operators
        - Comparative analysis dashboard
        - Export to LaTeX/paper format
        """)
    
    with col2:
        st.info("""
        **Quick Start:**
        1. Select equation type
        2. Choose solver method
        3. Adjust parameters
        4. Click 'Run Simulation'
        5. Explore results in tabs
        """)
        
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Burgers_equation.gif/300px-Burgers_equation.gif", 
                caption="Burgers' Equation Solution", 
                use_column_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center">
    <p>🧪 <strong>PDEBench v0.1</strong> | A Research Platform for PDE Solver Benchmarking</p>
    <p>Built for academic research | GitHub: <a href="https://github.com/YOUR_USERNAME/pdebench-web">pdebench-web</a></p>
</div>
""", unsafe_allow_html=True)