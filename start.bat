@echo off
REM Simple launcher for Microfinance Platform
echo 🚀 Starting Microfinance Platform...
echo 📍 Access your application at: http://localhost:5000
echo.
echo 💡 If commands don't work, use: py app.py
echo.

REM Try to start the application
py app.py

REM If that fails, show instructions
if errorlevel 1 (
    echo.
    echo ❌ Could not start application
    echo 💡 Try manual commands:
    echo    1. Install deps: py -m pip install -r requirements.txt
    echo    2. Setup database: mysql -u root -p < database_setup.sql
    echo    3. Create admin: py admin_setup.py
    echo    4. Start app: py app.py
    echo.
    echo 📋 See windows_setup_guide.md for detailed help
    pause
)
