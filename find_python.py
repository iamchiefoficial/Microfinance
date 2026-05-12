# Find Python installation and provide startup commands
import os
import glob
import subprocess

print("=== Python Installation Finder ===")

# Search for Python installations
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

if found_pythons:
    print("Found Python installations:")
    for i, python_path in enumerate(found_pythons, 1):
        print(f"{i}. {python_path}")
    
    # Use first found Python
    python_exe = found_pythons[0]
    print(f"\n=== Using: {python_exe} ===")
    
    # Create startup commands
    print("Use these commands:")
    print(f'1. Install deps: "{python_exe}" -m pip install -r requirements.txt')
    print(f'2. Setup database: mysql -u root -p < database_setup.sql')
    print(f'3. Create admin: "{python_exe}" admin_setup.py')
    print(f'4. Start app: "{python_exe}" app.py')
    
else:
    print("❌ No Python found!")
    print("\n=== SOLUTIONS ===")
    print("1. Install Python from: https://www.python.org/downloads/")
    print("2. During installation: ✅ Check 'Add Python to PATH'")
    print("3. Restart Command Prompt after installation")
    print("4. Look for 'python.exe' in:")
    print("   - C:\\Python39\\")
    print("   - C:\\Program Files\\Python39\\")
    print("   - C:\\Users\\yourname\\AppData\\Local\\Programs\\Python\\Python39\\")
