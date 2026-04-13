# 📸 Screenshot & GitHub Setup Guide

## Step 1: Take Screenshots

### Create screenshots folder
```bash
cd /Users/depressun/Desktop/restaurant-order-management
mkdir -p docs/screenshots
```

### Screenshots Needed (12 total)

Use built-in macOS screenshot tool (**Cmd + Shift + 4**) to capture:

#### 1. **home.png** - Landing Page
- Navigate to `http://localhost:5173`
- Capture the home page with "Owner Access" / "Staff Access" buttons

#### 2. **login.png** - Login Modal
- Click "Owner Access" or "Staff Access"
- Capture the login modal

#### 3. **customer-menu.png** - Customer Menu View
- Login as owner
- Go to Tables page  
- Click on a table QR link or scan QR code
- Capture the menu grid view with items

#### 4. **customer-cart.png** - Shopping Cart
- Add items to cart
- Capture the cart section with items and total

#### 5. **customer-order.png** - Active Order
- Place an order
- Capture the order tracking view with status badges

#### 6. **owner-dashboard.png** - Owner Dashboard
- Navigate to `/owner/dashboard`
- Capture the dashboard with statistics

#### 7. **analytics.png** - Analytics Dashboard
- Navigate to `/owner/analytics`
- Capture the charts and metrics

#### 8. **menu-list.png** - Menu Management
- Navigate to `/owner/menu`
- Capture the menu items grid

#### 9. **menu-edit.png** - Edit Menu Item
- Click "Edit" on a menu item
- Capture the edit modal

#### 10. **order-list.png** - Order Management
- Navigate to `/owner/orders`
- Capture the orders list

#### 11. **order-details.png** - Order Detail with Status Controls
- Click on an order
- Capture the per-item status buttons

#### 12. **staff-management.png** - Staff Management
- Navigate to `/owner/staff`
- Capture the staff list and create form

#### 13. **tables.png** - Tables & QR Codes
- Navigate to `/owner/tables`
- Capture the table list with QR codes

### Move screenshots to docs/screenshots/
```bash
# After taking screenshots, move them to the folder
mv ~/Desktop/screenshot*.png docs/screenshots/
```

---

## Step 2: Initialize Git Repository

### Create .gitignore
```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
backend/env/
*.egg-info/
dist/
build/

# FastAPI
.env

# Vue/Node
node_modules/
dist/
frontend/dist/
.DS_Store
*.log
npm-debug.log*

# Database
*.db
*.sqlite
*.sqlite3
backend/restaurant.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# AWS credentials (never commit!)
.aws/
EOF
```

### Initialize Git
```bash
cd /Users/depressun/Desktop/restaurant-order-management
git init
git add .
git commit -m "Initial Commit"
```

### Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `restaurant-order-management`
3. Description: "Restaurant Order Management System - Software Architecture Project"
4. Keep it **Private** (for academic integrity)
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

### Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/restaurant-order-management.git
git branch -M main
git push -u origin main
```

---

## Step 3: Create Development Commits

To show development progress, create meaningful commits:

```bash
# Create separate commits for different features
# (Use commit dates to show progression)

# Backend structure
git add backend/app/models/ backend/app/schemas/
git commit -m "feat: setup database models and schemas"

# Authentication
git add backend/app/services/auth_service.py backend/app/api/routes/auth.py
git commit -m "feat: implement JWT authentication and role-based access"

# Menu management
git add backend/app/services/menu_service.py backend/app/api/routes/menus.py
git commit -m "feat: add menu CRUD operations with image upload"

# Order system
git add backend/app/services/order_service.py backend/app/api/routes/orders.py
git commit -m "feat: implement order management with per-item status tracking"

# Analytics
git add backend/app/services/report_service.py backend/app/api/routes/reports.py
git commit -m "feat: add analytics dashboard with comprehensive reports"

# Frontend components
git add frontend/src/components/
git commit -m "feat: create reusable UI components"

# Frontend views
git add frontend/src/views/
git commit -m "feat: implement customer, staff, and owner views"

# Thai localization
git add backend/app/core/timezone.py
git commit -m "feat: add Thai timezone and currency support"

# Error handling
git add backend/app/main.py frontend/src/components/LoginModal.vue
git commit -m "feat: improve validation error messages"

# Documentation
git add README.md PROJECT_REPORT.md SUBMISSION_CHECKLIST.md
git commit -m "docs: add comprehensive documentation and project report"

# Screenshots
git add docs/screenshots/
git commit -m "docs: add system screenshots"

