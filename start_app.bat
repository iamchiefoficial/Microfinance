@echo off
echo ========================================
echo    ORETHAN MICROFINANCE PLATFORM
echo ========================================
echo.
echo Starting application...
echo.

REM Try different Python commands
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Found: python
    python app_fixed_workflow.py
    goto end
)

python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo Found: python3
    python3 app_fixed_workflow.py
    goto end
)

py --version >nul 2>&1
if %errorlevel% == 0 (
    echo Found: py
    py app_fixed_workflow.py
    goto end
)

py -3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo Found: py -3
    py -3 app_fixed_workflow.py
    goto end
)

echo.
echo ERROR: Python not found!
echo Please install Python 3.7 or higher from https://python.org
echo.
pause

:end
echo.
echo Application stopped.
