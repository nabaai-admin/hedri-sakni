#!/bin/bash

# Quick Git initialization script

echo "🚀 Initializing Git repository..."

# Initialize Git
git init

# Add all files
echo "📝 Adding files..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Land Reservation Admin System

- Full-stack application with Flask backend and React frontend
- PostgreSQL database with complete schema
- Docker Compose setup for easy deployment
- Background job scheduler for automated reservations
- UiPath API integration
- Arabic RTL support
- Complete CRUD operations for Areas, Customers, and Reservations
- Analytics dashboard with filtering and reporting
- Swagger API documentation
- Comprehensive documentation and guides"

echo ""
echo "✅ Git repository initialized and committed!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Create repository on GitHub:"
echo "   → Go to: https://github.com/new"
echo "   → Name: hedri-sakni"
echo "   → Visibility: Private"
echo "   → Don't initialize with README"
echo "   → Click 'Create repository'"
echo ""
echo "2. Add remote and push:"
echo "   → Replace YOUR_USERNAME with your GitHub username"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/hedri-sakni.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
