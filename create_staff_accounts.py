# Create staff accounts with role names and mf@123 password
from werkzeug.security import generate_password_hash
import pymysql

def create_staff_accounts():
    try:
        # Connect to MySQL
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='microfinance_db'
        )
        cursor = connection.cursor()
        
        # Staff accounts with role names as usernames and mf@123 password
        staff_accounts = [
            ('System Administrator', 'admin@microfinance.com', 'ADMIN001', 'Administrator', 'admin'),
            ('General Director', 'director@microfinance.com', 'DIR001', 'General Director', 'general_director'),
            ('Managing Director', 'md@microfinance.com', 'MD001', 'Managing Director', 'managing_director'),
            ('Loan Manager', 'lm@microfinance.com', 'LM001', 'Loan Manager', 'loan_manager'),
            ('Loan Officer', 'lo@microfinance.com', 'LO001', 'Loan Officer', 'loan_officer')
        ]
        
        password_hash = generate_password_hash('mf@123')
        
        for username, email, national_id, occupation, role in staff_accounts:
            # Check if user already exists
            cursor.execute("SELECT id FROM user WHERE username = %s", (username,))
            if cursor.fetchone():
                print(f"✅ Staff account '{username}' already exists")
                continue
            
            # Insert staff account
            cursor.execute("""
                INSERT INTO user (username, password_hash, full_name, email, national_id, occupation, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (username, password_hash, username, email, national_id, occupation, role))
            
            print(f"✅ Created staff account: {username}")
        
        connection.commit()
        print("\n🎉 All staff accounts created successfully!")
        print("\n📋 Staff Login Credentials:")
        print("Username: System Administrator | Password: mf@123")
        print("Username: General Director | Password: mf@123")
        print("Username: Managing Director | Password: mf@123")
        print("Username: Loan Manager | Password: mf@123")
        print("Username: Loan Officer | Password: mf@123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure MySQL is running and database 'microfinance_db' exists")
    finally:
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == '__main__':
    create_staff_accounts()
