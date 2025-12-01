# 🐳 Docker Deployment Guide

## Quick Start (Easiest Way!)

### One Command to Run Everything:
```bash
./start.sh
```

That's it! The script will:
- ✅ Check Docker installation
- ✅ Create `.env` file if needed
- ✅ Build all containers
- ✅ Start all services (PostgreSQL, Backend, Frontend)
- ✅ Show you the access URLs

## 📦 What Gets Started

When you run `./start.sh`, Docker Compose will start:

1. **PostgreSQL Database** (Port 5432)
   - Container: `hedri-sakni-db`
   - Database: `hedri_sakni`
   - User: `postgres`
   - Password: `postgres` (change in production!)

2. **Flask Backend API** (Port 5000)
   - Container: `hedri-sakni-backend`
   - Swagger Docs: http://localhost:5000/api/docs
   - Health Check: http://localhost:5000/api/external/health

3. **React Frontend** (Port 5173)
   - Container: `hedri-sakni-frontend`
   - Web App: http://localhost:5173

## 🚀 Usage

### Start All Services
```bash
./start.sh
```

### Stop All Services
```bash
./stop.sh
```

### View Logs
```bash
# All services
./logs.sh

# Specific service
./logs.sh backend
./logs.sh frontend
./logs.sh postgres
```

### Manual Docker Compose Commands

If you prefer manual control:

```bash
# Start services
docker-compose up -d

# Start with rebuild
docker-compose up -d --build

# Stop services
docker-compose down

# Stop and remove volumes (⚠️ deletes database!)
docker-compose down -v

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend

# Restart a service
docker-compose restart backend

# Check service status
docker-compose ps

# Execute command in container
docker-compose exec backend bash
docker-compose exec postgres psql -U postgres -d hedri_sakni
```

## 🔧 Configuration

### Environment Variables

Edit `.env` file to configure:

```env
# UiPath API Configuration
UIPATH_API_URL=https://your-uipath-instance.com/api
UIPATH_API_KEY=your-api-key
UIPATH_CLIENT_ID=your-client-id
UIPATH_CLIENT_SECRET=your-client-secret

# Admin Credentials (Change in production!)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### Default Credentials

**Login:**
- Username: `admin`
- Password: `admin123`

**Database:**
- Host: `localhost` (or `postgres` from within containers)
- Port: `5432`
- Database: `hedri_sakni`
- User: `postgres`
- Password: `postgres`

## 📊 Accessing Services

Once started, access:

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | React Admin Dashboard |
| Backend API | http://localhost:5000 | Flask REST API |
| API Docs | http://localhost:5000/api/docs | Swagger Documentation |
| Database | localhost:5432 | PostgreSQL (use client) |

## 🔍 Troubleshooting

### Services Won't Start

**Check if ports are already in use:**
```bash
# Check port 5432 (PostgreSQL)
lsof -i :5432

# Check port 5000 (Backend)
lsof -i :5000

# Check port 5173 (Frontend)
lsof -i :5173
```

**Kill processes using ports:**
```bash
lsof -ti:5432 | xargs kill -9
lsof -ti:5000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

### View Container Logs

```bash
# All logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart frontend
```

### Database Issues

**Connect to database:**
```bash
docker-compose exec postgres psql -U postgres -d hedri_sakni
```

**Reset database (⚠️ deletes all data!):**
```bash
docker-compose down -v
docker-compose up -d
```

### Rebuild Containers

If you made code changes:
```bash
docker-compose down
docker-compose up -d --build
```

### Clean Everything

Remove all containers, volumes, and images:
```bash
docker-compose down -v
docker system prune -a
```

## 🏭 Production Deployment

For production, use the production compose file:

```bash
# Copy and edit production environment
cp .env.example .env.prod
nano .env.prod

# Start with production config
docker-compose -f docker-compose.prod.yml up -d --build
```

**Production differences:**
- Uses Gunicorn instead of Flask dev server
- Builds optimized React production bundle
- Serves frontend with Nginx
- Frontend runs on port 80
- Enhanced security settings

## 📁 Docker Volumes

Data is persisted in Docker volumes:

- `postgres_data` - Database files
- `backend_logs` - Application logs

**View volumes:**
```bash
docker volume ls
```

**Backup database:**
```bash
docker-compose exec postgres pg_dump -U postgres hedri_sakni > backup.sql
```

**Restore database:**
```bash
cat backup.sql | docker-compose exec -T postgres psql -U postgres -d hedri_sakni
```

## 🔒 Security Notes

### For Production:

1. **Change default passwords:**
   - Update `ADMIN_PASSWORD` in `.env`
   - Update `POSTGRES_PASSWORD` in `docker-compose.yml`

2. **Use strong secrets:**
   - Generate random `SECRET_KEY`
   - Generate random `JWT_SECRET_KEY`

3. **Update CORS origins:**
   - Set `CORS_ORIGINS` to your production domain

4. **Use HTTPS:**
   - Add SSL certificates
   - Configure reverse proxy (Nginx/Traefik)

5. **Limit database access:**
   - Don't expose port 5432 externally
   - Use internal Docker network

## 🐛 Common Issues

### "Port already in use"
Stop the service using that port or change the port in `docker-compose.yml`

### "Cannot connect to database"
Wait a few seconds for PostgreSQL to fully start, or check logs: `docker-compose logs postgres`

### "Frontend shows connection error"
Backend might not be ready. Check: `docker-compose logs backend`

### "Changes not reflected"
Rebuild containers: `docker-compose up -d --build`

## 📝 Development Workflow

### Making Code Changes

**Backend changes:**
```bash
# Code is mounted as volume, changes auto-reload
# If you add new dependencies:
docker-compose down
docker-compose up -d --build
```

**Frontend changes:**
```bash
# Vite hot-reload works automatically
# If you add new dependencies:
docker-compose restart frontend
```

### Database Migrations

```bash
# Access backend container
docker-compose exec backend bash

# Run migrations (if using Flask-Migrate)
flask db upgrade
```

## 🎯 Next Steps

1. **Start the application:**
   ```bash
   ./start.sh
   ```

2. **Access the frontend:**
   Open http://localhost:5173

3. **Login:**
   - Username: `admin`
   - Password: `admin123`

4. **Configure UiPath:**
   - Edit `.env` with your UiPath credentials
   - Restart: `docker-compose restart backend`

5. **Start using:**
   - Create areas
   - Add customers
   - Schedule reservations
   - View analytics

## 📞 Support

For issues:
- Check logs: `./logs.sh`
- Review this guide
- Check main `README.md`

---

**Happy Dockering! 🐳**
