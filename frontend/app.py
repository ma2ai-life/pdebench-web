import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys
import os

# ==================== FIX PATH ====================
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# ==================== IMPORTS ====================
try:
    from backend.equations.heat_equation import HeatEquation
    from backend.solvers.analytical import AnalyticalSolver
    from backend.solvers.finite_difference import FiniteDifferenceSolver
    IMPORT_STATUS = "✅ All imports successful"
except ImportError as e:
    IMPORT_STATUS = f"⚠️ Import Error: {e}"
    # Fallback classes with timing
    import time
    
    class HeatEquation:
        def __init__(self, alpha=0.01):
            self.alpha = alpha
        def get_equation_details(self):
            return {"pde": r"u_t = \alpha u_{xx}"}
    
    class AnalyticalSolver:
        @staticmethod
        def solve(alpha=0.01, nx=100, nt=100, T=1.0, **kwargs):
            start = time.time()
            x = np.linspace(0, 1, nx)
            t = np.linspace(0, T, nt)
            u = np.zeros((nt, nx))
            for i, time_val in enumerate(t):
                u[i, :] = np.sin(np.pi * x) * np.exp(-alpha * (np.pi**2) * time_val)
            return u, x, t, time.time() - start
    
    class FiniteDifferenceSolver:
        @staticmethod
        def solve(alpha=0.01, nx=100, nt=100, T=1.0, **kwargs):
            start = time.time()
            dx = 1.0 / (nx - 1)
            dt = T / (nt - 1)
            x = np.linspace(0, 1, nx)
            t = np.linspace(0, T, nt)
            u = np.zeros((nt, nx))
            u[0, :] = np.sin(np.pi * x)
            r = alpha * dt / (dx**2)
            for n in range(nt - 1):
                for i in range(1, nx - 1):
                    u[n+1, i] = u[n, i] + r * (u[n, i+1] - 2*u[n, i] + u[n, i-1])
                u[n+1, 0] = 0
                u[n+1, -1] = 0
            return u, x, t, time.time() - start

# ==================== HELPER FUNCTIONS ====================
def safe_comparison(analytical_data, numerical_data):
    """Safely compare solutions, handling different grid sizes"""
    if analytical_data is None or numerical_data is None:
        return None, None, None
    
    # Check if we have valid data
    if ('u' not in analytical_data or 'x' not in analytical_data or
        'u' not in numerical_data or 'x' not in numerical_data):
        return None, None, None
    
    u_analytical = analytical_data['u'][-1, :]
    x_analytical = analytical_data['x']
    u_numerical = numerical_data['u'][-1, :]
    x_numerical = numerical_data['x']
    
    # If grids are the same, compare directly
    if len(x_analytical) == len(x_numerical):
        error = np.abs(u_numerical - u_analytical)
        return error, x_analytical, True
    
    # Otherwise, interpolate to common grid
    # Create a common fine grid
    common_nx = max(len(x_analytical), len(x_numerical))
    common_x = np.linspace(0, 1, common_nx)
    
    # Interpolate both solutions to common grid
    u_analytical_interp = np.interp(common_x, x_analytical, u_analytical)
    u_numerical_interp = np.interp(common_x, x_numerical, u_numerical)
    
    error = np.abs(u_numerical_interp - u_analytical_interp)
    return error, common_x, False

