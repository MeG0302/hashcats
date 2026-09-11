@echo off
echo ==========================================
echo HASHCATS GPU MINER - WINDOWS SETUP
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found!
echo.

REM Install dependencies
echo Installing required packages...
pip install web3 eth-account pycryptodome requests numpy

echo.
echo Checking for CUDA/GPU...
nvidia-smi >nul 2>&1
if %errorlevel% equ 0 (
    echo GPU detected! Installing PyCUDA...
    pip install pycuda
) else (
    echo No NVIDIA GPU detected. Will use CPU mining.
)

echo.
echo ==========================================
echo SETUP COMPLETE!
echo ==========================================
echo.
echo To start mining:
echo   python hashcats_miner.py
echo.
pause
