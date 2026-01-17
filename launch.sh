#!/bin/bash
# PDEBench Launcher

echo "Starting PDEBench..."

# Check if in correct directory
if [ ! -d "interfaces/streamlit" ]; then
    echo "Error: Please run from project root directory"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate
    pip install -r interfaces/streamlit/requirements.txt
else
    source venv/bin/activate
fi

# Run the app
echo "Launching PDEBench..."
cd interfaces/streamlit
streamlit run app.py
