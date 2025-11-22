@echo off
REM Chemical Equipment Visualizer - Windows Setup Script

echo ======================================
echo Chemical Equipment Visualizer Setup
echo ======================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo √ Python found

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo X Node.js is not installed. Please install Node.js 16 or higher.
    pause
    exit /b 1
)
echo √ Node.js found

echo.
echo Setting up Django Backend...
echo ----------------------------

REM Create backend directories
if not exist "backend\chemical_equipment_api" mkdir backend\chemical_equipment_api
if not exist "backend\equipment" mkdir backend\equipment
if not exist "backend\media" mkdir backend\media

cd backend

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Run migrations
python manage.py makemigrations equipment
python manage.py migrate

echo.
echo √ Backend setup complete!
echo.

cd ..

REM Setup Web Frontend
echo Setting up React Web Frontend...
echo --------------------------------

cd frontend-web

REM Install npm dependencies
call npm install

echo.
echo √ Web frontend setup complete!
echo.

cd ..

REM Setup Desktop App
echo Setting up PyQt5 Desktop Application...
echo ---------------------------------------

cd frontend-desktop

REM Create virtual environment
if not exist "venv" python -m venv venv

call venv\Scripts\activate.bat
pip install -r desktop_requirements.txt

echo.
echo √ Desktop application setup complete!
echo.

cd ..

REM Final instructions
echo.
echo ======================================
echo √ Setup Complete! 🎉
echo ======================================
echo.
echo To start the application:
echo.
echo 1. Start Django Backend:
echo    cd backend
echo    venv\Scripts\activate.bat
echo    python manage.py runserver
echo.
echo 2. Start React Web App (new terminal):
echo    cd frontend-web
echo    npm start
echo.
echo 3. Start Desktop App (new terminal):
echo    cd frontend-desktop
echo    venv\Scripts\activate.bat
echo    python desktop_app.py
echo.
echo Sample data file: sample_equipment_data.csv
echo.
echo Happy coding! 🚀
echo ======================================

pause