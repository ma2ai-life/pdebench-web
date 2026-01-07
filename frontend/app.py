import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

# Import solver
try:
    from solvers.traditional.finite_difference import FiniteDifferenceSolver
    solver_available = True
except ImportError:
    st.error("⚠️ Could not import solver. Check backend structure.")
    solver_available = False

# Streamlit app
st.set_page_config(
    page_title="PDEBench - PDE Solver Benchmarking",
    page_icon="🧮",
    layout="wide"
)

st.title("🧮 PDEBench - PDE Solver Benchmarking Platform")
st.markdown("### Test and compare different PDE solvers")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    equation = st.selectbox(
        "Select PDE",
        ["Burgers' Equation", "Heat Equation"]
    )
    
    st.subheader("Parameters")
    
    if equation == "Burgers' Equation":
        nu = st.slider("Viscosity (ν)", 0.001, 0.1, 0.01, 0.001)
    else:
        nu = st.slider("Diffusion Coefficient (α)", 0.001, 0.1, 0.01, 0.001)
    
    nx = st.slider("Spatial Points", 50, 200, 100, 10)
    nt = st.slider("Time Steps", 50, 200, 100, 10)
    T = st.slider("Final Time", 0.1, 5.0, 1.0, 0.1)

# Main content
if st.button("🚀 Run Simulation", type="primary"):
    if not solver_available:
        st.error("Solver not available. Check file structure.")
    else:
        with st.spinner("Solving PDE..."):
            if equation == "Burgers' Equation":
                u, x, t = FiniteDifferenceSolver.solve_burgers(nu=nu, nx=nx, nt=nt, T=T)
                title = f"Burgers' Equation (ν={nu})"
            else:
                u, x, t = FiniteDifferenceSolver.solve_heat(alpha=nu, nx=nx, nt=nt, T=T)
                title = f"Heat Equation (α={nu})"
            
            # Create plot
            fig = go.Figure()
            
            # Initial solution
            fig.add_trace(go.Scatter(
                x=x, y=u[0, :],
                mode='lines',
                name='Initial (t=0)',
                line=dict(color='blue', dash='dash')
            ))
            
            # Final solution
            fig.add_trace(go.Scatter(
                x=x, y=u[-1, :],
                mode='lines',
                name=f'Final (t={T})',
                line=dict(color='red', width=2)
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title="x",
                yaxis_title="u(x,t)",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Max Value", f"{u[-1, :].max():.4f}")
            col2.metric("Min Value", f"{u[-1, :].min():.4f}")
            col3.metric("Grid Size", f"{nx} × {nt}")
            
            st.success("✅ Simulation complete!")

# Instructions
st.markdown("---")
st.markdown("""
### 📁 Current Structure Status:
- ✅ `backend/solvers/traditional/finite_difference.py` - Found
- ✅ `frontend/requirements.txt` - Found
- ❌ `frontend/app.py` - Need to create (this file)
- ❌ `backend/equations/burgers.py` - Missing
- ❌ `__init__.py` files - Missing

### Next Steps:
1. Create missing files
2. Fix folder structure
3. Push to GitHub
4. App will auto-deploy
""")