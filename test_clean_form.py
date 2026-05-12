#!/usr/bin/env python3
"""
Test script to verify the clean group loan form displays correctly
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_complete import app

@app.route('/test_clean_form')
def test_clean_form():
    """Test route to verify clean group loan form"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Clean Form Test - Orethan Microfinance</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .test-section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
            .success { background: #d4edda; color: #155724; }
            .btn { background: #2c5aa6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px; display: inline-block; }
        </style>
    </head>
    <body>
        <h2>🧪 Clean Group Loan Form Test</h2>
        
        <div class="test-section success">
            <h3>✅ Clean Form Created</h3>
            <p>A clean group_loan_form.html has been created with only HTML (no explanatory text)</p>
            <a href="/group_loan_form" class="btn">Test Group Loan Form</a>
        </div>
        
        <div class="test-section">
            <h3>📋 What to Check:</h3>
            <ul>
                <li>Form displays without any code/text mixed in</li>
                <li>All 6 sections are visible</li>
                <li>Swahili labels are correct</li>
                <li>Submit button works</li>
                <li>Back button returns to dashboard</li>
            </ul>
        </div>
        
        <div class="test-section">
            <h3>🚀 Steps to Test:</h3>
            <ol>
                <li>Click "Test Group Loan Form" below</li>
                <li>You should see ONLY the Swahili loan application form</li>
                <li>No Python code or explanatory text should be visible</li>
                <li>Fill out some fields and click "WASILISHA MAOMBI"</li>
                <li>Should redirect back to client dashboard</li>
            </ol>
        </div>
        
        <hr>
        <p><strong>🎯 Ready to test!</strong> The clean form should now display properly.</p>
    </body>
    </html>
    '''

if __name__ == "__main__":
    print("🧪 Testing Clean Group Loan Form...")
    print("🌐 Access at: http://127.0.0.1:5000/test_clean_form")
    print("⏹ Press Ctrl+C to stop")
    print("=" * 50)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