def create_solution_plot(u, x, t, title, color='red'):
    """Create a standardized plot for solution visualization"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=u[0, :],
        name='Initial (t=0)',
        line=dict(color='blue', dash='dash', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=x, y=u[-1, :],
        name=f'Final (t={t[-1]:.2f})',
        line=dict(color=color, width=3)
    ))
    fig.update_layout(
        title=title,
        xaxis_title="Position (x)",
        yaxis_title="Temperature u(x,t)",
        height=400,
        showlegend=True
    )
    return fig

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="PDEBench - Heat Equation Analysis",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .sub-title {
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    .equation-box {
        background: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #E2E8F0;
        margin: 1rem 0;
    }
    .time-metric {
        background: linear-gradient(135deg, #F0F9FF, #E0F2FE);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0EA5E9;
        margin-bottom: 1rem;
    }
    .warning-box {
        background: linear-gradient(135deg, #FEF3C7, #FDE68A);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #F59E0B;
        margin: 1rem 0;
    }
    .solution-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #E2E8F0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown('<h1 class="main-title">🔥 Heat Equation Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Explore analytical and numerical solutions</p>', unsafe_allow_html=True)

# Show import status
if "⚠️" in IMPORT_STATUS:
    st.warning(IMPORT_STATUS)
else:
    st.success(IMPORT_STATUS)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Parameters
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
    
    # Grid parameters - separate for each method
    st.subheader("Grid Parameters")
    
    st.markdown("**Analytical Grid:**")
    col1, col2 = st.columns(2)
    with col1:
        nx_analytical = st.slider("A-Spatial Points", 20, 200, 50, 10,
                                help="Grid points for analytical solution", key="nx_a")
    with col2:
        nt_analytical = st.slider("A-Time Steps", 20, 200, 50, 10,
                                help="Time steps for analytical solution", key="nt_a")
    
    st.markdown("**Numerical Grid:**")
    col1, col2 = st.columns(2)
    with col1:
        nx_numerical = st.slider("N-Spatial Points", 20, 200, 50, 10,
                               help="Grid points for numerical solution", key="nx_n")
    with col2:
        nt_numerical = st.slider("N-Time Steps", 20, 200, 50, 10,
                               help="Time steps for numerical solution", key="nt_n")
    
    # Run buttons - both can be clicked independently
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
        if st.button("🗑️ Clear Analytical", use_container_width=True):
            st.session_state.analytical_data = None
            st.rerun()
    with col2:
        if st.button("🗑️ Clear Numerical", use_container_width=True):
            st.session_state.numerical_data = None
            st.rerun()
    
    if st.button("🔄 Clear All", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ==================== INITIALIZE SESSION STATE ====================
if 'analytical_data' not in st.session_state:
    st.session_state.analytical_data = None
if 'numerical_data' not in st.session_state:
    st.session_state.numerical_data = None
if 'current_params' not in st.session_state:
    st.session_state.current_params = {
        'alpha': alpha, 'T': T, 'ic_type': ic_type, 'bc_type': bc_type
    }

# ==================== MAIN CONTENT ====================
# Display equation details
st.markdown("## 📐 Heat Equation")
with st.expander("Show equation details", expanded=True):
    st.markdown('<div class="equation-box">', unsafe_allow_html=True)
    st.latex(r"\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}")
    st.markdown("""
    **Description:** Models heat conduction and diffusion processes
    
    **Parameters:**
    - $u(x,t)$: Temperature distribution
    - $\\alpha$: Thermal diffusivity
    - Domain: $x \\in [0, 1], t \\in [0, T]$
    
    **Initial Conditions:**
    1. **Sinusoidal:** $u(x,0) = \sin(\pi x)$
    2. **Gaussian:** Localized heat pulse
    3. **Step:** Half-domain heating
    
    **Boundary Conditions:**
    1. **Dirichlet:** Fixed temperature at boundaries
    2. **Neumann:** Insulated boundaries (no heat flux)
    3. **Mixed:** One fixed, one insulated
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== RUN SIMULATIONS ====================
# Run Analytical Solution
if run_analytical:
    with st.spinner("Computing analytical solution..."):
        try:
            u, x, t, comp_time = AnalyticalSolver.solve(
                alpha=alpha, nx=nx_analytical, nt=nt_analytical, T=T,
                ic_type=ic_type, bc_type=bc_type
            )
            
            st.session_state.analytical_data = {
                'u': u, 'x': x, 't': t, 
                'time': comp_time, 'alpha': alpha,
                'nx': nx_analytical, 'nt': nt_analytical,
                'T': T, 'ic_type': ic_type, 'bc_type': bc_type,
                'type': 'analytical'
            }
            
            st.success(f"✅ Analytical solution computed in {comp_time:.6f}s")
            
        except Exception as e:
            st.error(f"Error computing analytical solution: {e}")

