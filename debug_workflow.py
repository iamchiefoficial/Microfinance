#!/usr/bin/env python3
"""
Debug script to check the loan approval workflow
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app_fixed_workflow import app, db, User, Loan
    from datetime import datetime
    
    print("🔍 Debugging Loan Approval Workflow...")
    
    with app.app_context():
        # Check all users
        print("\n📋 All Users:")
        users = User.query.all()
        for user in users:
            print(f"  - {user.username} (Role: {user.role})")
        
        # Check all loans
        print("\n📋 All Loans:")
        loans = Loan.query.all()
        if not loans:
            print("  ❌ No loans found in database!")
            print("  💡 A client needs to apply for a loan first!")
        else:
            for loan in loans:
                print(f"  - Loan #{loan.id}: ${loan.amount} for {loan.purpose}")
                print(f"    Status: {loan.status}")
                print(f"    Current Stage: {loan.current_stage}")
                print(f"    Client: {loan.client.username if loan.client else 'Unknown'}")
                print(f"    Created: {loan.created_at}")
                print()
        
        # Check loan officer pending loans
        print("\n🔍 Loan Officer Pending Loans:")
        loan_officer = User.query.filter_by(username='Loan Officer').first()
        if loan_officer:
            pending_loans = Loan.query.filter_by(current_stage='loan_officer', loan_officer_approved=False).all()
            print(f"  Found {len(pending_loans)} pending loans for Loan Officer")
            for loan in pending_loans:
                print(f"    - Loan #{loan.id}: ${loan.amount}")
        else:
            print("  ❌ Loan Officer account not found!")
        
        # Create a test loan if none exist
        if not loans:
            print("\n🚀 Creating a test loan...")
            client = User.query.filter_by(role='client').first()
            if client:
                test_loan = Loan(
                    client_id=client.id,
                    amount=1000.0,
                    purpose="Test Business Loan",
                    term_months=12,
                    interest_rate=10.0,
                    monthly_payment=100.0,
                    status='pending',
                    current_stage='loan_officer',
                    created_at=datetime.now()
                )
                db.session.add(test_loan)
                db.session.commit()
                print(f"  ✅ Created test loan #{test_loan.id} for client {client.username}")
                print("  🎯 Now login as 'Loan Officer' to see this loan!")
            else:
                print("  ❌ No client account found! Please register a client first.")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
