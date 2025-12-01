#!/bin/bash

# Land Reservation Admin System - Docker Quick Start Script

echo "🚀 Starting Land Reservation Admin System with Docker..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env file with your UiPath API credentials${NC}"
fi

# Stop any running containers
echo -e "${GREEN}🛑 Stopping any running containers...${NC}"
docker compose down 2>/dev/null || true

# Build and start containers
echo -e "${GREEN}🏗️  Building and starting containers...${NC}"
docker compose up -d --build

# Wait for services to be healthy
echo -e "${GREEN}⏳ Waiting for services to be ready...${NC}"
sleep 10

# Check if services are running
if docker compose ps | grep -q "Up"; then
    echo -e "${GREEN}✅ All services are running!${NC}"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${GREEN}🎉 Land Reservation Admin System is ready!${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📱 Frontend:     http://localhost:5173"
    echo "🔧 Backend API:  http://localhost:5000"
    echo "📚 API Docs:     http://localhost:5000/api/docs"
    echo ""
    echo "🔑 Default Login Credentials:"
    echo "   Username: admin"
    echo "   Password: admin123"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📋 Useful Commands:"
    echo "   View logs:        docker compose logs -f"
    echo "   Stop services:    docker compose down"
    echo "   Restart:          docker compose restart"
    echo "   View status:      docker compose ps"
    echo ""
    echo -e "${YELLOW}⚠️  Remember to configure .env with your UiPath API credentials${NC}"
else
    echo -e "${RED}❌ Failed to start services. Check logs with: docker compose logs${NC}"
    exit 1
fi
