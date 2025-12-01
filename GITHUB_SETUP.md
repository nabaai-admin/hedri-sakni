# 🚀 GitHub Setup Guide

## Quick Setup (Automated)

Run the setup script:
```bash
./setup-github.sh
```

The script will:
1. ✅ Initialize Git repository
2. ✅ Add all files
3. ✅ Create initial commit
4. ✅ Create private GitHub repository
5. ✅ Push code to GitHub

---

## Prerequisites

### Option 1: Using GitHub CLI (Recommended)

Install GitHub CLI:

**Ubuntu/Debian:**
```bash
sudo apt install gh
```

**macOS:**
```bash
brew install gh
```

**Other systems:**
Visit: https://cli.github.com/

### Option 2: Manual Setup

You'll need:
- Git installed
- GitHub account
- Personal Access Token (for authentication)

---

## Automated Setup (with GitHub CLI)

1. **Run the script:**
   ```bash
   ./setup-github.sh
   ```

2. **Authenticate when prompted:**
   - Browser will open for GitHub login
   - Follow the authentication steps

3. **Done!**
   - Repository created
   - Code pushed
   - You'll see the repository URL

---

## Manual Setup (without GitHub CLI)

### Step 1: Initialize Git

```bash
git init
git add .
git commit -m "Initial commit: Land Reservation Admin System"
```

### Step 2: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `hedri-sakni`
3. Description: `Land Reservation Admin System - Full-stack application`
4. Visibility: **Private** ✓
5. **Do NOT** initialize with README, .gitignore, or license
6. Click **Create repository**

### Step 3: Push Code

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/hedri-sakni.git
git branch -M main
git push -u origin main
```

If prompted for credentials:
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your password)

---

## Creating a Personal Access Token

If you need to create a token:

1. Go to: https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Note: `hedri-sakni-access`
4. Expiration: Choose duration
5. Scopes: Select **repo** (full control)
6. Click **Generate token**
7. **Copy the token** (you won't see it again!)
8. Use this token as your password when pushing

---

## After Setup

### Clone on Another Machine

```bash
git clone https://github.com/YOUR_USERNAME/hedri-sakni.git
cd hedri-sakni
```

### Update Repository

```bash
# Make changes to your code
git add .
git commit -m "Description of changes"
git push
```

### Pull Latest Changes

```bash
git pull
```

### View Repository

```bash
# If using GitHub CLI
gh repo view --web

# Or visit
https://github.com/YOUR_USERNAME/hedri-sakni
```

---

## Troubleshooting

### Authentication Failed

**Problem:** Git asks for password but rejects it

**Solution:** Use Personal Access Token instead of password
1. Create token at: https://github.com/settings/tokens
2. Use token as password

### Permission Denied

**Problem:** `Permission denied (publickey)`

**Solution:** Set up SSH key or use HTTPS with token

### Repository Already Exists

**Problem:** Repository name already taken

**Solution:** 
1. Delete the existing repository on GitHub
2. Or use a different name in the script

### Large Files Warning

**Problem:** Git warns about large files

**Solution:** Files over 100MB should use Git LFS
```bash
git lfs install
git lfs track "*.large-extension"
```

---

## Repository Structure

Your repository will include:

```
hedri-sakni/
├── backend/           # Flask API
├── frontend/          # React App
├── docker-compose.yml # Docker setup
├── README.md          # Main documentation
├── DOCKER.md          # Docker guide
├── .gitignore         # Ignored files
└── setup-github.sh    # This setup script
```

---

## Security Notes

### Files Excluded (in .gitignore)

- ✅ `.env` files (secrets)
- ✅ `node_modules/`
- ✅ `venv/`
- ✅ `__pycache__/`
- ✅ Log files
- ✅ Database files

### What's Included

- ✅ Source code
- ✅ Docker configuration
- ✅ Documentation
- ✅ `.env.example` (template only)

**Important:** Never commit `.env` files with real credentials!

---

## Collaboration

### Add Collaborators

1. Go to repository settings
2. Manage access → Invite a collaborator
3. Enter their GitHub username
4. Choose permission level

### Branch Protection

For production:
1. Settings → Branches
2. Add rule for `main` branch
3. Enable:
   - Require pull request reviews
   - Require status checks
   - Include administrators

---

## Next Steps

After pushing to GitHub:

1. ✅ **Set up CI/CD** (GitHub Actions)
2. ✅ **Add branch protection**
3. ✅ **Configure secrets** for deployment
4. ✅ **Add collaborators** if working in team
5. ✅ **Create releases** for versions

---

## Useful Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Merge branch
git merge feature-name

# Discard changes
git checkout -- filename

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View remote URL
git remote -v
```

---

## GitHub Features to Use

- **Issues** - Track bugs and features
- **Projects** - Organize work
- **Wiki** - Extended documentation
- **Actions** - CI/CD automation
- **Releases** - Version management
- **Insights** - Repository analytics

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review GitHub documentation
3. Check Git configuration: `git config --list`

---

**Happy coding! 🚀**
