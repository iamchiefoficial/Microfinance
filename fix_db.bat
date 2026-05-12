@echo off
echo Adding approved_by column to loans table...
mysql -u root -p microfinance_db < add_approved_by_fixed.sql
if %ERRORLEVEL% EQU 0 (
    echo ✅ Database column added successfully!
) else (
    echo ❌ Error adding column: %ERRORLEVEL%
)
pause
