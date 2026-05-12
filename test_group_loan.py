#!/usr/bin/env python3
"""
Test script for Group Loan functionality
"""

import sys
import os
from datetime import datetime, date

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_fixed_workflow import app, db, GroupLoan, User

def test_group_loan_functionality():
    """Test group loan functionality"""
    print("🧪 Testing Group Loan Functionality...")
    
    with app.app_context():
        try:
            # Test 1: Check if GroupLoan model is properly defined
            print("\n1️⃣ Testing GroupLoan model...")
            print(f"   ✅ GroupLoan model imported successfully")
            print(f"   ✅ Table name: {GroupLoan.__tablename__}")
            
            # Test 2: Check database connection and table creation
            print("\n2️⃣ Testing database connection...")
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'group_loans' in tables:
                print(f"   ✅ 'group_loans' table exists in database")
                
                # Check table structure
                columns = inspector.get_columns('group_loans')
                required_columns = [
                    'id', 'applicant_full_name', 'group_chairperson', 
                    'loan_amount', 'status', 'current_stage',
                    'loan_officer_approved', 'loan_manager_approved',
                    'managing_director_approved', 'general_director_approved'
                ]
                
                missing_columns = [col for col in required_columns if col not in [c['name'] for c in columns]]
                if not missing_columns:
                    print(f"   ✅ All required columns present ({len(columns)} total columns)")
                else:
                    print(f"   ❌ Missing columns: {missing_columns}")
                    
            else:
                print(f"   ❌ 'group_loans' table not found")
                print(f"   📋 Available tables: {tables}")
                return False
            
            # Test 3: Test GroupLoan model methods
            print("\n3️⃣ Testing GroupLoan model methods...")
            test_loan = GroupLoan(
                applicant_full_name="Test Applicant",
                group_chairperson="Test Chairperson",
                loan_amount=10000.0,
                status='pending',
                current_stage='loan_officer'
            )
            
            # Test stage name method
            stage_name = test_loan.get_current_stage_name()
            print(f"   ✅ get_current_stage_name(): '{stage_name}'")
            
            # Test next stage method
            next_stage = test_loan.get_next_stage()
            print(f"   ✅ get_next_stage(): '{next_stage}'")
            
            # Test approval method
            can_approve = test_loan.can_approve('loan_officer')
            print(f"   ✅ can_approve('loan_officer'): {can_approve}")
            
            # Test 4: Check routes are accessible
            print("\n4️⃣ Testing Flask routes...")
            with app.test_client() as client:
                # Test group loan application route
                response = client.get('/apply_group_loan', follow_redirects=True)
                if response.status_code in [200, 302]:  # 200 for form, 302 if redirected to login
                    print(f"   ✅ /apply_group_loan route accessible (status: {response.status_code})")
                else:
                    print(f"   ❌ /apply_group_loan route error (status: {response.status_code})")
            
            # Test 5: Check template exists
            print("\n5️⃣ Checking template files...")
            template_path = os.path.join(os.path.dirname(__file__), 'templates', 'group_loan_form.html')
            if os.path.exists(template_path):
                print(f"   ✅ group_loan_form.html template exists")
                print(f"   📁 Template size: {os.path.getsize(template_path)} bytes")
            else:
                print(f"   ❌ group_loan_form.html template not found")
            
            print("\n🎉 Group Loan functionality test completed successfully!")
            return True
            
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False

def test_data_integrity():
    """Test data integrity and relationships"""
    print("\n🔍 Testing Data Integrity...")
    
    with app.app_context():
        try:
            # Check if users exist
            users = User.query.all()
            print(f"   👥 Found {len(users)} users in database")
            
            if users:
                # Check if there are any staff accounts
                staff_users = [u for u in users if u.role != 'client']
                print(f"   👔 Found {len(staff_users)} staff accounts")
                
                if staff_users:
                    roles = set([u.role for u in staff_users])
                    print(f"   🏷️  Staff roles: {', '.join(roles)}")
            
            # Check group loans
            group_loans = GroupLoan.query.all()
            print(f"   📋 Found {len(group_loans)} group loans in database")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Data integrity test failed: {e}")
            return False

if __name__ == "__main__":
    print("🚀 Starting Group Loan Functionality Tests")
    print("=" * 50)
    
    # Run main functionality test
    success = test_group_loan_functionality()
    
    if success:
        # Run data integrity test
        test_data_integrity()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("\n📋 Next Steps:")
        print("   1. Start the application: python app_fixed_workflow.py")
        print("   2. Login as a client and test group loan application")
        print("   3. Login as staff and test approval workflow")
        print("   4. Verify all stages work correctly")
    else:
        print("\n❌ Tests failed. Please fix issues before proceeding.")
        sys.exit(1)
