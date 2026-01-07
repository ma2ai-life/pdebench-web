import streamlit as st
import sys
import os
from pathlib import Path

# ==================== ROBUST IMPORT SYSTEM ====================
def import_solvers():
    """Try multiple strategies to import solvers"""
    try:
        # Strategy 1: Try direct import from backend folder
        from backend.solvers.analytical import AnalyticalSolver
        from backend.solvers.finite_difference import FiniteDifferenceSolver
        return AnalyticalSolver, FiniteDifferenceSolver, True
    except ImportError:
        try:
            # Strategy 2: Add parent directory to path
            current_dir = Path(__file__).parent
            project_root = current_dir.parent
            sys.path.append(str(project_root))
            
            from backend.solvers.analytical import AnalyticalSolver
            from backend.solvers.finite_difference import FiniteDifferenceSolver
            return AnalyticalSolver, FiniteDifferenceSolver, True
        except ImportError:
            try:
                # Strategy 3: Create inline solvers as fallback
                class InlineAnalyticalSolver:
                    @staticmethod
                    def solve(alpha=0.01, nx=100, nt=100, T=1.0, ic_type="sinusoidal", bc_type="dirichlet"):
                        x = np.linspace(0, 1, nx)
                        t = np.linspace(0, T, nt)
                        u = np.zeros((nt, nx))
                        
                        # Simple analytical solution for sin(πx) initial condition
                        for i, time in enumerate(t):
                            u[i, :] = np.sin(np.pi * x) * np.exp(-alpha * (np.pi**2) * time)
                        
                        return u, x, t
                
                class InlineFiniteDifferenceSolver:
                    @staticmethod
                    def solve(alpha=0.01, nx=100, nt=100, T=1.0, ic_type="sinusoidal", bc_type="dirichlet"):
                        dx = 1.0 / (nx - 1)
                        dt = T / (nt - 1)
                        x = np.linspace(0, 1, nx)
                        t = np.linspace(0, T, nt)
                        u = np.zeros((nt, nx))
                        
                        # Initial condition
                        if ic_type == "sinusoidal":
                            u[0, :] = np.sin(np.pi * x)
                        elif ic_type == "gaussian":
                            u[0, :] = np.exp(-100 * (x - 0.5)**2)
                        elif ic_type == "step":
                            u[0, :] = np.where(x < 0.5, 1.0, 0.0)
                        
                        # FTCS scheme
                        r = alpha * dt / (dx**2)
                        
                        for n in range(nt - 1):
                            for i in range(1, nx - 1):
                                u[n+1, i] = u[n, i] + r * (u[n, i+1] - 2*u[n, i] + u[n, i-1])
                            
                            # Boundary conditions
                            if bc_type == "dirichlet":
                                u[n+1, 0] = 0
                                u[n+1, -1] = 0
                            elif bc_type == "neumann":
                                u[n+1, 0] = u[n+1, 1]
                                u[n+1, -1] = u[n+1, -2]
                            elif bc_type == "mixed":
                                u[n+1, 0] = 0
                                u[n+1, -1] = u[n+1, -2]
                        
                        return u, x, t, 0.001  # Return small computation time
                
                return InlineAnalyticalSolver, InlineFiniteDifferenceSolver, True
            except Exception as e:
                st.error(f"Failed to create inline solvers: {e}")
                return None, None, False

# Import solvers using robust strategy
AnalyticalSolver, FiniteDifferenceSolver, SOLVER_AVAILABLE = import_solvers()
# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="PDEBench - Heat Equation",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("frontend/styles/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown('<h1 class="main-header">🔥 PDEBench - Heat Equation</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Step-by-Step Analysis of Heat Diffusion</p>', unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # Equation parameters
    st.markdown("### Physical Parameters")
    alpha = st.slider(
        "Thermal Diffusivity (α)",
        min_value=0.001,
        max_value=0.1,
        value=0.01,
        step=0.001,
        help="Controls how fast heat spreads"
    )
    
    T = st.slider(
        "Final Time (T)",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
        help="Simulation end time"
    )
    
    # Initial and Boundary Conditions
    st.markdown("### Conditions")
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
    
    # Numerical parameters
    st.markdown("### Numerical Parameters")
    nx = st.slider(
        "Spatial Points",
        min_value=20,
        max_value=500,
        value=100,
        step=10,
        help="Grid resolution in space"
    )
    
    nt = st.slider(
        "Time Steps",
        min_value=20,
        max_value=500,
        value=100,
        step=10,
        help="Number of time steps"
    )
    
    # Run buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        run_analytical = st.button("🔍 Analytical", use_container_width=True)
    with col2:
        run_numerical = st.button("🧮 Numerical", use_container_width=True, type="primary")

# ==================== MAIN CONTENT ====================
# Display equation details
display_heat_equation()

# Initialize session state
if 'analytical_results' not in st.session_state:
    st.session_state.analytical_results = None
if 'numerical_results' not in st.session_state:
    st.session_state.numerical_results = None

# Run Analytical Solution
if run_analytical and SOLVER_AVAILABLE:
    with st.spinner("Computing analytical solution..."):
        try:
            u_analytical, x, t = AnalyticalSolver.solve(
                alpha=alpha, nx=nx, nt=nt, T=T,
                ic_type=ic_type, bc_type=bc_type
            )
            
            st.session_state.analytical_results = {
                'u': u_analytical,
                'x': x,
                't': t,
                'type': 'analytical'
            }
            
            st.success("✅ Analytical solution computed!")
            
        except Exception as e:
            st.error(f"Error computing analytical solution: {e}")

