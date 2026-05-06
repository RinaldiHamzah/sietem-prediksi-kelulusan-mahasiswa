@echo off
REM Test script for Vercel deployment (Windows)

echo.
echo ======================================
echo Testing Vercel Deployment Setup
echo ======================================
echo.

REM Check Python
echo [1/6] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    pause
    exit /b 1
)
echo OK: Python found
echo.

REM Install dependencies
echo [2/6] Installing dependencies...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo OK: Dependencies installed
echo.

REM Check model files
echo [3/6] Checking model files...
if not exist "model_c45.pkl" (
    echo ERROR: model_c45.pkl not found
    pause
    exit /b 1
)
echo OK: model_c45.pkl found

if not exist "label_encoders.pkl" (
    echo ERROR: label_encoders.pkl not found
    pause
    exit /b 1
)
echo OK: label_encoders.pkl found

if not exist "target_encoder.pkl" (
    echo ERROR: target_encoder.pkl not found
    pause
    exit /b 1
)
echo OK: target_encoder.pkl found
echo.

REM Check API files
echo [4/6] Checking API files...
if not exist "api\index.py" (
    echo ERROR: api\index.py not found
    pause
    exit /b 1
)
echo OK: api\index.py found
echo.

REM Check Vercel config
echo [5/6] Checking Vercel config...
if not exist "vercel.json" (
    echo ERROR: vercel.json not found
    pause
    exit /b 1
)
echo OK: vercel.json found
echo.

REM Test imports
echo [6/6] Testing Python imports...
python -c "from fastapi import FastAPI; print('OK: FastAPI import successful')"
if %errorlevel% neq 0 (
    echo ERROR: Failed to import FastAPI
    pause
    exit /b 1
)

python -c "import pandas; import sklearn; print('OK: Data science imports successful')"
if %errorlevel% neq 0 (
    echo ERROR: Failed to import data science libraries
    pause
    exit /b 1
)
echo.

echo ======================================
echo ✓ All tests passed!
echo ======================================
echo.
echo Ready to deploy to Vercel!
echo.
echo Next steps:
echo   1. git add .
echo   2. git commit -m "Vercel deployment ready"
echo   3. git push
echo.
pause
