# 🚀 Quick Start - Docker Compose

## One Command Setup

Simply run:

```bash
docker compose up -d
```

That's it! All services will be automatically installed and configured.

## What Happens Automatically

When you run `docker compose up -d`, the system automatically:

1. ✅ **Pulls/builds all Docker images** (PostgreSQL, Backend, Frontend)
2. ✅ **Starts PostgreSQL database**
3. ✅ **Waits for PostgreSQL to be ready**
4. ✅ **Creates all database tables automatically**
5. ✅ **Starts the Flask backend API**
6. ✅ **Starts the React frontend**

## Access the Application

After running `docker compose up -d`, wait about 30-60 seconds for all services to initialize, then access:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **API Documentation**: http://localhost:5000/api/docs

## Default Login Credentials

```
Username: admin
Password: admin123
```

## Configuration (Optional)

If you need to configure UiPath integration or other settings:

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your settings:
   ```bash
   nano .env
   ```

3. Restart the services:
   ```bash
   docker compose restart
   ```

## Useful Commands

```bash
# View logs from all services
docker compose logs -f

# View logs from specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres

# Stop all services
docker compose down

# Stop and remove all data (including database)
docker compose down -v

# Restart services
docker compose restart

# Rebuild and restart (after code changes)
docker compose up -d --build

# Check service status
docker compose ps
```

## Troubleshooting

### Services not starting?

Check the logs:
```bash
docker compose logs
```

### Database connection issues?

Wait a bit longer (up to 60 seconds) for PostgreSQL to fully initialize, then check:
```bash
docker compose logs postgres
docker compose logs backend
```

### Port already in use?

If ports 5000, 5173, or 5432 are already in use, you can modify them in `docker-compose.yml`.

### Reset everything

To completely reset and start fresh:
```bash
docker compose down -v
docker compose up -d --build
```

## Production Deployment

For production deployment, use:
```bash
docker compose -f docker-compose.prod.yml up -d
```

Make sure to:
- Set strong passwords in `.env`
- Configure proper CORS origins
- Set up SSL/TLS certificates
- Configure proper logging and monitoring

---

**Need help?** Check the full documentation in `README.md` or `DOCKER.md`
