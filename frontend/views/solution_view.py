"""
View for displaying a single solution
"""

import streamlit as st
from frontend.components.plots import create_2d_plot, create_3d_plot
from frontend.components.metrics import calculate_solution_metrics, display_solution_metrics

class SolutionView:
    @staticmethod
    def display(solution_data, column, solution_type="Solution"):
        """Display a solution in a column"""
        if solution_data is None:
            SolutionView._display_placeholder(column, solution_type)
            return
        
        with column:
            # Title
            if solution_type == "analytical":
                title = f"🔍 Analytical Solution"
                color = 'red'
                icon = "🔍"
            else:
                title = f"🧮 Numerical Solution"
                color = 'green'
                icon = "🧮"
            
            st.markdown(f"### {icon} {title}")
            
            # 2D Plot
            fig_2d = create_2d_plot(
                u=solution_data['u'],
                x=solution_data['x'],
                t=solution_data['t'],
                title=f"{solution_type.capitalize()} (α={solution_data['params']['alpha']})",
                color=color
            )
            st.plotly_chart(fig_2d, use_container_width=True)
            
            # Metrics
            metrics = calculate_solution_metrics(
                solution_data['u'],
                solution_data['x']
            )
            display_solution_metrics(
                metrics,
                solution_data['time'],
                title="Performance Metrics"
            )
            
            # Parameters
            with st.expander("📋 View Parameters"):
                st.json(solution_data['params'])
    
    @staticmethod
    def _display_placeholder(column, solution_type):
        """Display placeholder when no solution available"""
        with column:
            if solution_type == "analytical":
                message = "Click 'Run Analytical' to compute solution"
                icon = "🔍"
            else:
                message = "Click 'Run Numerical' to compute solution"
                icon = "🧮"
            
            st.info(f"{icon} {message}")
            
            # Show current settings preview
            st.markdown("**Current Settings Preview:**")
            st.code("""
            Parameters will appear here
            after running simulation
            """, language="text")
    
    @staticmethod
    def display_3d(solution_data, solution_type):
        """Display 3D visualization"""
        if solution_data is None:
            st.info(f"Run {solution_type} solution to see 3D visualization")
            return
        
        if solution_type == "analytical":
            title = f"Analytical 3D View (Nx={len(solution_data['x'])})"
            colorscale = 'Viridis'
        else:
            title = f"Numerical 3D View (Nx={len(solution_data['x'])})"
            colorscale = 'Plasma'
        
        fig_3d = create_3d_plot(
            solution_data['u'],
            solution_data['x'],
            solution_data['t'],
            title=title,
            colorscale=colorscale
        )
        st.plotly_chart(fig_3d, use_container_width=True)
