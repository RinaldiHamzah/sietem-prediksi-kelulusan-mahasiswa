@echo off
setlocal

REM ==========================================
REM Startup Aplikasi Prediksi Kelulusan
REM ==========================================

cd /d "%~dp0"

echo.
echo ====================================================
echo   APLIKASI PREDIKSI KELULUSAN MAHASISWA
echo   Decision Tree C4.5
echo ====================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python tidak terinstall atau tidak ada di PATH.
    echo Silakan install Python dari https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python terdeteksi
echo.

if exist "requirements.txt" (
    echo [INFO] Memastikan dependency sudah terinstall...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Gagal menginstall dependency dari requirements.txt.
        pause
        exit /b 1
    )
) else (
    echo [WARNING] requirements.txt tidak ditemukan. Melewati instalasi dependency.
)

echo.

if not exist "data\kelulusan.csv" (
    echo [INFO] Dataset belum ditemukan. Membuat dataset...
    python generate.py
    if %errorlevel% neq 0 (
        echo ERROR: Gagal membuat dataset.
        pause
        exit /b 1
    )
)

if not exist "models\model_c45.pkl" goto train_model
if not exist "models\label_encoders.pkl" goto train_model
if not exist "models\target_encoder.pkl" goto train_model
if not exist "assets\decision_tree_visualization.png" goto train_model
if not exist "assets\feature_importance.png" goto train_model
if not exist "assets\confusion_matrix.png" goto train_model
goto run_app

:train_model
echo [INFO] File model/visualisasi belum lengkap. Melatih model...
python model.py
if %errorlevel% neq 0 (
    echo ERROR: Gagal melatih model.
    pause
    exit /b 1
)

:run_app
if not exist "app.py" (
    echo ERROR: app.py tidak ditemukan.
    pause
    exit /b 1
)

echo.
echo ====================================================
echo   Memulai aplikasi...
echo ====================================================
echo.
echo   URL: http://localhost:8501
echo   Tekan CTRL+C untuk menghentikan aplikasi.
echo.

python -m streamlit run app.py --server.port 8501

pause
