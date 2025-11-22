#!/bin/bash

# Chemical Equipment Visualizer - Quick Setup Script
# This script sets up the entire project automatically

echo "======================================"
echo "Chemical Equipment Visualizer Setup"
echo "======================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✓ Python found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi
echo "✓ Node.js found: $(node --version)"

echo ""
echo "Setting up Django Backend..."
echo "----------------------------"

# Create backend directory structure
mkdir -p backend/chemical_equipment_api
mkdir -p backend/equipment
mkdir -p backend/media

cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create Django project files if they don't exist
if [ ! -f "manage.py" ]; then
    django-admin startproject chemical_equipment_api .
    python manage.py startapp equipment
fi

# Run migrations
python manage.py makemigrations equipment
python manage.py migrate

echo ""
echo "✓ Backend setup complete!"
echo ""

cd ..

# Setup Web Frontend
echo "Setting up React Web Frontend..."
echo "--------------------------------"

cd frontend-web

# Install npm dependencies
npm install

echo ""
echo "✓ Web frontend setup complete!"
echo ""

cd ..

# Setup Desktop App
echo "Setting up PyQt5 Desktop Application..."
echo "---------------------------------------"

cd frontend-desktop

# Use same virtual environment or create new one
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r desktop_requirements.txt

echo ""
echo "✓ Desktop application setup complete!"
echo ""

cd ..

# Final instructions
echo ""
echo "======================================"
echo "✓ Setup Complete! 🎉"
echo "======================================"
echo ""
echo "To start the application:"
echo ""
echo "1. Start Django Backend:"
echo "   cd backend"
echo "   source venv/bin/activate  (or venv\\Scripts\\activate on Windows)"
echo "   python manage.py runserver"
echo ""
echo "2. Start React Web App (new terminal):"
echo "   cd frontend-web"
echo "   npm start"
echo ""
echo "3. Start Desktop App (new terminal):"
echo "   cd frontend-desktop"
echo "   source venv/bin/activate  (or venv\\Scripts\\activate on Windows)"
echo "   python desktop_app.py"
echo ""
echo "Sample data file: sample_equipment_data.csv"
echo ""
echo "Default credentials for testing:"
echo "Username: testuser"
echo "Password: testpass123"
echo ""
echo "Happy coding! 🚀"
echo "======================================"