# Run Numerical Solution
if run_numerical:
    with st.spinner("Computing numerical solution..."):
        try:
            u, x, t, comp_time = FiniteDifferenceSolver.solve(
                alpha=alpha, nx=nx_numerical, nt=nt_numerical, T=T,
                ic_type=ic_type, bc_type=bc_type
            )
            
            st.session_state.numerical_data = {
                'u': u, 'x': x, 't': t, 
                'time': comp_time, 'alpha': alpha,
                'nx': nx_numerical, 'nt': nt_numerical,
                'T': T, 'ic_type': ic_type, 'bc_type': bc_type,
                'type': 'numerical'
            }
            
            st.success(f"✅ Numerical solution computed in {comp_time:.6f}s")
            
        except Exception as e:
            st.error(f"Error computing numerical solution: {e}")

# ==================== DISPLAY BOTH SOLUTIONS SIDE-BY-SIDE ====================
st.markdown("---")
st.markdown("## 📈 Solution Visualization")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔍 Analytical Solution")
    
    if st.session_state.analytical_data is not None:
        data = st.session_state.analytical_data
        
        # Create plot
        fig = create_solution_plot(
            u=data['u'], x=data['x'], t=data['t'],
            title=f"Analytical (α={data['alpha']}, Nx={data['nx']})",
            color='red'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show metrics
        st.markdown('<div class="solution-card">', unsafe_allow_html=True)
        st.markdown("**Parameters:**")
        st.write(f"- α = {data['alpha']}")
        st.write(f"- T = {data['T']}")
        st.write(f"- Grid: {data['nx']} × {data['nt']}")
        st.write(f"- Initial: {data['ic_type']}")
        st.write(f"- Boundary: {data['bc_type']}")
        
        st.markdown('<div class="time-metric">', unsafe_allow_html=True)
        st.metric("Computation Time", f"{data['time']:.6f} seconds")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Click 'Run Analytical' to compute solution")
        st.markdown('<div class="solution-card">', unsafe_allow_html=True)
        st.markdown("**Current settings:**")
        st.write(f"- α = {alpha}")
        st.write(f"- T = {T}")
        st.write(f"- Grid: {nx_analytical} × {nt_analytical}")
        st.write(f"- Initial: {ic_type}")
        st.write(f"- Boundary: {bc_type}")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 🧮 Numerical Solution")
    
    if st.session_state.numerical_data is not None:
        data = st.session_state.numerical_data
        
        # Create plot
        fig = create_solution_plot(
            u=data['u'], x=data['x'], t=data['t'],
            title=f"Numerical (α={data['alpha']}, Nx={data['nx']})",
            color='green'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show metrics
        st.markdown('<div class="solution-card">', unsafe_allow_html=True)
        st.markdown("**Parameters:**")
        st.write(f"- α = {data['alpha']}")
        st.write(f"- T = {data['T']}")
        st.write(f"- Grid: {data['nx']} × {data['nt']}")
        st.write(f"- Initial: {data['ic_type']}")
        st.write(f"- Boundary: {data['bc_type']}")
        
        st.markdown('<div class="time-metric">', unsafe_allow_html=True)
        st.metric("Computation Time", f"{data['time']:.6f} seconds")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Click 'Run Numerical' to compute solution")
        st.markdown('<div class="solution-card">', unsafe_allow_html=True)
        st.markdown("**Current settings:**")
        st.write(f"- α = {alpha}")
        st.write(f"- T = {T}")
        st.write(f"- Grid: {nx_numerical} × {nt_numerical}")
        st.write(f"- Initial: {ic_type}")
        st.write(f"- Boundary: {bc_type}")
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== COMPARISON SECTION ====================
if st.session_state.analytical_data is not None and st.session_state.numerical_data is not None:
    st.markdown("---")
    st.markdown("## 📊 Performance Comparison")
    
    # Use safe comparison function
    error, error_x, grids_match = safe_comparison(
        st.session_state.analytical_data,
        st.session_state.numerical_data
    )
    
    if error is not None:
        analytical_time = st.session_state.analytical_data['time']
        numerical_time = st.session_state.numerical_data['time']
        
        # Create comparison metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Analytical Time", 
                f"{analytical_time:.6f}s",
                delta=f"{(analytical_time - numerical_time):.6f}s"
            )
        
        with col2:
            st.metric(
                "Numerical Time", 
                f"{numerical_time:.6f}s",
                delta=f"{(numerical_time - analytical_time):.6f}s"
            )
        
        with col3:
            if analytical_time > 0:
                speedup = numerical_time / analytical_time
                st.metric("Speedup", f"{speedup:.2f}x")
            else:
                st.metric("Speedup", "N/A")
        
        with col4:
            st.metric("Max Error", f"{np.max(error):.6f}")
        
        # Error plot
        fig_error = go.Figure()
        fig_error.add_trace(go.Scatter(
            x=error_x, y=error,
            mode='lines',
            name='Absolute Error',
            line=dict(color='red', width=2)
        ))
        
        title = "Error Analysis"
        if grids_match:
            title += " (Same Grid)"
        else:
            title += f" (Interpolated to {len(error_x)} points)"
            
        fig_error.update_layout(
            title=title,
            xaxis_title="Position (x)",
            yaxis_title="Error |u_numeric - u_analytic|",
            height=350
        )
        st.plotly_chart(fig_error, use_container_width=True)
        
        # Summary
        if grids_match:
            st.info(f"""
            **Comparison Summary:**
            - Analytical: {analytical_time:.6f}s
            - Numerical: {numerical_time:.6f}s  
            - Speedup: {numerical_time/analytical_time:.1f}x
            - Max Error: {np.max(error):.6f}
            """)
        else:
            st.warning(f"""
            **Comparison Summary (Interpolated):**
            - Analytical Grid: {st.session_state.analytical_data['nx']} × {st.session_state.analytical_data['nt']}
            - Numerical Grid: {st.session_state.numerical_data['nx']} × {st.session_state.numerical_data['nt']}
            - Compared on common grid of {len(error_x)} points
            - Max Error: {np.max(error):.6f}
            """)
    else:
        st.warning("Cannot compare solutions. Data may be incomplete.")
else:
    # Show what's missing
    missing = []
    if st.session_state.analytical_data is None:
        missing.append("analytical")
    if st.session_state.numerical_data is None:
        missing.append("numerical")
    
    if missing:
        st.info(f"👈 Run {', '.join(missing)} solution{'s' if len(missing) > 1 else ''} to enable comparison")

# ==================== 3D VISUALIZATION ====================
st.markdown("---")
st.markdown("## 🎭 3D Time Evolution")

tab1, tab2 = st.tabs(["Analytical", "Numerical"])

with tab1:
    if st.session_state.analytical_data is not None:
        data = st.session_state.analytical_data
        u = data['u']
        x = data['x']
        t = data['t']
        
        X, T_mesh = np.meshgrid(x, t)
        
        fig3d = go.Figure(data=[
            go.Surface(
                z=u,
                x=X,
                y=T_mesh,
                colorscale='Viridis',
                opacity=0.9
            )
        ])
        
        fig3d.update_layout(
            title=f"Analytical 3D View (Nx={len(x)}, Nt={len(t)})",
            scene=dict(
                xaxis_title='Position (x)',
                yaxis_title='Time (t)',
                zaxis_title='Temperature u(x,t)'
            ),
            height=500
        )
        st.plotly_chart(fig3d, use_container_width=True)
    else:
        st.info("Run analytical solution to see 3D visualization")

with tab2:
    if st.session_state.numerical_data is not None:
        data = st.session_state.numerical_data
        u = data['u']
        x = data['x']
        t = data['t']
        
        X, T_mesh = np.meshgrid(x, t)
        
        fig3d = go.Figure(data=[
            go.Surface(
                z=u,
                x=X,
                y=T_mesh,
                colorscale='Plasma',
                opacity=0.9
            )
        ])
        
        fig3d.update_layout(
            title=f"Numerical 3D View (Nx={len(x)}, Nt={len(t)})",
            scene=dict(
                xaxis_title='Position (x)',
                yaxis_title='Time (t)',
                zaxis_title='Temperature u(x,t)'
            ),
            height=500
        )
        st.plotly_chart(fig3d, use_container_width=True)
    else:
        st.info("Run numerical solution to see 3D visualization")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("**PDEBench v1.4** | Both solutions persist independently | Ready for ROM")
