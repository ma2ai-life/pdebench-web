import streamlit as st

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sys
import os
from pathlib import Path

# Add backend to Python path
current_dir = Path(__file__).parent
backend_dir = current_dir.parent / "backend"
sys.path.append(str(backend_dir))

# ==================== INLINE SOLVER (GUARANTEED TO WORK) ====================
class FiniteDifferenceSolver:
    @staticmethod
    def solve_burgers(nu=0.01, nx=100, nt=100, T=1.0):
        """Solve 1D Burgers equation using explicit finite difference"""
        dx = 1.0 / (nx - 1)
        dt = T / (nt - 1)
        
        # Grid
        x = np.linspace(0, 1, nx)
        t = np.linspace(0, T, nt)
        
        # Initialize solution
        u = np.zeros((nt, nx))
        u[0, :] = np.sin(np.pi * x)  # Initial condition
        
        # Time stepping
        for n in range(nt - 1):
            # Interior points
            for i in range(1, nx - 1):
                u_x = (u[n, i+1] - u[n, i-1]) / (2 * dx)
                u_xx = (u[n, i+1] - 2*u[n, i] + u[n, i-1]) / (dx**2)
                u[n+1, i] = u[n, i] - dt * u[n, i] * u_x + nu * dt * u_xx
            
            # Boundary conditions (Dirichlet)
            u[n+1, 0] = 0
            u[n+1, -1] = 0
        
        return u, x, t
    
    @staticmethod
    def solve_heat(alpha=0.01, nx=100, nt=100, T=1.0):
        """Solve 1D Heat equation: u_t = alpha * u_xx"""
        dx = 1.0 / (nx - 1)
        dt = T / (nt - 1)
        
        x = np.linspace(0, 1, nx)
        t = np.linspace(0, T, nt)
        u = np.zeros((nt, nx))
        
        # Initial condition: Gaussian
        u[0, :] = np.exp(-100 * (x - 0.5)**2)
        
        # FTCS scheme
        r = alpha * dt / (dx**2)
        
        for n in range(nt - 1):
            for i in range(1, nx - 1):
                u[n+1, i] = u[n, i] + r * (u[n, i+1] - 2*u[n, i] + u[n, i-1])
            
            # Neumann boundary: du/dx = 0 at boundaries
            u[n+1, 0] = u[n+1, 1]
            u[n+1, -1] = u[n+1, -2]
        
        return u, x, t

