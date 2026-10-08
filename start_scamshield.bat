@echo off
title ScamShield
cd /d "%~dp0"

echo ============================================================
echo                  ScamShield Launcher
echo ============================================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found.
    echo Install Python 3.11-3.13 and try again.
    pause
    exit /b 1
)

echo Checking Python...
python --version
echo.

echo Installing/updating required packages...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Package installation failed.
    echo Check your internet connection and Python installation.
    pause
    exit /b 1
)

echo.
echo Starting ScamShield...
python app.py

echo.
echo ScamShield stopped.
pause
