#!/usr/bin/env python3
"""
Script to create GroupLoan table in the database
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_fixed_workflow import app, db, GroupLoan

def create_group_loan_table():
    """Create the GroupLoan table if it doesn't exist"""
    with app.app_context():
        try:
            # Create all tables (this will create GroupLoan table)
            db.create_all()
            print("✅ GroupLoan table created successfully!")
            
            # Check if table exists and has the right structure
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'group_loans' in tables:
                print("✅ 'group_loans' table found in database")
                
                # Get column information
                columns = inspector.get_columns('group_loans')
                print(f"📊 Table has {len(columns)} columns:")
                for column in columns:
                    print(f"   - {column['name']}: {column['type']}")
            else:
                print("❌ 'group_loans' table not found")
                
        except Exception as e:
            print(f"❌ Error creating GroupLoan table: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("🔧 Creating GroupLoan table...")
    success = create_group_loan_table()
    
    if success:
        print("🎉 GroupLoan table setup completed!")
        print("💡 You can now use the group loan application feature.")
    else:
        print("❌ Failed to create GroupLoan table.")
        sys.exit(1)
