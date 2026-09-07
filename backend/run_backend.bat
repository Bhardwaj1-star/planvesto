@echo off
title Planvesto Backend
echo =======================================
echo   Planvesto Backend Starting...
echo =======================================

:: Miniconda initialize karo
call C:\Users\lenovo\miniconda3\Scripts\activate.bat C:\Users\lenovo\miniconda3

:: planvesto conda environment activate karo
call conda activate planvesto

:: Backend directory mein jao
cd /d "D:\Desktop files\system\backend"

echo.
echo [INFO] Environment  : planvesto
echo [INFO] Directory    : %CD%
echo [INFO] Entry Point  : main.py
echo [INFO] Server URL   : http://127.0.0.1:8000
echo.
echo =======================================
echo   Press Ctrl+C to stop the server
echo =======================================
echo.

:: FastAPI/Uvicorn server start karo
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

pause
