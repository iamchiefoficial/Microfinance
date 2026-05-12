@echo off
echo Adding approved_by column to loans table...
mysql -u root -p microfinance_db -e "ALTER TABLE loans ADD COLUMN approved_by VARCHAR(100) DEFAULT NULL;"
if %ERRORLEVEL% EQU 0 (
    echo ✅ Database column added successfully!
) else (
    echo ❌ Error adding column: %ERRORLEVEL%
)
pause
