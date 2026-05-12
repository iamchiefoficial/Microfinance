# Python script to add approved_by column to database
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
        
        # Add approved_by column to loans table
        try:
            cursor.execute("""
                ALTER TABLE loans 
                ADD COLUMN approved_by VARCHAR(100) DEFAULT NULL
            """)
            connection.commit()
            print("✅ Successfully added approved_by column to loans table")
            
        except Exception as e:
            if "Duplicate column name" not in str(e):
                print("⚠️ approved_by column already exists")
            else:
                print(f"❌ Error adding column: {e}")
        
        # Update existing loans to set approved_by based on current stage
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
        print("✅ Updated existing loans with approved_by values")
        
        connection.close()
        print("✅ Database schema updated successfully!")
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == '__main__':
    add_approved_by_column()
