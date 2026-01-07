import streamlit as st

def display_heat_equation():
    """Display Heat Equation details"""
    st.markdown("""
    ## 🔥 Heat Equation
    
    ### Governing Equation:
    $$
    \\frac{\partial u}{\partial t} = \\alpha \\frac{\partial^2 u}{\partial x^2}
    $$
    
    ### Domain:
    - Space: $x \\in [0, L]$, $L = 1$
    - Time: $t \\in [0, T]$
    
    ### Analytical Solution (for Dirichlet BC):
    $$
    u(x,t) = \\sum_{n=1}^{\\infty} \\frac{2}{n\\pi}(1 - (-1)^n) 
    \\sin\\left(\\frac{n\\pi x}{L}\\right) e^{-\\alpha (n\\pi/L)^2 t}
    $$
    """)
    
    # Parameters explanation
    with st.expander("📖 Physical Interpretation"):
        st.markdown("""
        **Parameters:**
        - $u(x,t)$: Temperature distribution
        - $\\alpha$: Thermal diffusivity (m²/s)
        - Controls how fast heat spreads
        
        **Boundary Conditions:**
        1. **Dirichlet**: Fixed temperature at boundaries
           - $u(0,t) = u(L,t) = 0$
        2. **Neumann**: Insulated boundaries (no heat flux)
           - $\\frac{\partial u}{\partial x}(0,t) = \\frac{\partial u}{\partial x}(L,t) = 0$
        3. **Mixed**: One fixed, one insulated
        
        **Initial Conditions:**
        1. **Sinusoidal**: $u(x,0) = \\sin(\\pi x/L)$
        2. **Gaussian**: Localized heat pulse
        3. **Step**: Half-domain heating
        """)