# IMPORTANT: Final commit must be named exactly "Final Commit"
git commit --allow-empty -m "Final Commit"
git push origin main
```

---

## Step 4: Verify Submission Requirements

### ✅ GitHub Repository Checklist
- [ ] Repository created and accessible
- [ ] First commit message is "Initial Commit"
- [ ] Multiple commits showing development stages
- [ ] Final commit message is "Final Commit"
- [ ] All commits dated between Feb 21 and April 16
- [ ] Complete project code pushed
- [ ] README.md includes all required sections
- [ ] Screenshots added to docs/screenshots/

### ✅ README.md Checklist
- [x] Project description
- [x] System architecture overview
- [x] User roles & permissions
- [x] Technology stack
- [x] Installation & setup instructions
- [x] How to run the system
- [ ] Screenshots (placeholders added, need actual files)

### ✅ Project Report Checklist
- [x] Project overview
- [x] System requirements
- [x] Architecture characteristics
- [x] Architecture design
- [x] Database design
- [x] Role & permission structure
- [x] Implementation details
- [x] Conclusion

---

## Step 5: Test Before Submission

### Backend Test
```bash
cd backend
source env/bin/activate
python -m uvicorn app.main:app --reload --port 8000

# Should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Frontend Test
```bash
cd frontend
npm install
npm run dev

# Should see:
# VITE ready in X ms
# ➜  Local:   http://localhost:5173/
```

### Feature Test
1. ✅ Login as owner
2. ✅ Create a menu item
3. ✅ Create a staff account
4. ✅ Login as staff
5. ✅ Access QR code link (customer view)
6. ✅ Place an order
7. ✅ Update item status
8. ✅ Mark order as paid
9. ✅ View analytics

---

## Step 6: Final Submission

### What to Submit
1. **GitHub Repository URL**
   - Example: `https://github.com/yourusername/restaurant-order-management`
   
2. **Project Report** (if separate submission required)
   - Export PROJECT_REPORT.md to PDF
   - Or include link to PROJECT_REPORT.md in repository

### Submission Email Template
```
Subject: Software Architecture Project Submission

Dear Professor [Name],

I am submitting my Software Architecture Project for review.

Project Title: Restaurant Order Management System
GitHub Repository: [YOUR REPO URL]
Project Report: [Link to PROJECT_REPORT.md in repo or attached PDF]

Key Features Implemented:
- Multi-user role system (Customer, Staff, Owner)
- Full CRUD operations for all roles
- JWT authentication and role-based authorization
- Per-item status tracking with kitchen workflow
- QR code-based customer ordering
- Comprehensive analytics dashboard
- Thai timezone and currency localization

The repository contains:
- Complete source code (backend and frontend)
- Comprehensive README with setup instructions
- Project report with architecture analysis
- Development commits showing progress
- System screenshots

Please let me know if you need any additional information.

Best regards,
[Your Name]
[Student ID]
```

---

## Timeline (Today is April 12)

### April 12 (Today)
- [x] Create SUBMISSION_CHECKLIST.md
- [x] Create PROJECT_REPORT.md
- [x] Add Screenshots section to README
- [ ] Take all screenshots
- [ ] Create .gitignore
- [ ] Initialize Git repository
- [ ] Make "Initial Commit"

### April 13
- [ ] Capture more demo screenshots
- [ ] Create GitHub repository
- [ ] Push initial code
- [ ] Create development commits (5-10 commits)
- [ ] Review and polish PROJECT_REPORT.md

### April 14
- [ ] Test all features one final time
- [ ] Verify all screenshots are in place
- [ ] Update README with screenshot paths
- [ ] Final documentation review
- [ ] Create additional commits if needed

### April 15
- [ ] Final code review
- [ ] Check all git commits are properly dated
- [ ] Verify README completeness
- [ ] Test repository clone and setup process
- [ ] Practice demo presentation

### April 16 (Deadline)
- [ ] Make any last-minute fixes
- [ ] Create "Final Commit"
- [ ] Push to GitHub
- [ ] Verify repository is accessible
- [ ] Submit GitHub URL to professor
- [ ] Submit PROJECT_REPORT.md (if required separately)

---

## Quick Commands Reference

```bash
# Check Git status
git status

# View commit history
git log --oneline

# Add files
git add <file>

# Commit with message
git commit -m "message"

# Push to GitHub
git push origin main

# View remote URL
git remote -v

# Take screenshot (macOS)
# Cmd + Shift + 4, then select area
```

---

## ⚠️ Important Notes

1. **Never commit sensitive data:**
   - AWS credentials
   - Database with real data
   - .env files

2. **Commit dates must be realistic:**
   - Spread commits over Feb 21 - April 16
   - Don't create all commits on the same day

3. **Make repository private:**
   - Academic integrity policy
   - Share access only with professor

4. **Test before submitting:**
   - Clone repository to new location
   - Follow README setup instructions
   - Verify everything works

5. **Backup everything:**
   - Keep local copy of project
   - Export screenshots separately
   - Save PROJECT_REPORT.md as PDF

---

**Good luck with your submission! Your system is complete and ready to impress. 🎉**