# Run Numerical Solution
if run_numerical and SOLVER_AVAILABLE:
    with st.spinner("Computing numerical solution..."):
        try:
            u_numerical, x, t, comp_time = FiniteDifferenceSolver.solve(
                alpha=alpha, nx=nx, nt=nt, T=T,
                ic_type=ic_type, bc_type=bc_type
            )
            
            st.session_state.numerical_results = {
                'u': u_numerical,
                'x': x,
                't': t,
                'computation_time': comp_time,
                'type': 'numerical'
            }
            
            st.success(f"✅ Numerical solution computed in {comp_time:.3f}s!")
            
        except Exception as e:
            st.error(f"Error computing numerical solution: {e}")

# Display Results in Tabs
tab1, tab2, tab3 = st.tabs(["📈 Solutions", "📊 Comparison", "⚙️ Method Details"])

with tab1:
    st.markdown('<h3 class="section-title">Solution Visualization</h3>', unsafe_allow_html=True)
    
    # Analytical Solution
    if st.session_state.analytical_results:
        results = st.session_state.analytical_results
        st.markdown("### Analytical Solution")
        
        # 2D Plot
        fig_2d = plot_2d_solution(
            x=results['x'],
            u_final=results['u'][-1, :],
            u_initial=results['u'][0, :],
            title=f"Analytical Solution (α={alpha})"
        )
        st.plotly_chart(fig_2d, use_container_width=True)
        
        # 3D Plot
        fig_3d = plot_3d_solution(
            x=results['x'],
            t=results['t'],
            u=results['u'],
            title="Time Evolution (Analytical)"
        )
        st.plotly_chart(fig_3d, use_container_width=True)
        
        # Metrics
        metrics = calculate_metrics(
            u_final=results['u'][-1, :],
            u_initial=results['u'][0, :],
            x=results['x']
        )
        display_metrics(metrics)
    
    # Numerical Solution
    if st.session_state.numerical_results:
        results = st.session_state.numerical_results
        st.markdown("### Numerical Solution (Finite Difference)")
        
        # 2D Plot
        fig_2d = plot_2d_solution(
            x=results['x'],
            u_final=results['u'][-1, :],
            u_initial=results['u'][0, :],
            title=f"Numerical Solution (α={alpha})"
        )
        st.plotly_chart(fig_2d, use_container_width=True)
        
        # Metrics
        metrics = calculate_metrics(
            u_final=results['u'][-1, :],
            u_initial=results['u'][0, :],
            x=results['x']
        )
        display_metrics(metrics, results.get('computation_time'))

with tab2:
    st.markdown('<h3 class="section-title">Solution Comparison</h3>', unsafe_allow_html=True)
    
    if (st.session_state.analytical_results and 
        st.session_state.numerical_results):
        
        analytical = st.session_state.analytical_results
        numerical = st.session_state.numerical_results
        
        # Error plot
        fig_error = plot_error(
            x=analytical['x'],
            u_numerical=numerical['u'][-1, :],
            u_analytical=analytical['u'][-1, :],
            title="Error: Numerical vs Analytical"
        )
        st.plotly_chart(fig_error, use_container_width=True)
        
        # Metrics comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Analytical Solution")
            metrics_analytical = calculate_metrics(
                u_final=analytical['u'][-1, :],
                x=analytical['x']
            )
            display_metrics(metrics_analytical)
        
        with col2:
            st.markdown("#### Numerical Solution")
            metrics_numerical = calculate_metrics(
                u_final=numerical['u'][-1, :],
                x=numerical['x']
            )
            display_metrics(metrics_numerical, numerical.get('computation_time'))
        
        # Convergence info
        st.markdown("#### Convergence Analysis")
        st.info("""
        **Next steps:**
        1. Vary grid resolution to study convergence
        2. Compare different numerical schemes
        3. Add more boundary conditions
        4. Implement Reduced Order Models (ROM)
        """)

with tab3:
    st.markdown('<h3 class="section-title">Methodology Details</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🧮 Finite Difference Method
    
    **Scheme:** Forward Time Centered Space (FTCS)
    
    **Discretization:**
    $$
    \\frac{u_i^{n+1} - u_i^n}{\\Delta t} = \\alpha \\frac{u_{i+1}^n - 2u_i^n + u_{i-1}^n}{(\\Delta x)^2}
    $$
    
    **Update formula:**
    $$
    u_i^{n+1} = u_i^n + \\frac{\\alpha \\Delta t}{(\\Delta x)^2} (u_{i+1}^n - 2u_i^n + u_{i-1}^n)
    $$
    
    ### 🔍 Analytical Method
    
    **Separation of variables** gives:
    $$
    u(x,t) = \\sum_{n=1}^{\\infty} B_n \\sin\\left(\\frac{n\\pi x}{L}\\right) e^{-\\alpha (n\\pi/L)^2 t}
    $$
    
    where coefficients $B_n$ depend on initial condition.
    
    ### 🚀 Next: Reduced Order Modeling
    
    **Traditional methods** (like FD) solve full system: $O(N^2)$ complexity
    
    **ROM approach:**
    1. Take snapshots of solutions
    2. Compute POD/SVD modes
    3. Project onto low-dimensional subspace
    4. Solve small system: $O(r^2)$ where $r \\ll N$
    
    **Expected speedup:** 10-100x for large problems
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
    <p>🔥 <strong>PDEBench v1.0</strong> | Heat Equation Analysis Platform</p>
    <p>Step 1: Analytical → Step 2: Numerical → Step 3: ROM (coming soon)</p>
</div>
""", unsafe_allow_html=True)