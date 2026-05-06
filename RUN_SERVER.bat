@echo off
REM Run local FastAPI server

echo.
echo ====================================
echo FastAPI Development Server
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

REM Install/Update uvicorn if needed
echo Checking dependencies...
pip install -q fastapi uvicorn pandas numpy scikit-learn pydantic

echo.
echo Starting FastAPI server...
echo.
echo Server will run at: http://localhost:8000
echo.
echo API Docs:
echo   - Swagger UI: http://localhost:8000/docs
echo   - ReDoc: http://localhost:8000/redoc
echo.
echo Frontend:
echo   - http://localhost:8000/public/index.html
echo.
echo Press CTRL+C to stop the server
echo.

python main.py

pause
