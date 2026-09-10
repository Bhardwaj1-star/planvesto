@echo off
setlocal

set "CONDA_ROOT=C:\Users\lenovo\miniconda3"
set "ENV_NAME=planvesto"
set "PROJECT_ROOT=D:\Desktop files\system"

echo [INFO] Initializing Miniconda...
call "%CONDA_ROOT%\Scripts\activate.bat"

if errorlevel 1 (
    echo [ERROR] Could not initialize Miniconda.
    exit /b 1
)

echo [INFO] Activating environment: %ENV_NAME%
call conda activate %ENV_NAME%

if errorlevel 1 (
    echo [ERROR] Could not activate Conda environment: %ENV_NAME%
    exit /b 1
)

echo [INFO] Python:
python --version

echo [INFO] Python path:
where python

cd /d "%PROJECT_ROOT%"

echo [SUCCESS] Planvesto environment is ready.
endlocal