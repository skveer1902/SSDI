import subprocess
import os

# Start backend
backend_path = os.path.join("backend", "app")
backend_command = ["uvicorn", "main:app", "--reload"]

# Start frontend
frontend_path = "frontend"
frontend_command = ["npm", "start"]

# Launch backend
backend = subprocess.Popen(backend_command, cwd=backend_path)

# Launch frontend
frontend = subprocess.Popen(frontend_command, cwd=frontend_path)

# (Optional) Wait for both to end
backend.wait()
frontend.wait()