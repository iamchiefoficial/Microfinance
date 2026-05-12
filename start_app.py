#!/usr/bin/env python3
"""
Startup script for Microfinance Application
Finds the correct Python executable and starts the app
"""

import sys
import os
import subprocess
import shutil

def find_python():
    """Find the correct Python executable"""
    # Try different Python commands
    python_commands = ['python', 'python3', 'py', 'py -3']
    
    for cmd in python_commands:
        try:
            # Try to get Python version
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print(f"✅ Found Python: {result.stdout.strip()}")
                return cmd
        except:
            continue
    
    return None

def start_application():
    """Start the microfinance application"""
    print("🚀 Starting Orethan Microfinance Platform...")
    
    # Find Python executable
    python_cmd = find_python()
    if not python_cmd:
        print("❌ Python not found. Please install Python 3.7 or higher.")
        return False
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📁 Working directory: {script_dir}")
    
    # Start the application
    try:
        print(f"🐍 Starting application with: {python_cmd}")
        print("🌐 Application will be available at: http://127.0.0.1:9000")
        print("⏹ Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Run the app
        subprocess.run([python_cmd, 'app_fixed_workflow.py'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting application: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = start_application()
    if not success:
        sys.exit(1)
