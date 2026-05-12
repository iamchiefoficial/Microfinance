#!/usr/bin/env python3
"""
Test script to verify logo display in templates
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_complete import app

@app.route('/test_logo')
def test_logo():
    """Test route to verify logo display"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Logo Test - Orethan Microfinance</title>
    </head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>🧪 Logo Display Test</h2>
        
        <h3>Static File Test:</h3>
        <img src="/static/images/orethan_logo.png" alt="Orethan Logo" style="height: 60px; border: 1px solid #ccc;">
        <p>✅ Static file should display above</p>
        
        <h3>Template Test:</h3>
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
            <img src="{{ url_for('static', filename='images/orethan_logo.png') }}" alt="Orethan Logo" style="height: 50px;">
            <div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #2c5aa6; margin: 0;">ORETHAN MICROFINANCE</div>
                <div style="font-size: 0.9rem; color: #666; margin: 5px 0;">Professional Financial Services</div>
            </div>
        </div>
        <p>✅ Template logo should display above</p>
        
        <h3>Navigation:</h3>
        <ul>
            <li><a href="/login">Login Page</a></li>
            <li><a href="/register">Register Page</a></li>
            <li><a href="/dashboard">Dashboard (requires login)</a></li>
        </ul>
        
        <hr>
        <p><strong>🎯 If logos display correctly above, everything is working!</strong></p>
    </body>
    </html>
    '''

if __name__ == "__main__":
    print("🧪 Starting Logo Display Test...")
    print("🌐 Access at: http://127.0.0.1:5000/test_logo")
    print("⏹ Press Ctrl+C to stop")
    print("=" * 50)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
