@echo off
REM Microfinance Platform Deployment Script for Windows
echo 🚀 Starting Microfinance Platform Deployment...

REM Set environment variables
set FLASK_APP=app.py
set FLASK_ENV=production

REM Install dependencies using Python launcher
echo 📦 Installing Python dependencies...
py -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    echo 💡 Try: python -m pip install --user -r requirements.txt
    pause
    exit /b 1
)

REM Setup database - try multiple approaches
echo 🗄️ Setting up MySQL database...

REM Try standard mysql command
mysql -u root -p < database_setup.sql
if errorlevel 1 (
    echo 🔄 MySQL command failed, trying alternative...
    
    REM Try with full path (common MySQL installation paths)
    "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < database_setup.sql
    if errorlevel 1 (
        echo 🔄 Trying alternative path...
        "C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < database_setup.sql
        if errorlevel 1 (
            echo ❌ MySQL not found. Please install MySQL or add to PATH.
            echo 📋 See windows_setup_guide.md for manual setup
            pause
            exit /b 1
        )
    )
)

REM Create admin account using Python launcher
echo 👤 Creating admin account...
py admin_setup.py
if errorlevel 1 (
    echo ❌ Failed to create admin account
    pause
    exit /b 1
)

REM Start the application using Python launcher
echo 🌐 Starting Microfinance Platform...
echo 📍 Access your application at: http://localhost:5000
echo.
echo ✅ Deployment complete!
echo.
echo 📝️  System Features:
echo    - Pure server-side rendering (no JavaScript)
echo    - MySQL database backend
echo    - Role-based access control
echo    - Complete loan approval workflow
echo    - Production-ready security
echo.
echo 📝️  Don't forget to:
echo    - Change default admin password
echo    - Configure proper environment variables
echo    - Set up HTTPS in production
echo    - Configure firewall rules
echo.
echo 🌐 Opening browser...
start http://localhost:5000

py app.py
