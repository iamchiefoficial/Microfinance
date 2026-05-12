# Final working Flask test
print("=== FINAL FLASK TEST ===")

try:
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "<h1>✅ MICROFINANCE PLATFORM WORKING</h1><p>Server running successfully!</p>"
    
    print("✅ Flask app ready")
    print("🌐 Starting on http://127.0.0.1:5000")
    print("📱 Open browser to see success message")
    
    app.run(host='127.0.0.1', port=5000)
    
except ImportError:
    print("❌ Flask not installed. Run: pip install flask")
except Exception as e:
    print(f"❌ Error: {e}")
