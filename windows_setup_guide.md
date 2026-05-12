# Windows Setup Guide for Microfinance Platform

## Prerequisites Installation

### 1. Install Python
Download and install Python from: https://www.python.org/downloads/
- Choose "Add Python to PATH" during installation
- Verify installation: Open Command Prompt and type `python --version`

### 2. Install MySQL
Download and install MySQL Community Server from: https://dev.mysql.com/downloads/mysql/
- During installation, set root password
- Make sure to include MySQL Command Line Tools

### 3. Verify PATH
Open Command Prompt and test:
```cmd
python --version
pip --version
mysql --version
```

If any command shows "not recognized", you need to add to PATH or use full paths.

## Step-by-Step Deployment

### Step 1: Open Command Prompt as Administrator
- Right-click Command Prompt
- Select "Run as administrator"

### Step 2: Navigate to Project Directory
```cmd
cd "C:\Users\user\Desktop\new wid pyth"
```

### Step 3: Install Python Dependencies
```cmd
python -m pip install -r requirements.txt
```

### Step 4: Setup MySQL Database
```cmd
mysql -u root -p < database_setup.sql
```
Enter your MySQL root password when prompted.

### Step 5: Create Admin Account
```cmd
python admin_setup.py
```

### Step 6: Start Application
```cmd
python app.py
```

## Alternative: Using Python Launcher
If `python` command doesn't work, try:
```cmd
py -m pip install -r requirements.txt
py admin_setup.py
py app.py
```

## Troubleshooting

### "python is not recognized"
- Restart Command Prompt
- Use "py" instead of "python"
- Reinstall Python with PATH option

### "pip is not recognized"
- Use `python -m pip` instead of `pip`
- Check Python installation

### "mysql is not recognized"
- Add MySQL bin folder to PATH
- Use full path: `"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"`
- Reinstall MySQL with Command Line Tools

### Database Connection Issues
- Ensure MySQL service is running
- Check credentials in app.py
- Verify database exists

## Quick Start Commands
Once everything is set up, you can use these shortcuts:

```cmd
# Install and run
cd "C:\Users\user\Desktop\new wid pyth"
python -m pip install -r requirements.txt && python admin_setup.py && python app.py
```

## Browser Access
After successful startup, open your browser and navigate to:
http://localhost:5000
