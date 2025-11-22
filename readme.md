# Chemical Equipment Parameter Visualizer
### Hybrid Web + Desktop Application

A full-stack application for visualizing and analyzing chemical equipment parameters. Features both a React web interface and PyQt5 desktop application, both consuming the same Django REST API backend.

---

## 📋 Features

- ✅ **CSV Upload**: Upload equipment data via web or desktop interface
- 📊 **Data Visualization**: Interactive charts using Chart.js (Web) and Matplotlib (Desktop)
- 📈 **Analytics**: Automatic calculation of averages and distributions
- 🗃️ **History Management**: Store and retrieve last 5 uploaded datasets
- 🔐 **Authentication**: Secure user registration and login with token-based auth
- 📄 **PDF Reports**: Generate comprehensive PDF reports with data summaries
- 🎨 **Responsive UI**: Modern, intuitive interfaces for both platforms

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend (Web)** | React.js + Chart.js | Interactive web visualization |
| **Frontend (Desktop)** | PyQt5 + Matplotlib | Native desktop application |
| **Backend** | Django + Django REST Framework | RESTful API server |
| **Data Processing** | Pandas | CSV parsing and analytics |
| **Database** | SQLite | Data persistence |
| **Reporting** | ReportLab | PDF generation |

---

## 📁 Project Structure

```
chemical-equipment-visualizer/
├── backend/                    # Django Backend
│   ├── chemical_equipment_api/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── equipment/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── manage.py
│   └── requirements.txt
│
├── frontend-web/              # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   └── package.json
│
├── frontend-desktop/          # PyQt5 Desktop App
│   ├── desktop_app.py
│   └── desktop_requirements.txt
│
├── sample_equipment_data.csv  # Sample data
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- pip
- npm

### 1. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin panel)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Backend will run at: `http://localhost:8000`

### 2. Web Frontend Setup (React)

```bash
# Navigate to web frontend directory
cd frontend-web

# Install dependencies
npm install

# Start development server
npm start
```

Web app will open at: `http://localhost:3000`

### 3. Desktop Application Setup (PyQt5)

```bash
# Navigate to desktop directory
cd frontend-desktop

# Create virtual environment (if not using backend's)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r desktop_requirements.txt

# Run desktop application
python desktop_app.py
```

---

## 📊 Sample Data

A sample CSV file (`sample_equipment_data.csv`) is included with 25 equipment records containing:

- Equipment Name
- Type (Reactor, Pump, Heat Exchanger, etc.)
- Flowrate
- Pressure
- Temperature

Use this file to test the application functionality.

---

## 🔑 API Endpoints

### Authentication

- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - User login

### Datasets

- `GET /api/datasets/` - List user's datasets (last 5)
- `POST /api/datasets/upload/` - Upload CSV file
- `GET /api/datasets/{id}/` - Get dataset details
- `GET /api/datasets/{id}/summary/` - Get dataset summary with analytics
- `GET /api/datasets/{id}/generate_pdf/` - Download PDF report

---

## 💻 Usage Guide

### Web Application

1. **Register/Login**: Create account or login with existing credentials
2. **Upload CSV**: Click "Select File" and choose your CSV file
3. **View Data**: Charts and tables automatically display after upload
4. **Navigate History**: Click any dataset in the sidebar to view it
5. **Download Report**: Click "Download PDF Report" for any dataset

### Desktop Application

1. **Launch**: Run `python desktop_app.py`
2. **Authenticate**: Register or login with your credentials
3. **Upload File**: Click "Select File" → Choose CSV → Click "Upload"
4. **View Visualizations**: Charts and data table display automatically
5. **Access History**: Click any dataset from the history list
6. **Generate PDF**: Click "Download PDF Report" button

---

## 📸 Screenshots
<img width="1427" height="830" alt="image" src="https://github.com/user-attachments/assets/2565ca66-0d93-4e6d-adeb-8b05f25ec6c5" />
<img width="1417" height="268" alt="image" src="https://github.com/user-attachments/assets/d43f9a54-dc67-4972-9b59-3a4d4cdef3d5" />
<img width="1422" height="1585" alt="image" src="https://github.com/user-attachments/assets/360a81ed-fd42-456a-9e57-d672917553c8" />
<img width="400" height="242" alt="image" src="https://github.com/user-attachments/assets/76c7295c-43e5-44f4-8271-13e9b76f15f1" />
<img width="401" height="357" alt="image" src="https://github.com/user-attachments/assets/6f8f0ea8-c43a-4677-b50b-8c683168dbfa" />




### Web Application
- Modern gradient design with responsive layout
- Interactive Chart.js visualizations
- Clean table display with hover effects

### Desktop Application
- Native OS look and feel
- Matplotlib-powered charts
- Sidebar navigation with dataset history

---

## 🎯 Key Features Explained

### 1. CSV Upload & Validation
- Validates required columns
- Handles data cleaning (removes null values)
- Provides clear error messages

### 2. Data Analytics
- Calculates average Flowrate, Pressure, Temperature
- Generates equipment type distribution
- Stores complete dataset for future reference

