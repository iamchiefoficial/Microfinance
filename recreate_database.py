import sqlite3
import os

# Remove old database and create new one
if os.path.exists('microfinance.db'):
    os.remove('microfinance.db')
    print('✅ Removed old database')

conn = sqlite3.connect('microfinance.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'client',
    full_name TEXT,
    email TEXT,
    phone TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create loans table with all disbursement columns
cursor.execute('''
CREATE TABLE loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    purpose TEXT,
    status TEXT DEFAULT 'pending',
    current_stage TEXT DEFAULT 'loan_officer',
    term_months INTEGER DEFAULT 12,
    monthly_payment FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    disbursement_method TEXT,
    disbursement_date TIMESTAMP,
    disbursed_by INTEGER,
    disbursement_phone TEXT,
    disbursement_account TEXT,
    FOREIGN KEY (client_id) REFERENCES users (id)
)
''')

# Create group_loans table
cursor.execute('''
CREATE TABLE group_loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    applicant_full_name TEXT NOT NULL,
    applicant_national_id TEXT NOT NULL,
    group_chairperson TEXT NOT NULL,
    loan_amount FLOAT NOT NULL,
    loan_purpose TEXT,
    repayment_period INTEGER NOT NULL,
    status TEXT DEFAULT 'pending',
    current_stage TEXT DEFAULT 'loan_officer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES users (id)
)
''')

# Create payments table
cursor.execute('''
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    payment_method TEXT,
    payment_type TEXT,
    transaction_id TEXT UNIQUE,
    phone_number TEXT,
    account_number TEXT,
    bank_name TEXT,
    status TEXT DEFAULT 'pending',
    reference_number TEXT,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (loan_id) REFERENCES loans (id),
    FOREIGN KEY (client_id) REFERENCES users (id)
)
''')

# Create disbursements table
cursor.execute('''
CREATE TABLE disbursements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    method TEXT,
    phone_number TEXT,
    bank_name TEXT,
    account_number TEXT,
    transaction_id TEXT,
    disbursement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    confirmed_by INTEGER,
    FOREIGN KEY (loan_id) REFERENCES loans (id),
    FOREIGN KEY (client_id) REFERENCES users (id),
    FOREIGN KEY (confirmed_by) REFERENCES users (id)
)
''')

# Insert staff users
staff_users = [
    ('Admin', 'admin123', 'admin', 'System Administrator'),
    ('Loan Officer', 'mf@123', 'loan_officer', 'Loan Officer'),
    ('Loan Manager', 'mf@123', 'loan_manager', 'Loan Manager'),
    ('Managing Director', 'mf@123', 'managing_director', 'Managing Director'),
    ('General Director', 'mf@123', 'general_director', 'General Director')
]

for username, password, role, full_name in staff_users:
    cursor.execute('INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)',
                   (username, password, role, full_name))

conn.commit()
conn.close()

print('✅ Database recreated with all tables and columns!')
print('✅ Staff users created!')
print('✅ Disbursement columns added to loans table!')
