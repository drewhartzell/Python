from cx_Freeze import setup, Executable

# List all extra Python scripts
extra_scripts = ["biometrics load v2.py", "enrollment load v2.py", "point solution load.py", "pharmacy load v2.py", "medical load v2.py"]

# List of images and any additional required files
extra_files = ["Inn. Logo (no back).png", "X Text v2.png", "Mapping Logo.ico"]

# Combine everything
include_files = extra_scripts + extra_files

# Options for cx_Freeze
options = {
    "build_exe": {
        "packages": ["customtkinter", "pandas", "openpyxl"],  # Add necessary libraries
        "include_files": include_files,  # Include extra scripts and images
        "excludes": ["unittest"],  # Exclude unnecessary libraries
    }
}

# Define the executable
exe = Executable(
    script="Modern UI.py",  # Your main script
    target_name="Mapping Tool.exe",  # Output executable name
    icon="Mapping Logo.ico",  # Icon file (must be .ico format)
    base="Win32GUI"  # Removes console window (for GUI apps)
)

# Setup configuration
setup(
    name="MyApp",
    version="1.0",
    description="Auto-Mapping Tool",
    options=options,
    executables=[exe],
)
