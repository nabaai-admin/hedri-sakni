# نظام إدارة حجوزات الأراضي (Land Reservation Admin System)

A full-stack admin application for managing and reviewing land reservation attempts with UiPath automation integration.

## 🚀 Features

### Backend (Flask REST API)
- ✅ RESTful API with Flask
- ✅ PostgreSQL database
- ✅ JWT authentication
- ✅ Swagger/OpenAPI documentation
- ✅ Background job scheduler (APScheduler)
- ✅ UiPath API integration
- ✅ Complete logging and traceability
- ✅ External webhook for status updates

### Frontend (React.js)
- ✅ Modern React with Vite
- ✅ Arabic RTL support
- ✅ Responsive design
- ✅ React Query for data management
- ✅ Toast notifications
- ✅ Premium UI/UX with animations

### Core Functionality
1. **Admin Dashboard**
   - Overview statistics
   - Success rate visualization
   - Area-based analytics

2. **Management Module**
   - Areas management (CRUD)
   - Customers management with Arabic fields:
     - الاسم (Name)
     - رقم الهاتف (Phone Number)
     - الرقم الوطني (National ID)
     - المنطقة (Area - dropdown)
     - حالة الحجز (Reservation Status: OPEN/SUCCESS/FAILED)
   - Reservation slots management

3. **Analytics & Review Dashboard**
   - Aggregated success/failure/open counts by area
   - Date range filtering
   - Filters by area, status, and reservation date
   - Success rate calculations
   - Detailed attempt logs with exact response messages

4. **Automation Integration**
   - Background jobs trigger at scheduled times
   - Sends requests to UiPath API with authentication
   - External update webhook receives status updates
   - Stores response messages exactly as received

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 12+
- npm or yarn

## 🛠️ Installation

### 🐳 Docker Installation (Recommended - Easiest!)

**One command to run everything:**
```bash
./start.sh
```

That's it! Docker will automatically:
- ✅ Start PostgreSQL database
- ✅ Start Flask backend API
- ✅ Start React frontend
- ✅ Configure networking between services

**Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- API Docs: http://localhost:5000/api/docs

**Default credentials:**
- Username: `admin`
- Password: `admin123`

**Useful commands:**
```bash
./start.sh    # Start all services
./stop.sh     # Stop all services
./logs.sh     # View logs
```

📚 **For detailed Docker instructions, see [DOCKER.md](DOCKER.md)**

---

### 💻 Manual Installation (Alternative)

If you prefer to run without Docker:

#### 1. Clone the Repository
```bash
cd /home/abdulrasheed/NabaAI/hedri-sakni
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

**Configure `.env`:**
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/hedri_sakni
UIPATH_API_URL=https://your-uipath-instance.com/api
UIPATH_API_KEY=your-api-key
UIPATH_CLIENT_ID=your-client-id
UIPATH_CLIENT_SECRET=your-client-secret
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb hedri_sakni

# Initialize database (tables will be created automatically on first run)
python run.py
```

### 4. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file (optional)
echo "VITE_API_URL=http://localhost:5000/api" > .env
```

## 🚀 Running the Application

### Start Backend
```bash
cd backend
source venv/bin/activate
python run.py
```
Backend will run on `http://localhost:5000`

### Start Frontend
```bash
cd frontend
npm run dev
```
Frontend will run on `http://localhost:5173`

## 📚 API Documentation

Once the backend is running, access Swagger documentation at:
```
http://localhost:5000/api/docs
```

### Key Endpoints

#### Authentication
- `POST /api/auth/login` - Admin login

#### Areas
- `GET /api/areas` - List all areas
- `POST /api/areas` - Create area
- `PUT /api/areas/:id` - Update area
- `DELETE /api/areas/:id` - Delete area

#### Customers
- `GET /api/customers` - List customers (with filters)
- `POST /api/customers` - Create customer
- `PUT /api/customers/:id` - Update customer
- `DELETE /api/customers/:id` - Delete customer

#### Reservations
- `GET /api/reservations` - List reservation slots
- `POST /api/reservations` - Create and schedule slot
- `PUT /api/reservations/:id` - Update slot
- `DELETE /api/reservations/:id` - Delete slot

#### Analytics
- `GET /api/analytics/summary` - Aggregated statistics
- `GET /api/analytics/attempts` - Detailed attempts log

#### External Integration
- `POST /api/external/update` - Webhook for UiPath status updates
- `GET /api/external/health` - Health check

## 🔐 Default Credentials

**Username:** `admin`  
**Password:** `admin123`

⚠️ **Change these in production!**

## 🏗️ Project Structure

```
hedri-sakni/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── config.py            # Configuration
│   │   ├── models.py            # Database models
│   │   ├── schemas.py           # Validation schemas
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # Business logic
│   │   └── utils/               # Utilities
│   ├── requirements.txt
│   └── run.py                   # Entry point
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API client
│   │   ├── App.jsx              # Main app
│   │   └── main.jsx             # Entry point
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🔄 Background Job Scheduler

The system automatically:
1. Schedules jobs for each reservation slot
2. At the scheduled time, sends requests to UiPath API for all customers in that area with OPEN status
3. Logs all requests and responses
4. Waits for external webhook to update final status

## 📊 Database Schema

### Tables
- **areas** - Geographical areas
- **customers** - Customer information with Arabic fields
- **reservation_slots** - Scheduled reservation times per area
- **reservation_attempts** - Complete log of all attempts with responses

## 🌐 External API Integration

### UiPath Request Format
```json
{
  "national_id": "string",
  "phone_number": "string",
  "area": "string",
  "timestamp": "ISO 8601"
}
```

### Webhook Update Format
```json
{
  "national_id": "string",
  "status": "SUCCESS|FAILED",
  "response_code": 200,
  "message": "Response message",
  "additional_data": {}
}
```

## 🎨 UI Features

- ✨ Modern, premium design
- 🌙 Smooth animations and transitions
- 📱 Fully responsive
- 🔄 RTL support for Arabic
- 🎯 Intuitive navigation
- 📊 Interactive charts and visualizations

## 🔧 Development

### Backend Development
```bash
# Run with auto-reload
FLASK_ENV=development python run.py
```

### Frontend Development
```bash
# Run with hot reload
npm run dev
```

### Build for Production
```bash
# Frontend
npm run build

# Backend - use production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 📝 Environment Variables

### Backend
- `FLASK_ENV` - Environment (development/production)
- `DATABASE_URL` - PostgreSQL connection string
- `UIPATH_API_URL` - UiPath API endpoint
- `UIPATH_API_KEY` - API key
- `UIPATH_CLIENT_ID` - OAuth client ID
- `UIPATH_CLIENT_SECRET` - OAuth client secret
- `ADMIN_USERNAME` - Admin username
- `ADMIN_PASSWORD` - Admin password
- `JWT_SECRET_KEY` - JWT signing key
- `CORS_ORIGINS` - Allowed CORS origins

### Frontend
- `VITE_API_URL` - Backend API URL

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Create database if missing
createdb hedri_sakni
```

### Port Already in Use
```bash
# Backend (port 5000)
lsof -ti:5000 | xargs kill -9

# Frontend (port 5173)
lsof -ti:5173 | xargs kill -9
```

## 📄 License

This project is proprietary software.

## 👥 Support

For support, please contact the development team.

---

Built with ❤️ using Flask, React, and PostgreSQL
