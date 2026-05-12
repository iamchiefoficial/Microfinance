# Comprehensive diagnostic and startup script
import sys
import os

print("=== Microfinance Platform Diagnostic ===")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Test imports
try:
    import flask
    print("✅ Flask imported successfully")
except ImportError as e:
    print(f"❌ Flask import failed: {e}")
    
try:
    import flask_sqlalchemy
    print("✅ Flask-SQLAlchemy imported successfully")
except ImportError as e:
    print(f"❌ Flask-SQLAlchemy import failed: {e}")

try:
    import pymysql
    print("✅ PyMySQL imported successfully")
except ImportError as e:
    print(f"❌ PyMySQL import failed: {e}")

try:
    from werkzeug.security import generate_password_hash
    print("✅ Werkzeug imported successfully")
except ImportError as e:
    print(f"❌ Werkzeug import failed: {e}")

print("\n=== Starting Flask App ===")

try:
    # Simple Flask app for testing
    from flask import Flask, render_template
    
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "<h1>Microfinance Platform - Working!</h1><p>✅ Flask app is running successfully</p>"
    
    @app.route('/test')
    def test():
        return "<h1>Test Page</h1><p>All systems operational</p>"
    
    print("✅ Flask app created successfully")
    print("🌐 Starting server on http://127.0.0.1:5000")
    print("📱 Open browser to: http://127.0.0.1:5000")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
    
except Exception as e:
    print(f"❌ Failed to start Flask app: {e}")
    print("\n=== Troubleshooting ===")
    print("1. Install missing packages:")
    print("   pip install flask flask-sqlalchemy pymysql werkzeug")
    print("2. Check Python installation")
    print("3. Try running with: python debug_app.py")
    
input("\nPress Enter to exit...")
