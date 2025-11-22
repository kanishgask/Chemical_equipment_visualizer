# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Clone/Download the Project

```bash
git clone <your-repo-url>
cd chemical-equipment-visualizer
```

### Step 2: Automatic Setup

**On macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```bash
setup.bat
```

### Step 3: Start the Applications

Open **3 separate terminals**:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python manage.py runserver
```

**Terminal 2 - Web App:**
```bash
cd frontend-web
npm start
```

**Terminal 3 - Desktop App:**
```bash
cd frontend-desktop
source venv/bin/activate  # Windows: venv\Scripts\activate
python desktop_app.py
```

### Step 4: Test the Application

1. **Register a new account** in either web or desktop app
2. **Upload** the provided `sample_equipment_data.csv`
3. **View** the beautiful visualizations
4. **Download** a PDF report

---

## 📱 Access Points

- **Backend API**: http://localhost:8000
- **Web Application**: http://localhost:3000
- **Desktop Application**: Runs natively on your system

---

## 🆘 Quick Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 8000
# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Dependencies Not Installing
```bash
# Update pip first
pip install --upgrade pip

# Then retry
pip install -r requirements.txt
```

### React Won't Start
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 📊 Sample Data Format

Your CSV should look like this:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-A1,Reactor,125.5,15.2,350.0
Pump-B2,Pump,85.3,22.5,45.0
```

---

## 🎥 Demo Checklist

When recording your demo video:

✅ Show registration/login  
✅ Upload sample CSV  
✅ Display charts and tables  
✅ Navigate dataset history  
✅ Generate PDF report  
✅ Show both web AND desktop apps  
✅ Keep it under 3 minutes  

---

## 📞 Need Help?

Check the full README.md for:
- Detailed installation steps
- API documentation
- Deployment guide
- Configuration options

---

**Remember**: Make sure Django backend is running before starting the frontend applications!

Good luck with your intern screening task! 🎓