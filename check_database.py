import sqlite3

conn = sqlite3.connect('microfinance.db')
cursor = conn.cursor()

# Check current columns
cursor.execute('PRAGMA table_info(loans)')
columns = cursor.fetchall()
print('Current columns in loans table:')
for col in columns:
    print(f'  - {col[1]} ({col[2]})')

# Add missing columns
columns_to_add = [
    ('disbursement_method', 'TEXT'),
    ('disbursement_date', 'TIMESTAMP'),
    ('disbursed_by', 'INTEGER'),
    ('disbursement_phone', 'TEXT'),
    ('disbursement_account', 'TEXT')
]

print('\nAdding missing columns...')
for col_name, col_type in columns_to_add:
    try:
        cursor.execute(f'ALTER TABLE loans ADD COLUMN {col_name} {col_type}')
        print(f'✅ Added column: {col_name}')
    except Exception as e:
        if 'duplicate column' in str(e).lower():
            print(f'⚠️ Column {col_name} already exists')
        else:
            print(f'❌ Error adding {col_name}: {e}')

conn.commit()

# Verify columns were added
print('\nUpdated columns in loans table:')
cursor.execute('PRAGMA table_info(loans)')
columns = cursor.fetchall()
for col in columns:
    print(f'  - {col[1]} ({col[2]})')

# Create payments table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS payments (
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
    payment_date TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (loan_id) REFERENCES loans (id),
    FOREIGN KEY (client_id) REFERENCES users (id)
)
''')

# Create disbursements table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS disbursements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    method TEXT,
    phone_number TEXT,
    bank_name TEXT,
    account_number TEXT,
    transaction_id TEXT,
    disbursement_date TIMESTAMP,
    status TEXT DEFAULT 'pending',
    confirmed_by INTEGER,
    FOREIGN KEY (loan_id) REFERENCES loans (id),
    FOREIGN KEY (client_id) REFERENCES users (id),
    FOREIGN KEY (confirmed_by) REFERENCES users (id)
)
''')

conn.commit()
conn.close()

print('\n✅ Database update complete!')
