"""
Controller for managing comparisons
"""

import numpy as np
from backend.utils.comparison import compare_solutions
from frontend.state.session import get_solution_data

class ComparisonController:
    @staticmethod
    def compare_solutions():
        """Compare analytical and numerical solutions"""
        analytical_data = get_solution_data('analytical')
        numerical_data = get_solution_data('numerical')
        
        if analytical_data is None or numerical_data is None:
            return {
                'success': False,
                'error': 'Both analytical and numerical solutions required',
                'data': None
            }
        
        try:
            error, common_x, grids_match = compare_solutions(
                analytical_data, numerical_data
            )
            
            return {
                'success': True,
                'data': {
                    'error': error,
                    'common_x': common_x,
                    'grids_match': grids_match,
                    'analytical_time': analytical_data['time'],
                    'numerical_time': numerical_data['time'],
                    'analytical_params': analytical_data['params'],
                    'numerical_params': numerical_data['params']
                },
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'data': None
            }
    
    @staticmethod
    def calculate_comparison_metrics(comparison_data):
        """Calculate metrics from comparison data"""
        if not comparison_data['success']:
            return None
        
        data = comparison_data['data']
        
        metrics = {
            'max_error': float(np.max(data['error'])),
            'mean_error': float(np.mean(data['error'])),
            'rmse': float(np.sqrt(np.mean(data['error']**2))),
            'analytical_time': data['analytical_time'],
            'numerical_time': data['numerical_time']
        }
        
        # Calculate speedup
        if data['analytical_time'] > 0:
            metrics['speedup'] = data['numerical_time'] / data['analytical_time']
        else:
            metrics['speedup'] = 0
        
        return metrics
    
    @staticmethod
    def get_comparison_summary(comparison_data, metrics):
        """Get a summary text for comparison"""
        if not comparison_data['success']:
            return "Comparison not available"
        
        data = comparison_data['data']
        
        if data['grids_match']:
            summary = f"""
            **Direct Comparison:**
            - Grids match: {data['analytical_params']['nx']} × {data['analytical_params']['nt']}
            - Analytical time: {data['analytical_time']:.6f}s
            - Numerical time: {data['numerical_time']:.6f}s
            - Speedup: {metrics['speedup']:.1f}x
            - Max error: {metrics['max_error']:.6f}
            """
        else:
            summary = f"""
            **Interpolated Comparison:**
            - Analytical grid: {data['analytical_params']['nx']} × {data['analytical_params']['nt']}
            - Numerical grid: {data['numerical_params']['nx']} × {data['numerical_params']['nt']}
            - Compared on common grid of {len(data['common_x'])} points
            - Max error: {metrics['max_error']:.6f}
            """
        
        return summary
