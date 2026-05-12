"""
Simple startup script for Orethan Microfinance Platform
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🚀 Starting Orethan Microfinance Platform...")
    print("🌐 Access at: http://127.0.0.1:9000")
    print("⏹ Press Ctrl+C to stop")
    print("=" * 50)
    
    # Import and run the app
    from app_fixed_workflow import app
    app.run(host='0.0.0.0', port=9000, debug=True)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure all required packages are installed:")
    print("   pip install flask flask-sqlalchemy pymysql werkzeug waitress")
    
except Exception as e:
    print(f"❌ Error starting application: {e}")
    import traceback
    traceback.print_exc()
