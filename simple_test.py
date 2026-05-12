# Simple Flask test to isolate the issue
print("Starting simple Flask test...")

try:
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return "<h1>Flask Working!</h1><p>Basic test successful</p>"
    
    print("✅ Flask app created")
    print("🌐 Starting on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nSolutions:")
    print("1. Install Flask: pip install flask")
    print("2. Check Python installation")
    print("3. Try: python simple_test.py")

input("Press Enter to exit...")