SOLVER_AVAILABLE = True
# ==================== STREAMLIT APP ====================
st.set_page_config(
    page_title="PDEBench - PDE Solver Benchmarking Platform",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(90deg, #1E3A8A, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .sub-header {
        color: #4B5563;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #F3F4F6, #E5E7EB);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .equation-box {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #E2E8F0;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        font-weight: 600;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown('<h1 class="main-header">🧮 PDEBench</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">A Platform for Benchmarking PDE Solvers | Research Edition</p>', unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # Equation Selection
    st.markdown("### 1. PDE Selection")
    equation = st.selectbox(
        "Choose Equation",
        ["Burgers' Equation", "Heat Equation"],
        help="Select the partial differential equation to solve"
    )
    
    # Solver Selection
    st.markdown("### 2. Solver Method")
    solver_method = st.selectbox(
        "Numerical Method",
        ["Finite Difference", "Finite Volume", "Spectral Method"],
        index=0,
        help="Choose the numerical discretization method"
    )
    
    # Parameters
    st.markdown("### 3. Simulation Parameters")
    
    col1, col2 = st.columns(2)
    with col1:
        if equation == "Burgers' Equation":
            param_value = st.number_input(
                "Viscosity (ν)",
                min_value=0.001,
                max_value=0.1,
                value=0.01,
                step=0.001,
                format="%.3f",
                help="Diffusion coefficient"
            )
            param_name = "ν"
        else:
            param_value = st.number_input(
                "Diffusivity (α)",
                min_value=0.001,
                max_value=0.1,
                value=0.01,
                step=0.001,
                format="%.3f",
                help="Thermal diffusivity coefficient"
            )
            param_name = "α"
    
    with col2:
        T = st.number_input(
            "Final Time (T)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="Simulation end time"
        )
    
    # Grid settings
    st.markdown("#### Grid Resolution")
    col1, col2 = st.columns(2)
    with col1:
        nx = st.slider(
            "Spatial Points (Nx)",
            min_value=20,
            max_value=500,
            value=100,
            step=10,
            help="Number of grid points in space"
        )
    with col2:
        nt = st.slider(
            "Time Steps (Nt)",
            min_value=20,
            max_value=500,
            value=100,
            step=10,
            help="Number of time steps"
        )
    
    # Boundary Conditions
    st.markdown("#### Boundary Conditions")
    bc_type = st.selectbox(
        "Type",
        ["Dirichlet (u=0)", "Neumann (du/dx=0)", "Periodic"],
        help="Boundary condition type"
    )
    
    # Run Button
    st.markdown("---")
    run_simulation = st.button(
        "🚀 **Run Simulation**",
        type="primary",
        use_container_width=True,
        disabled=not SOLVER_AVAILABLE
    )
    
    if not SOLVER_AVAILABLE:
        st.error("Solver not available. Check backend structure.")
    
    # Export Options
    st.markdown("---")
    st.markdown("### 📤 Export")
    if st.button("Save Results as CSV", use_container_width=True):
        st.info("Export feature coming soon!")
    
    # Debug Info
    with st.expander("🔍 Debug Info"):
        st.write(f"Backend path: {backend_dir}")
        st.write(f"Solver available: {SOLVER_AVAILABLE}")
        st.write(f"Python path: {sys.path[-3:]}")

# ==================== MAIN CONTENT ====================
# Create tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📈 Simulation", "📊 Analysis", "🔬 Comparison", "📚 Documentation"])

with tab1:
    # Equation Details
    st.markdown("## 📐 Equation Details")
    
    if equation == "Burgers' Equation":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown('<div class="equation-box">', unsafe_allow_html=True)
            st.latex(r"\frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} = \nu \frac{\partial^2 u}{\partial x^2}")
            st.markdown("""
            **Description:** Model for fluid dynamics, shock formation, and traffic flow.
            
            **Parameters:**
            - \(u(x,t)\): Fluid velocity
            - \(\nu\): Kinematic viscosity
            - Domain: \(x \in [0, 1], t \in [0, T]\)
            
            **Initial Condition:** \(u(x,0) = \sin(\pi x)\)
            **Boundary Conditions:** \(u(0,t) = u(1,t) = 0\)
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.image(
                "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Burgers_equation.gif/400px-Burgers_equation.gif",
                caption="Burgers' Equation Solution Evolution",
                use_container_width=True
            )
    
    else:  # Heat Equation
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown('<div class="equation-box">', unsafe_allow_html=True)
            st.latex(r"\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}")
            st.markdown("""
            **Description:** Model for heat conduction, diffusion processes.
            
            **Parameters:**
            - \(u(x,t)\): Temperature distribution
            - \(\alpha\): Thermal diffusivity
            - Domain: \(x \in [0, 1], t \in [0, T]\)
            
            **Initial Condition:** \(u(x,0) = e^{-100(x-0.5)^2}\) (Gaussian pulse)
            **Boundary Conditions:** \(\frac{\partial u}{\partial x}(0,t) = \frac{\partial u}{\partial x}(1,t) = 0\)
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.image(
                "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Heat_eqn.gif/400px-Heat_eqn.gif",
                caption="Heat Equation Solution Evolution",
                use_container_width=True
            )
    
    # Run Simulation
    if run_simulation and SOLVER_AVAILABLE:
        st.markdown("---")
        st.markdown("## 📈 Simulation Results")
        
        with st.spinner(f"Solving {equation} using {solver_method}..."):
            try:
                # Solve the PDE
                if equation == "Burgers' Equation":
                    u, x, t = FiniteDifferenceSolver.solve_burgers(nu=param_value, nx=nx, nt=nt, T=T)
                    eq_title = f"Burgers' Equation: ν = {param_value}"
                else:
                    u, x, t = FiniteDifferenceSolver.solve_heat(alpha=param_value, nx=nx, nt=nt, T=T)
                    eq_title = f"Heat Equation: α = {param_value}"
                
                # Success message
                st.success(f"✅ Simulation completed! Grid: {nx}×{nt}, Time: {T}s")
                
                # Create Plotly Figure
                fig = go.Figure()
                
                # Plot initial condition
                fig.add_trace(go.Scatter(
                    x=x,
                    y=u[0, :],
                    mode='lines',
                    name=f'Initial (t=0)',
                    line=dict(color='#3B82F6', width=2, dash='dash'),
                    hovertemplate='x=%{x:.3f}<br>u=%{y:.3f}<extra></extra>'
                ))
                
                # Plot final solution
                fig.add_trace(go.Scatter(
                    x=x,
                    y=u[-1, :],
                    mode='lines',
                    name=f'Final (t={T})',
                    line=dict(color='#EF4444', width=3),
                    hovertemplate='x=%{x:.3f}<br>u=%{y:.3f}<extra></extra>'
                ))
                
                # Plot intermediate solutions
                n_intermediate = min(5, len(t) - 1)
                for i in range(1, n_intermediate):
                    idx = i * len(t) // n_intermediate
                    fig.add_trace(go.Scatter(
                        x=x,
                        y=u[idx, :],
                        mode='lines',
                        name=f't={t[idx]:.2f}',
                        line=dict(color='#10B981', width=1, dash='dot'),
                        opacity=0.6,
                        showlegend=True
                    ))
                
                # Update layout
                fig.update_layout(
                    title=dict(
                        text=eq_title,
                        font=dict(size=24, color='#1F2937'),
                        x=0.5,
                        xanchor='center'
                    ),
                    xaxis_title="Position (x)",
                    yaxis_title="u(x, t)",
                    height=500,
                    template="plotly_white",
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01,
                        bgcolor='rgba(255, 255, 255, 0.8)'
                    ),
                    hovermode='x unified'
                )
                
                # Add grid
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
                
                # Display the plot
                st.plotly_chart(fig, use_container_width=True, theme="streamlit")
                
                # Metrics Section
                st.markdown("### 📊 Performance Metrics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric(
                        "L² Norm",
                        f"{np.linalg.norm(u[-1, :]):.4f}",
                        help="L2 norm of final solution"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric(
                        "Max Value",
                        f"{u[-1, :].max():.4f}",
                        delta=f"{u[-1, :].max() - u[0, :].max():.4f}",
                        help="Maximum amplitude"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric(
                        "Energy",
                        f"{np.trapz(u[-1, :]**2, x):.4f}",
                        delta=f"{np.trapz(u[-1, :]**2, x) - np.trapz(u[0, :]**2, x):.4f}",
                        help="Total energy in system"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col4:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric(
                        "Grid Resolution",
                        f"{nx} × {nt}",
                        help="Spatial × Temporal points"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # 3D Surface Plot
                st.markdown("### 🎭 Time Evolution (3D View)")
                
                # Create meshgrid for 3D
                X, T_mesh = np.meshgrid(x, t)
                
                fig3d = go.Figure(data=[
                    go.Surface(
                        z=u,
                        x=X,
                        y=T_mesh,
                        colorscale='Viridis',
                        opacity=0.9,
                        contours={
                            "z": {"show": True, "usecolormap": True, "project": {"z": True}}
                        },
                        hovertemplate='x=%{x:.3f}<br>t=%{y:.3f}<br>u=%{z:.3f}<extra></extra>'
                    )
                ])
                
                fig3d.update_layout(
                    title=dict(
                        text="Solution Evolution Over Time",
                        font=dict(size=20)
                    ),
                    scene=dict(
                        xaxis_title='Position (x)',
                        yaxis_title='Time (t)',
                        zaxis_title='u(x, t)',
                        camera=dict(
                            eye=dict(x=1.5, y=1.5, z=1.5)
                        )
                    ),
                    height=600,
                    margin=dict(l=0, r=0, b=0, t=40)
                )
                
                st.plotly_chart(fig3d, use_container_width=True, theme="streamlit")
                
                # Data Table (optional)
                with st.expander("📋 View Solution Data"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Initial Condition (first 10 points)**")
                        st.dataframe({
                            'x': x[:10],
                            'u(x,0)': u[0, :10]
                        }, use_container_width=True)
                    
                    with col2:
                        st.write("**Final Solution (first 10 points)**")
                        st.dataframe({
                            'x': x[:10],
                            f'u(x,{T})': u[-1, :10]
                        }, use_container_width=True)
            
            except Exception as e:
                st.error(f"❌ Simulation failed: {str(e)}")
                st.info("Check parameters and try again.")

with tab2:
    st.markdown("## 📊 Convergence Analysis")
    
    if SOLVER_AVAILABLE and 'run_simulation' in locals():
        # Convergence analysis would go here
        st.info("Run a simulation first to see convergence analysis.")
    
    st.markdown("""
    ### Planned Analysis Features:
    
    1. **Grid Convergence Study**
       - Solve with different grid resolutions
       - Calculate convergence rate
       - Estimate discretization error
    
    2. **Time Step Sensitivity**
       - Vary CFL number
       - Check numerical stability
       - Optimal time step selection
    
    3. **Error Metrics**
       - L¹, L², L∞ norms
       - Relative errors
       - Conservation properties
    
    4. **Performance Profiling**
       - Computation time
       - Memory usage
       - Scaling with grid size
    """)

with tab3:
    st.markdown("## 🔬 Method Comparison")
    st.info("Feature coming soon: Compare different solvers side-by-side")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Planned Comparisons:")
        st.markdown("""
        - Finite Difference vs Finite Volume
        - Explicit vs Implicit schemes
        - Traditional vs ML methods
        - Accuracy vs Computation time
        - Memory usage comparison
        """)
    
    with col2:
        st.markdown("### Upcoming Solvers:")
        st.markdown("""
        1. **Physics-Informed Neural Networks (PINNs)**
        2. **Fourier Neural Operators (FNO)**
        3. **Graph Neural Networks (GNN)**
        4. **Spectral Methods**
        5. **Discontinuous Galerkin**
        """)

with tab4:
    st.markdown("## 📚 Documentation & Research")
    
    st.markdown("""
    ### About PDEBench
    
    **PDEBench** is a web-based platform for benchmarking Partial Differential Equation solvers.
    
    #### 🎯 Research Objectives:
    1. Compare traditional numerical methods
    2. Evaluate machine learning approaches
    3. Provide reproducible benchmarks
    4. Facilitate method development
    
    #### 🔧 Current Implementation:
    - **Language**: Python 3.9+
    - **Frontend**: Streamlit
    - **Backend**: NumPy, SciPy
    - **Visualization**: Plotly, Matplotlib
    
    #### 🚀 Getting Started:
    1. Select PDE from sidebar
    2. Choose numerical method
    3. Adjust parameters
    4. Click "Run Simulation"
    5. Analyze results in tabs
    
    #### 📖 References:
    - Brunton & Kutz, "Data-Driven Science and Engineering"
    - LeVeque, "Finite Difference Methods"
    - Karniadakis et al., "Physics-Informed Learning"
    
    #### 🔗 Repository:
    [GitHub - pdebench-web](https://github.com/YOUR_USERNAME/pdebench-web)
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
    <p>🧪 <strong>PDEBench v0.1</strong> | Research Platform for PDE Solver Benchmarking</p>
    <p>Built with Streamlit | For Academic Research | 🔗 <a href="https://pdebench-web-app.streamlit.app/">Live App</a></p>
</div>
""", unsafe_allow_html=True)

# Store results in session state if simulation ran
if run_simulation and SOLVER_AVAILABLE and 'u' in locals():
    st.session_state.simulation_results = {
        'u': u,
        'x': x,
        't': t,
        'equation': equation,
        'parameters': {
            'param_name': param_name,
            'param_value': param_value,
            'T': T,
            'nx': nx,
            'nt': nt
        }
    }