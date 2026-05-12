# Check if Python is available and show paths
import sys
import os

print("=== Python Installation Check ===")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path[0]}")
print(f"Current directory: {os.getcwd()}")

# Try to find Python installations
import subprocess
import glob

print("\n=== Searching for Python installations ===")
possible_paths = [
    r"C:\Python*\python.exe",
    r"C:\Program Files\Python*\python.exe", 
    r"C:\Program Files (x86)\Python*\python.exe",
    r"C:\Users\*\AppData\Local\Programs\Python*\python.exe"
]

found_pythons = []
for path_pattern in possible_paths:
    matches = glob.glob(path_pattern)
    for match in matches:
        found_pythons.append(match)

for python_path in found_pythons:
    print(f"Found: {python_path}")

if not found_pythons:
    print("No Python installations found in standard locations")
    print("\n=== Solutions ===")
    print("1. Install Python from https://www.python.org/downloads/")
    print("2. During installation, check 'Add Python to PATH'")
    print("3. Restart Command Prompt after installation")

input("\nPress Enter to exit...")