### 3. Visualization
- **Bar Charts**: Average parameter values
- **Pie Charts**: Equipment type distribution
- **Data Tables**: Complete equipment listings

### 4. History Management
- Automatically maintains last 5 datasets
- Older datasets are removed automatically
- Quick access to previous uploads

### 5. PDF Generation
- Professional report layout
- Summary statistics table
- Equipment type distribution
- Downloadable in one click

### 6. Authentication
- Secure token-based authentication
- User-specific data isolation
- Session management

---

## 🔧 Configuration

### Backend Configuration

Edit `backend/chemical_equipment_api/settings.py`:

```python
# Change secret key in production
SECRET_KEY = 'your-secret-key-here'

# Set DEBUG to False in production
DEBUG = False

# Configure allowed hosts
ALLOWED_HOSTS = ['yourdomain.com']

# Database configuration (for production use PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        # ... other settings
    }
}
```

### Frontend Configuration

Edit `frontend-web/src/App.js`:

```javascript
// Change API URL for production
const API_URL = 'https://your-api-domain.com/api';
```

Edit `frontend-desktop/desktop_app.py`:

```python
# Change API URL for production
API_URL = 'https://your-api-domain.com/api'
```

---

## 🚢 Deployment

### Backend Deployment (Django)

**Option 1: Heroku**
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

**Option 2: DigitalOcean / AWS / Google Cloud**
- Use Gunicorn as WSGI server
- Configure Nginx as reverse proxy
- Set up SSL certificate
- Use PostgreSQL for database

### Frontend Deployment (React)

**Option 1: Vercel**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend-web
vercel
```

**Option 2: Netlify**
```bash
# Build production bundle
npm run build

# Deploy build folder to Netlify
```

### Desktop Application Distribution

**Windows:**
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed desktop_app.py
```

**macOS:**
```bash
# Use py2app
pip install py2app
python setup.py py2app
```

---

## 🧪 Testing

### Test CSV Upload
1. Use provided `sample_equipment_data.csv`
2. Verify data appears in table
3. Check chart generation
4. Confirm PDF download

### Test Authentication
1. Register new user
2. Logout and login
3. Verify token persistence
4. Test invalid credentials

### Test Data Management
1. Upload 6 datasets
2. Verify only last 5 are retained
3. Check dataset details retrieval

---

## 🐛 Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError`
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Issue**: Database errors
```bash
# Solution: Delete db.sqlite3 and migrations
rm db.sqlite3
rm equipment/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

### Frontend Issues

**Issue**: CORS errors
```python
# Solution: Check CORS settings in settings.py
CORS_ALLOW_ALL_ORIGINS = True  # Development only
```

**Issue**: API connection refused
- Ensure Django backend is running on port 8000
- Check API_URL in frontend code

### Desktop App Issues

**Issue**: PyQt5 installation fails
```bash
# Solution: Try specific version
pip install PyQt5==5.15.9
```

**Issue**: Charts not displaying
```bash
# Solution: Install matplotlib dependencies
pip install matplotlib --upgrade
```

---

## 📝 Development Notes

### Adding New Features

1. **Backend**: Add endpoints in `views.py`, update `serializers.py`
2. **Web Frontend**: Create components, update API calls in `App.js`
3. **Desktop**: Add methods to `MainWidget`, update UI in `init_ui()`

### CSV Format Requirements

Your CSV must include these exact column names:
- `Equipment Name`
- `Type`
- `Flowrate`
- `Pressure`
- `Temperature`

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

---

## 📄 License

This project is created for educational purposes. Feel free to use and modify as needed.

---

## 👥 Support

For issues or questions:
- Create an issue on GitHub
- Check documentation in `/docs`
- Review API documentation at `/api/docs` (when available)

---

## 🎬 Demo Video Guide

When creating your demo video (2-3 minutes), cover:

1. **Introduction** (15s)
   - Project overview
   - Tech stack

2. **Web Application Demo** (60s)
   - Login/Registration
   - CSV upload
   - Data visualization
   - PDF generation

3. **Desktop Application Demo** (60s)
   - Launch and login
   - File upload
   - Charts display
   - History navigation

4. **Technical Highlights** (15s)
   - API architecture
   - Data processing
   - Code structure

---

## ✅ Project Checklist

- [x] Django REST API with authentication
- [x] CSV upload and parsing
- [x] Data analytics (averages, distribution)
- [x] SQLite database with models
- [x] Last 5 datasets history management
- [x] React web frontend
- [x] PyQt5 desktop application
- [x] Chart.js visualizations (web)
- [x] Matplotlib visualizations (desktop)
- [x] PDF report generation
- [x] Token-based authentication
- [x] Sample CSV data
- [x] Comprehensive README
- [x] Requirements files

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Chart.js Documentation](https://www.chartjs.org/)
- [Matplotlib Documentation](https://matplotlib.org/)

---

**Built with ❤️ for the Intern Screening Task**

*Last Updated: November 2024*
