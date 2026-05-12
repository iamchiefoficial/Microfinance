#!/usr/bin/env python3
"""
Database Update Script for Microfinance Platform
This script updates the database schema to include the new workflow columns
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app_fixed_workflow import app, db, User, Loan
    from datetime import datetime
    
    print("🔄 Starting database update...")
    
    with app.app_context():
        try:
            # Drop and recreate all tables (clean slate)
            print("📋 Dropping existing tables...")
            db.drop_all()
            print("✅ Tables dropped successfully")
            
            # Create all tables with new schema
            print("📋 Creating tables with new workflow schema...")
            db.create_all()
            print("✅ Tables created successfully")
            
            # Create staff accounts
            print("👥 Creating staff accounts...")
            
            staff_users = [
                {'username': 'Loan Officer', 'password': 'mf@123', 'role': 'loan_officer', 'full_name': 'John Officer'},
                {'username': 'Loan Manager', 'password': 'mf@123', 'role': 'loan_manager', 'full_name': 'Jane Manager'},
                {'username': 'Managing Director', 'password': 'mf@123', 'role': 'managing_director', 'full_name': 'Bob Director'},
                {'username': 'General Director', 'password': 'mf@123', 'role': 'general_director', 'full_name': 'Alice General'},
                {'username': 'System Administrator', 'password': 'mf@123', 'role': 'admin', 'full_name': 'Admin User'}
            ]
            
            for staff in staff_users:
                existing = User.query.filter_by(username=staff['username']).first()
                if not existing:
                    new_user = User(
                        username=staff['username'],
                        password=generate_password_hash(staff['password']),
                        role=staff['role'],
                        full_name=staff['full_name'],
                        email=f"{staff['username'].lower().replace(' ', '_')}@microfinance.com",
                        created_at=datetime.now()
                    )
                    db.session.add(new_user)
                    print(f"  ✅ Created {staff['username']}")
            
            db.session.commit()
            print("✅ Staff accounts created successfully!")
            
            # Verify loan table has new columns
            print("🔍 Verifying loan table schema...")
            loan_columns = [column.name for column in Loan.__table__.columns]
            required_columns = [
                'loan_officer_approved', 'loan_officer_id', 'loan_officer_approved_at',
                'loan_manager_approved', 'loan_manager_id', 'loan_manager_approved_at',
                'managing_director_approved', 'managing_director_id', 'managing_director_approved_at',
                'general_director_approved', 'general_director_id', 'general_director_approved_at',
                'rejection_reason', 'rejected_by', 'rejected_at', 'current_stage'
            ]
            
            missing_columns = [col for col in required_columns if col not in loan_columns]
            if missing_columns:
                print(f"❌ Missing columns: {missing_columns}")
            else:
                print("✅ All workflow columns are present!")
            
            print("\n🎉 Database update completed successfully!")
            print("📊 Database schema is now ready for multi-level approval workflow")
            print("🔑 Staff login credentials:")
            for staff in staff_users:
                print(f"   {staff['username']}: mf@123")
            
        except Exception as e:
            print(f"❌ Error during database update: {e}")
            import traceback
            traceback.print_exc()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure app_fixed_workflow.py is in the same directory")
    sys.exit(1)

if __name__ == '__main__':
    pass
