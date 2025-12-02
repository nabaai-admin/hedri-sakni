#!/bin/bash

# Backend Entrypoint Script
# This script handles all initialization automatically

set -e

echo "🚀 Starting Land Reservation Backend..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Wait for PostgreSQL to be ready
echo -e "${YELLOW}⏳ Waiting for PostgreSQL to be ready...${NC}"
max_retries=30
retry_count=0

while ! pg_isready -h postgres -U postgres > /dev/null 2>&1; do
    retry_count=$((retry_count + 1))
    if [ $retry_count -ge $max_retries ]; then
        echo -e "${RED}❌ PostgreSQL is not available after $max_retries attempts${NC}"
        exit 1
    fi
    echo -e "${YELLOW}⏳ Waiting for PostgreSQL... (attempt $retry_count/$max_retries)${NC}"
    sleep 2
done

echo -e "${GREEN}✅ PostgreSQL is ready!${NC}"

# Create database tables
echo -e "${GREEN}📊 Creating database tables...${NC}"
python -c "
from app import create_app
from app.models import db
import os

env = os.getenv('FLASK_ENV', 'development')
app = create_app(env)

with app.app_context():
    db.create_all()
    
    # Auto-migration: Add link column if it doesn't exist
    try:
        from sqlalchemy import text
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE areas ADD COLUMN IF NOT EXISTS link VARCHAR(500);"))
            conn.commit()
            print('✅ Database schema updated (link column checked/added)')
    except Exception as e:
        print(f'⚠️ Schema update warning: {e}')
        
    print('✅ Database tables created successfully!')
"

# Check if initialization was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backend initialization complete!${NC}"
else
    echo -e "${RED}❌ Backend initialization failed!${NC}"
    exit 1
fi

# Start the application
echo -e "${GREEN}🚀 Starting Flask application...${NC}"
exec python run.py
