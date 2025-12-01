# 🚀 Deployment Checklist

## Pre-Deployment

### Backend Configuration
- [ ] Update `SECRET_KEY` in `.env` with a strong random key
- [ ] Update `JWT_SECRET_KEY` in `.env` with a strong random key
- [ ] Change `ADMIN_PASSWORD` to a secure password
- [ ] Configure `DATABASE_URL` with production database credentials
- [ ] Set `UIPATH_API_URL` to production UiPath endpoint
- [ ] Configure `UIPATH_API_KEY`, `UIPATH_CLIENT_ID`, `UIPATH_CLIENT_SECRET`
- [ ] Update `CORS_ORIGINS` with production frontend URL
- [ ] Set `FLASK_ENV=production`
- [ ] Configure `LOG_FILE` path for production logs

### Frontend Configuration
- [ ] Update `VITE_API_URL` in `.env` to production backend URL
- [ ] Build production bundle: `npm run build`
- [ ] Test production build locally: `npm run preview`

### Database
- [ ] Create production PostgreSQL database
- [ ] Run migrations if using Flask-Migrate
- [ ] Backup strategy in place
- [ ] Set up automated backups

### Security
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable database encryption
- [ ] Review and update CORS settings
- [ ] Implement API key rotation strategy

## Deployment Steps

### Backend Deployment

#### Option 1: Using Gunicorn (Recommended)
```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Or with systemd service
sudo nano /etc/systemd/system/hedri-sakni.service
```

**Systemd Service File:**
```ini
[Unit]
Description=Hedri Sakni Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/hedri-sakni/backend
Environment="PATH=/path/to/hedri-sakni/backend/venv/bin"
ExecStart=/path/to/hedri-sakni/backend/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 run:app

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable hedri-sakni
sudo systemctl start hedri-sakni
```

#### Option 2: Using Docker
```dockerfile
# Dockerfile for backend
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

### Frontend Deployment

#### Option 1: Nginx
```bash
# Build
npm run build

# Copy to nginx
sudo cp -r dist/* /var/www/hedri-sakni/
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /var/www/hedri-sakni;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Option 2: Docker
```dockerfile
# Dockerfile for frontend
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

### Database Migration
```bash
# Backup current database
pg_dump hedri_sakni > backup_$(date +%Y%m%d).sql

# Restore to production
psql production_db < backup.sql
```

## Post-Deployment

### Verification
- [ ] Test login functionality
- [ ] Verify API endpoints via Swagger docs
- [ ] Test CRUD operations for all entities
- [ ] Verify background scheduler is running
- [ ] Test UiPath webhook integration
- [ ] Check analytics and reporting
- [ ] Verify Arabic RTL display
- [ ] Test on mobile devices

### Monitoring
- [ ] Set up application monitoring (e.g., Sentry)
- [ ] Configure log aggregation
- [ ] Set up uptime monitoring
- [ ] Configure alerts for errors
- [ ] Monitor database performance
- [ ] Track API response times

### Backup & Recovery
- [ ] Automated daily database backups
- [ ] Test restore procedure
- [ ] Document recovery steps
- [ ] Store backups in secure location

### Documentation
- [ ] Update API documentation
- [ ] Document deployment process
- [ ] Create runbook for common issues
- [ ] Document environment variables
- [ ] Create user manual

## Production Environment Variables

### Backend (.env)
```env
FLASK_ENV=production
SECRET_KEY=<generate-strong-random-key>
JWT_SECRET_KEY=<generate-strong-random-key>
DATABASE_URL=postgresql://user:pass@prod-db:5432/hedri_sakni
UIPATH_API_URL=https://prod-uipath.com/api
UIPATH_API_KEY=<production-key>
UIPATH_CLIENT_ID=<production-client-id>
UIPATH_CLIENT_SECRET=<production-secret>
ADMIN_USERNAME=<secure-username>
ADMIN_PASSWORD=<strong-password>
CORS_ORIGINS=https://your-domain.com
LOG_LEVEL=INFO
LOG_FILE=/var/log/hedri-sakni/app.log
PORT=5000
```

### Frontend (.env)
```env
VITE_API_URL=https://your-domain.com/api
```

## Security Hardening

### Backend
- [ ] Disable debug mode (`FLASK_ENV=production`)
- [ ] Use environment variables for all secrets
- [ ] Implement rate limiting
- [ ] Add request validation
- [ ] Enable CSRF protection
- [ ] Use secure session cookies
- [ ] Implement API versioning

### Database
- [ ] Use strong passwords
- [ ] Limit database user permissions
- [ ] Enable SSL connections
- [ ] Regular security updates
- [ ] Implement connection pooling

### Network
- [ ] Use HTTPS only
- [ ] Configure firewall rules
- [ ] Implement DDoS protection
- [ ] Use VPN for database access
- [ ] Regular security audits

## Performance Optimization

### Backend
- [ ] Enable database query caching
- [ ] Implement Redis for session storage
- [ ] Use connection pooling
- [ ] Optimize database indexes
- [ ] Enable gzip compression

### Frontend
- [ ] Enable CDN for static assets
- [ ] Implement lazy loading
- [ ] Optimize images
- [ ] Enable browser caching
- [ ] Minify assets

## Maintenance

### Regular Tasks
- [ ] Weekly: Review logs for errors
- [ ] Weekly: Check disk space
- [ ] Monthly: Update dependencies
- [ ] Monthly: Review security patches
- [ ] Quarterly: Performance audit
- [ ] Quarterly: Security audit

### Backup Schedule
- [ ] Daily: Database backup
- [ ] Weekly: Full system backup
- [ ] Monthly: Offsite backup
- [ ] Test restore: Monthly

## Rollback Plan

### If Deployment Fails
1. Stop new services
2. Restore previous version
3. Restore database from backup
4. Verify system functionality
5. Investigate and fix issues
6. Plan next deployment

### Rollback Commands
```bash
# Backend
sudo systemctl stop hedri-sakni
# Restore previous version
sudo systemctl start hedri-sakni

# Database
psql hedri_sakni < backup_previous.sql

# Frontend
# Restore previous dist folder
sudo cp -r dist_backup/* /var/www/hedri-sakni/
```

## Support & Maintenance

### Contact Information
- **Development Team:** [contact info]
- **System Admin:** [contact info]
- **Database Admin:** [contact info]

### Documentation Links
- API Documentation: `/api/docs`
- User Manual: `README.md`
- Quick Start: `QUICKSTART_AR.md`
- Project Summary: `PROJECT_SUMMARY.md`

---

**Last Updated:** $(date)
**Deployment Status:** ⏳ Pending
