# Contributing & GitHub Setup Guide

## How to Upload to GitHub

### Step 1: Create Repository on GitHub
1. Go to [github.com](https://github.com) and sign in
2. Click "+" → "New repository"
3. Name it: `parking-management-system`
4. Add description: "A parking management system built with Python & Tkinter"
5. Choose "Public" or "Private"
6. Click "Create repository"

### Step 2: Initialize Local Git Repository

```bash
# Navigate to your project folder
cd parking-management-system

# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Parking management system OSSD project"

# Add remote repository (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/parking-management-system.git

# Push to GitHub (use 'main' or 'master' depending on GitHub default)
git branch -M main
git push -u origin main
```

## File Organization Summary

| File | Purpose |
|------|---------|
| `main.py` | Main application - run this file |
| `database.py` | Database operations (SQLite) |
| `dialogs.py` | UI dialog windows |
| `requirements.txt` | Dependencies (currently none needed) |
| `.gitignore` | Files to ignore in Git |
| `README.md` | Project documentation |

## Recommended Workflow

1. **Main Branch** - Production-ready code
2. **Features Branch** - New features (`git checkout -b feature/feature-name`)
3. **Bug Fix Branch** - Bug fixes (`git checkout -b bugfix/issue-number`)

## Common Git Commands

```bash
# Check status
git status

# Add changes
git add .
git add filename.py

# Commit changes
git commit -m "Descriptive message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main

# Create new branch
git checkout -b feature-name
```

## GitHub Best Practices

✅ Write clear commit messages
✅ Keep commits small and focused
✅ Update README for new features
✅ Use meaningful branch names
✅ Add .gitignore to exclude unnecessary files
✅ Document code with comments
✅ Test before pushing

## File Size Guide

This project structure keeps individual files small:
- `main.py` - ~200 lines (Main UI)
- `database.py` - ~130 lines (DB operations)
- `dialogs.py` - ~80 lines (Dialog windows)

## Total Project Size
- **Code**: ~410 lines
- **Database**: Generated at runtime (~100KB when active)
- **Easy to review and understand**

## Adding to GitHub Pages (Optional)

To create a project website:

1. Go to repository Settings
2. Scroll to "GitHub Pages"
3. Select "main" branch as source
4. Your README will be displayed at `https://yourusername.github.io/parking-management-system`

## License Suggestion

Add to your repository root as `LICENSE` file:

```
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge...
```

## Next Steps

1. Upload all files to GitHub
2. Add descriptive commit messages
3. Keep the repository updated with improvements
4. Document any new features
5. Consider adding issues/projects for future enhancements

---

**Happy coding! 🚀**
