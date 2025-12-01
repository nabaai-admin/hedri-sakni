#!/bin/bash

# GitHub Repository Setup Script for Hedri Sakni

echo "🚀 Setting up GitHub repository for Hedri Sakni..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Repository details
REPO_NAME="hedri-sakni"
REPO_DESCRIPTION="Land Reservation Admin System - Full-stack application with Flask, React, and PostgreSQL"

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}║          GitHub Repository Setup - Hedri Sakni               ║${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed. Please install Git first.${NC}"
    exit 1
fi

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${YELLOW}⚠️  GitHub CLI (gh) is not installed.${NC}"
    echo ""
    echo "You have two options:"
    echo ""
    echo "Option 1: Install GitHub CLI (Recommended)"
    echo "  Ubuntu/Debian: sudo apt install gh"
    echo "  macOS: brew install gh"
    echo ""
    echo "Option 2: Create repository manually"
    echo "  1. Go to https://github.com/new"
    echo "  2. Create a private repository named: ${REPO_NAME}"
    echo "  3. Don't initialize with README, .gitignore, or license"
    echo "  4. Run this script again"
    echo ""
    read -p "Do you want to continue with manual setup? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    MANUAL_SETUP=true
else
    MANUAL_SETUP=false
fi

# Initialize Git repository
echo -e "${GREEN}📦 Initializing Git repository...${NC}"
git init

# Add all files
echo -e "${GREEN}📝 Adding files to Git...${NC}"
git add .

# Create initial commit
echo -e "${GREEN}💾 Creating initial commit...${NC}"
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

# Create GitHub repository
if [ "$MANUAL_SETUP" = false ]; then
    echo ""
    echo -e "${YELLOW}🔐 GitHub Authentication Required${NC}"
    echo "You need to authenticate with GitHub CLI."
    echo "This will open your browser for authentication."
    echo ""
    read -p "Press Enter to continue..."
    
    # Check if already authenticated
    if ! gh auth status &> /dev/null; then
        echo -e "${GREEN}Authenticating with GitHub...${NC}"
        gh auth login
    fi
    
    echo ""
    echo -e "${GREEN}🏗️  Creating private GitHub repository...${NC}"
    gh repo create "$REPO_NAME" \
        --private \
        --description "$REPO_DESCRIPTION" \
        --source=. \
        --remote=origin \
        --push
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Repository created and code pushed successfully!${NC}"
        echo ""
        echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${BLUE}║                                                              ║${NC}"
        echo -e "${BLUE}║                    🎉 Success!                               ║${NC}"
        echo -e "${BLUE}║                                                              ║${NC}"
        echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        
        # Get repository URL
        REPO_URL=$(gh repo view --json url -q .url)
        echo -e "${GREEN}📍 Repository URL:${NC}"
        echo "   $REPO_URL"
        echo ""
        echo -e "${GREEN}🔗 Clone URL (HTTPS):${NC}"
        echo "   $(gh repo view --json url -q .url).git"
        echo ""
        echo -e "${GREEN}🔗 Clone URL (SSH):${NC}"
        echo "   $(gh repo view --json sshUrl -q .sshUrl)"
        echo ""
    else
        echo -e "${RED}❌ Failed to create repository${NC}"
        exit 1
    fi
else
    echo ""
    echo -e "${YELLOW}📋 Manual Setup Instructions:${NC}"
    echo ""
    echo "1. Go to: https://github.com/new"
    echo "2. Repository name: ${REPO_NAME}"
    echo "3. Description: ${REPO_DESCRIPTION}"
    echo "4. Visibility: Private ✓"
    echo "5. Do NOT initialize with README, .gitignore, or license"
    echo "6. Click 'Create repository'"
    echo ""
    echo "After creating the repository, GitHub will show you commands."
    echo "Use these commands to push your code:"
    echo ""
    echo -e "${GREEN}git remote add origin https://github.com/YOUR_USERNAME/${REPO_NAME}.git${NC}"
    echo -e "${GREEN}git branch -M main${NC}"
    echo -e "${GREEN}git push -u origin main${NC}"
    echo ""
    read -p "Press Enter when you've created the repository and are ready to add the remote..."
    
    echo ""
    read -p "Enter your GitHub username: " GITHUB_USERNAME
    
    # Add remote
    git remote add origin "https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
    
    # Rename branch to main
    git branch -M main
    
    # Push to GitHub
    echo -e "${GREEN}📤 Pushing to GitHub...${NC}"
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Code pushed successfully!${NC}"
        echo ""
        echo -e "${GREEN}📍 Repository URL:${NC}"
        echo "   https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
        echo ""
    else
        echo -e "${RED}❌ Failed to push to GitHub${NC}"
        echo "You may need to authenticate. Try:"
        echo "  git push -u origin main"
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}║                  Next Steps                                  ║${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "✅ Your code is now on GitHub (private repository)"
echo "✅ You can clone it on any machine"
echo "✅ You can collaborate with team members"
echo ""
echo "📝 To clone on another machine:"
echo "   git clone https://github.com/YOUR_USERNAME/${REPO_NAME}.git"
echo ""
echo "🔄 To update the repository:"
echo "   git add ."
echo "   git commit -m 'Your commit message'"
echo "   git push"
echo ""
echo "🎉 All done!"
