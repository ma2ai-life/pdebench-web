#!/bin/bash
echo "Fixing all imports in the project..."

# List of files that might have import issues
FILES_TO_FIX=(
    "interfaces/streamlit/controllers/simulation_controller.py"
    "interfaces/streamlit/services/analytical_service.py"
    "interfaces/streamlit/services/numerical_service.py"
    "interfaces/streamlit/views/dashboard_view.py"
    "interfaces/streamlit/views/solution_view.py"
    "interfaces/streamlit/views/comparison_view.py"
)

for file in "${FILES_TO_FIX[@]}"; do
    if [ -f "$file" ]; then
        echo "Checking $file..."
        # Fix core.utils to core.solvers
        sed -i 's/from core\.utils\./from core\.solvers\./g' "$file"
        sed -i 's/from core\.utils import/from core\.solvers import/g' "$file"
        
        # Fix backend.utils to core.solvers
        sed -i 's/from backend\.utils\./from core\.solvers\./g' "$file"
        sed -i 's/from backend\.utils import/from core\.solvers import/g' "$file"
    fi
done

echo "✅ Import fixes applied"
