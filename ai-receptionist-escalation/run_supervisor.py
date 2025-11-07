"""
Supervisor UI Launcher
Handles Python path and starts the Flask web application
"""
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now import and run
from supervisor.app import app

if __name__ == '__main__':
    print("🌐 Starting Supervisor Web UI...")
    print(f"📁 Project root: {project_root}")
    print("🔗 Visit: http://localhost:5000")
    print("Press Ctrl+C to stop")
    app.run(debug=True, port=5000, host='127.0.0.1')
