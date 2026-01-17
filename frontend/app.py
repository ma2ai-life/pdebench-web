import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys
import os

# ==================== FIX PATH FIRST ====================
# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# ==================== SIMPLE IMPORT SYSTEM ====================
try:
    # Now this should work
    from backend.solvers.analytical import AnalyticalSolver
    from backend.solvers.finite_difference import FiniteDifferenceSolver
    SOLVER_AVAILABLE = True
    IMPORT_STATUS = "✅ Backend imports successful"
except ImportError as e:
    IMPORT_STATUS = f"⚠️ Using inline solvers: {str(e)[:50]}..."
    # Create inline fallback
    class AnalyticalSolver:
        @staticmethod
        def solve(alpha=0.01, nx=100, nt=100, T=1.0, ic_type="sinusoidal", bc_type="dirichlet"):
            x = np.linspace(0, 1, nx)
            t = np.linspace(0, T, nt)
            u = np.zeros((nt, nx))
            for i, time in enumerate(t):
                u[i, :] = np.sin(np.pi * x) * np.exp(-alpha * (np.pi**2) * time)
            return u, x, t
    
    class FiniteDifferenceSolver:
        @staticmethod
        def solve(alpha=0.01, nx=100, nt=100, T=1.0, ic_type="sinusoidal", bc_type="dirichlet"):
            import time
            start = time.time()
            dx = 1.0 / (nx - 1)
            dt = T / (nt - 1)
            x = np.linspace(0, 1, nx)
            t = np.linspace(0, T, nt)
            u = np.zeros((nt, nx))
            
            if ic_type == "sinusoidal":
                u[0, :] = np.sin(np.pi * x)
            elif ic_type == "gaussian":
                u[0, :] = np.exp(-100 * (x - 0.5)**2)
            else:
                u[0, :] = np.where(x < 0.5, 1.0, 0.0)
            
            r = alpha * dt / (dx**2)
            for n in range(nt - 1):
                for i in range(1, nx - 1):
                    u[n+1, i] = u[n, i] + r * (u[n, i+1] - 2*u[n, i] + u[n, i-1])
                if bc_type == "dirichlet":
                    u[n+1, 0] = 0
                    u[n+1, -1] = 0
                else:
                    u[n+1, 0] = u[n+1, 1]
                    u[n+1, -1] = u[n+1, -2]
            
            return u, x, t, time.time() - start
    
    SOLVER_AVAILABLE = True

# ==================== STREAMLIT APP ====================
st.set_page_config(
    page_title="PDEBench - Heat Equation",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 PDEBench - Heat Equation")
st.markdown("### Minimal Working Version")

# Show import status
st.info(IMPORT_STATUS)

# Sidebar
with st.sidebar:
    st.header("Parameters")
    alpha = st.slider("α (Diffusivity)", 0.001, 0.1, 0.01, 0.001)
    nx = st.slider("Grid Points", 20, 200, 50)
    T = st.slider("Final Time", 0.1, 2.0, 1.0, 0.1)
    
    col1, col2 = st.columns(2)
    with col1:
        run_analytical = st.button("Analytical", use_container_width=True)
    with col2:
        run_numerical = st.button("Numerical", use_container_width=True, type="primary")

# Main content
if run_analytical:
    with st.spinner("Computing analytical solution..."):
        u, x, t = AnalyticalSolver.solve(alpha=alpha, nx=nx, T=T)
        
        # Simple plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=u[0, :], name='Initial', line=dict(dash='dash')))
        fig.add_trace(go.Scatter(x=x, y=u[-1, :], name=f'Final (t={T})', line=dict(width=2)))
        fig.update_layout(title=f"Analytical Solution (α={alpha})", height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        st.success("✅ Analytical solution computed!")

if run_numerical:
    with st.spinner("Computing numerical solution..."):
        u, x, t, comp_time = FiniteDifferenceSolver.solve(alpha=alpha, nx=nx, T=T)
        
        # Simple plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=u[0, :], name='Initial', line=dict(dash='dash')))
        fig.add_trace(go.Scatter(x=x, y=u[-1, :], name=f'Final (t={T})', line=dict(width=2)))
        fig.update_layout(title=f"Numerical Solution (α={alpha})", height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        st.success(f"✅ Numerical solution computed in {comp_time:.3f}s!")

# Footer
st.markdown("---")
st.markdown("**Test:** Try both buttons - they should work now!")
