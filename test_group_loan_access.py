#!/usr/bin/env python3
"""
Test script to verify group loan form accessibility
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_fixed_workflow import app

def test_group_loan_routes():
    """Test if group loan routes are accessible"""
    print("🧪 Testing Group Loan Route Accessibility...")
    
    with app.test_client() as client:
        # Test 1: Check if apply_group_loan route exists
        print("\n1️⃣ Testing /apply_group_loan route...")
        response = client.get('/apply_group_loan', follow_redirects=True)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ Route exists - redirecting to login (expected)")
            print("   💡 This means you need to login first")
        elif response.status_code == 200:
            print("   ✅ Route accessible - form should be visible")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
        
        # Test 2: Check if login route works
        print("\n2️⃣ Testing /login route...")
        response = client.get('/login')
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Login route working")
        else:
            print(f"   ❌ Login route error: {response.status_code}")
        
        # Test 3: Check if client_dashboard route exists
        print("\n3️⃣ Testing /client_dashboard route...")
        response = client.get('/client_dashboard', follow_redirects=True)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ Route exists - redirecting to login (expected)")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
        
        # Test 4: Check if template exists
        print("\n4️⃣ Checking template files...")
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'group_loan_form.html')
        if os.path.exists(template_path):
            print(f"   ✅ group_loan_form.html exists ({os.path.getsize(template_path)} bytes)")
        else:
            print(f"   ❌ group_loan_form.html not found")
        
        print("\n🎯 How to Access Group Loan Form:")
        print("   1. Start Flask server: python app_fixed_workflow.py")
        print("   2. Go to: http://127.0.0.1:9000")
        print("   3. Login as a CLIENT account")
        print("   4. Click 'Apply for Group Loan' button")
        print("   5. OR directly visit: http://127.0.0.1:9000/apply_group_loan")

if __name__ == "__main__":
    test_group_loan_routes()
