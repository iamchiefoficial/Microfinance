#!/usr/bin/env python3
"""
Direct test to show group loan form without authentication
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_fixed_workflow import app
from flask import render_template

@app.route('/test_group_loan')
def test_group_loan():
    """Test route to show group loan form directly"""
    return render_template('group_loan_form.html')

if __name__ == "__main__":
    print("🚀 Starting Direct Group Loan Test...")
    print("🌐 Access at: http://127.0.0.1:9000/test_group_loan")
    print("⏹ Press Ctrl+C to stop")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=9000, debug=True)
