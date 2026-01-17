"""
Main dashboard view
"""

import streamlit as st
from frontend.views.solution_view import SolutionView
from frontend.views.comparison_view import ComparisonView
from frontend.state.session import get_solution_data

class DashboardView:
    @staticmethod
    def display_solutions_dashboard():
        """Display the main solutions dashboard"""
        st.markdown("## 📈 Solution Visualization")
        
        col1, col2 = st.columns(2)
        
        # Get solution data
        analytical_data = get_solution_data('analytical')
        numerical_data = get_solution_data('numerical')
        
        # Display solutions
        SolutionView.display(analytical_data, col1, "analytical")
        SolutionView.display(numerical_data, col2, "numerical")
    
    @staticmethod
    def display_comparison_dashboard(comparison_controller):
        """Display the comparison dashboard"""
        st.markdown("---")
        st.markdown("## 📊 Performance Comparison")
        
        # Get comparison data
        comparison_result = comparison_controller.compare_solutions()
        
        if comparison_result['success']:
            metrics = comparison_controller.calculate_comparison_metrics(comparison_result)
            summary = comparison_controller.get_comparison_summary(comparison_result, metrics)
            
            ComparisonView.display(comparison_result, metrics, summary)
        else:
            # Display status
            analytical_data = get_solution_data('analytical')
            numerical_data = get_solution_data('numerical')
            ComparisonView.display_status(
                analytical_data is not None,
                numerical_data is not None
            )
    
    @staticmethod
    def display_3d_visualization():
        """Display 3D visualization section"""
        st.markdown("---")
        st.markdown("## 🎭 3D Time Evolution")
        
        tab1, tab2 = st.tabs(["Analytical", "Numerical"])
        
        with tab1:
            analytical_data = get_solution_data('analytical')
            SolutionView.display_3d(analytical_data, "analytical")
        
        with tab2:
            numerical_data = get_solution_data('numerical')
            SolutionView.display_3d(numerical_data, "numerical")
