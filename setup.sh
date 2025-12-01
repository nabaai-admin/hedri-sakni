#!/bin/bash

# Land Reservation Admin System - Setup Script

echo "🚀 Setting up Land Reservation Admin System..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend Setup
echo -e "${GREEN}📦 Setting up Backend...${NC}"
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env from example
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit backend/.env with your configuration${NC}"
fi

# Create logs directory
mkdir -p logs

# Database setup
echo -e "${GREEN}🗄️  Database Setup${NC}"
echo "Please ensure PostgreSQL is running and create the database:"
echo "  createdb hedri_sakni"
read -p "Press enter when database is ready..."

cd ..

# Frontend Setup
echo -e "${GREEN}🎨 Setting up Frontend...${NC}"
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

cd ..

echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "To start the application:"
echo ""
echo "1. Start Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python run.py"
echo ""
echo "2. Start Frontend (in a new terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Access the application:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:5000"
echo "   API Docs: http://localhost:5000/api/docs"
echo ""
echo "Default login credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo -e "${YELLOW}⚠️  Remember to configure backend/.env with your UiPath API credentials${NC}"
