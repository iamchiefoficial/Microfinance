# Complete diagnostic and fix script
import sys
import os
import subprocess

print("=== MICROFINANCE PLATFORM COMPLETE FIX ===")

# Step 1: Check Python environment
print(f"Python: {sys.version}")
print(f"Directory: {os.getcwd()}")

# Step 2: Install all required packages
packages = [
    'flask',
    'flask-sqlalchemy', 
    'pymysql',
    'werkzeug'
]

print("\n=== Installing Packages ===")
for package in packages:
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {package} installed successfully")
        else:
            print(f"❌ {package} failed: {result.stderr}")
    except Exception as e:
        print(f"❌ {package} error: {e}")

# Step 3: Create minimal working Flask app
print("\n=== Creating Minimal Flask App ===")
try:
    from flask import Flask, request, render_template, redirect, url_for, session
    from flask_sqlalchemy import SQLAlchemy
    from werkzeug.security import generate_password_hash
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_key_12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use SQLite for testing
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy(app)
    
    @app.route('/')
    def index():
        return '''
        <h1>Microfinance Platform</h1>
        <h2>✅ Application Working!</h2>
        <p>Flask server is running successfully</p>
        <p><a href="/login">Go to Login</a></p>
        '''
    
    @app.route('/login')
    def login():
        return '''
        <h1>Login Page</h1>
        <form method="post" action="/submit">
            <input type="text" name="username" placeholder="Username" required><br><br>
            <input type="password" name="password" placeholder="Password" required><br><br>
            <button type="submit">Login</button>
        </form>
        '''
    
    @app.route('/submit', methods=['POST'])
    def submit():
        username = request.form.get('username')
        return f"<h2>Hello {username}!</h2><p>Form submission working!</p>"
    
    print("✅ Minimal Flask app created")
    print("🌐 Starting server...")
    print("📱 Open browser to: http://127.0.0.1:5000")
    print("\nThis is a working test version!")
    print("If this works, the issue is with MySQL/database setup")
    
    app.run(host='127.0.0.1', port=5000, debug=False)
    
except Exception as e:
    print(f"❌ Critical error: {e}")
    print("\n=== Manual Steps ===")
    print("1. Install packages manually:")
    for pkg in packages:
        print(f"   pip install {pkg}")
    print("2. Try this simple app: python comprehensive_fix.py")
