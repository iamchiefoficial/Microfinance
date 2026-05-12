# Quick database fix - add approved_by column directly from Python
import pymysql

def add_approved_by_column():
    try:
        # Connect to MySQL with common settings
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='microfinance_db',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Add approved_by column
        cursor.execute("""
            ALTER TABLE loans ADD COLUMN approved_by VARCHAR(100) DEFAULT NULL
        """)
        
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
        print("✅ Database fixed successfully!")
        print("✅ approved_by column added")
        print("✅ existing loans updated")
        
        connection.close()
        print("✅ Your microfinance system is now ready!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    add_approved_by_column()
