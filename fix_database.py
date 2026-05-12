# Database Migration Script - Add missing approved_by column
import pymysql
from datetime import datetime

def add_approved_by_column():
    try:
        # Connect to MySQL
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='microfinance_db',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Add approved_by column to loans table if it doesn't exist
        try:
            cursor.execute("""
                ALTER TABLE loans 
                ADD COLUMN approved_by VARCHAR(50) AFTER current_stage
            """)
            print("✅ Added approved_by column to loans table")
        except Exception as e:
            if "Duplicate column name" not in str(e):
                print("⚠️ approved_by column already exists")
            else:
                print(f"❌ Error adding column: {e}")
        
        # Also check if we need to update existing loans
        cursor.execute("SELECT COUNT(*) FROM loans WHERE approved_by IS NULL")
        null_count = cursor.fetchone()[0]
        
        if null_count > 0:
            print(f"🔄 Updating {null_count} existing loans with approved_by values...")
            # Update existing loans to have approved_by based on current stage
            cursor.execute("""
                UPDATE loans 
                SET approved_by = CASE 
                    WHEN current_stage = 'loan_officer' THEN 'Loan Officer'
                    WHEN current_stage = 'loan_manager' THEN 'Loan Manager' 
                    WHEN current_stage = 'general_director' THEN 'General Director'
                    WHEN current_stage = 'managing_director' THEN 'Managing Director'
                    ELSE current_stage
                END
                WHERE approved_by IS NULL
            """)
            connection.commit()
            print(f"✅ Updated {null_count} loans with approved_by values")
        
        connection.close()
        print("✅ Database migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Database migration error: {e}")

if __name__ == '__main__':
    add_approved_by_column()
