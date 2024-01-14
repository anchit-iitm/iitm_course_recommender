import os
import subprocess
import sys

def is_venv_created(venv_path):
    # Check if the virtual environment is already created
    return os.path.exists(os.path.join(venv_path, "bin" if sys.platform != "win32" else "Scripts", "activate"))

def create_venv(venv_path):
    # Create a virtual environment
    subprocess.run([sys.executable, "-m", "venv", venv_path])

def install_requirements(venv_path):
    # Install requirements from requirements.txt in the virtual environment
    subprocess.run([os.path.join(venv_path, "bin", "pip"), "install", "-r", "requirements.txt"])

def is_log_folder_present(target_folder):
    # Check if the 'log' folder is present
    return os.path.exists(os.path.join(target_folder, "log"))

def run_script(script_path):
    # Run a Python script
    subprocess.run([sys.executable, script_path])

if __name__ == "__main__":
    # Specify the target folder and virtual environment name
    target_folder = os.path.dirname(os.path.abspath(__file__))
    venv_name = "venv"  # Use a common convention like "venv"

    # Full path to the virtual environment
    venv_path = os.path.join(target_folder, venv_name)

    # Check if the virtual environment is already created
    if not is_venv_created(venv_path):
        # Create and activate the virtual environment
        create_venv(venv_path)
        install_requirements(venv_path)
    
    # Check if the 'log' folder is present
    if not is_log_folder_present(target_folder):
        # Run init_app.py
        init_app_script = "init_app.py"
        run_script(os.path.join(target_folder, init_app_script))

    # Run app.py
    app_script = "app.py"
    run_script(os.path.join(target_folder, app_script))
