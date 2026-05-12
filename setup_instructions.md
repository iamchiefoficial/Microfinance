# MySQL Database Setup Instructions

## Prerequisites
1. Install MySQL Server on your system
2. Start MySQL service
3. Create database and user

## Database Setup

### Option 1: Using SQL File
```bash
mysql -u root -p < database_setup.sql
```

### Option 2: Manual Setup
```sql
-- Connect to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE microfinance_db;

-- Use the database
USE microfinance_db;

-- Create tables (copy from database_setup.sql)
```

## Configuration

The application is configured to connect to MySQL using:
- Host: localhost
- Database: microfinance_db
- User: root
- Password: password

To change these settings, modify the database URI in app.py:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@hostname/database_name'
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Run Application
```bash
python app.py
```

## Troubleshooting

### Connection Issues
- Ensure MySQL server is running
- Verify database exists: `SHOW DATABASES;`
- Check credentials in app.py
- Make sure PyMySQL is installed

### Permission Issues
- Grant privileges if needed:
```sql
GRANT ALL PRIVILEGES ON microfinance_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```
