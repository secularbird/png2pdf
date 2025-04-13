import os
import shutil
import subprocess

# Define project metadata
project_name = "png2pdf"
main_script = "main.py"
output_dir = "dist"
build_dir = "build"

def clean_previous_builds():
    """Remove previous build artifacts."""
    for folder in [output_dir, build_dir]:
        if os.path.exists(folder):
            shutil.rmtree(folder)

def build_executable():
    """Build the application using PyInstaller."""
    subprocess.run([
        "pyinstaller",
        "--onefile",  # Create a single executable
        "--noconsole",  # Suppress the console window
        f"--name={project_name}",  # Name of the executable
        f"--distpath={output_dir}",  # Output directory
        f"--workpath={build_dir}",  # Temporary build directory
        main_script
    ], check=True)

def main():
    try:
        print("Cleaning up previous builds...")
        clean_previous_builds()
        print("Building the application...")
        build_executable()
        print(f"Executable created successfully in {os.path.abspath(output_dir)}")
    except Exception as e:
        print(f"Error during build: {e}")

if __name__ == "__main__":
    main()
