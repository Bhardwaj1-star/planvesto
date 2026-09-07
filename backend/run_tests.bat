@echo off
title Planvesto - Backend Tests
echo =========================================
echo   Planvesto Backend Test Runner
echo =========================================

:: Miniconda initialize karo
call C:\Users\lenovo\miniconda3\Scripts\activate.bat C:\Users\lenovo\miniconda3

:: planvesto environment activate karo
call conda activate planvesto

:: Backend directory mein jao
cd /d "D:\Desktop files\system\backend"

echo.
echo [INFO] Running pytest on: tests/
echo [INFO] Environment: planvesto
echo [INFO] No database writes - pure unit tests
echo.
echo -----------------------------------------

:: pytest run karo with verbose + color output
python -m pytest tests/ -v --tb=short --no-header -q

echo.
echo =========================================
echo   Test run complete. See results above.
echo =========================================
pause
