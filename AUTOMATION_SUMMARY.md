# Automation Scripts Summary

Complete automation for setting up the AI Options Trading Platform locally.

---

## 📋 What You Get

**6 Automated Scripts** that handle all setup steps:

| Script | Purpose | Platform | Time |
|--------|---------|----------|------|
| `setup.py` | One-command setup | All | 5-10 min |
| `setup-windows.ps1` | Platform-specific setup | Windows | 5-10 min |
| `setup-linux-macos.sh` | Platform-specific setup | Linux/macOS | 5-10 min |
| `start-local.ps1` | Start app with checks | Windows | Instant |
| `start-local.sh` | Start app with checks | Linux/macOS | Instant |
| `verify-setup.py` | Verify everything works | All | 1 min |

---

## 🚀 Quick Start

### **Option 1: Easiest (One Command)**

Works on **any operating system**:

```bash
python3 setup.py
```

That's it! The script handles:
- ✅ Checking Python
- ✅ Creating virtual environment
- ✅ Installing 60+ dependencies
- ✅ Checking PostgreSQL
- ✅ Checking Redis
- ✅ Creating database
- ✅ Initializing schema
- ✅ Verifying everything

### **Option 2: Platform-Specific**

**Windows (PowerShell):**
```powershell
.\setup-windows.ps1
.\start-local.ps1
```

**Linux/macOS (Bash):**
```bash
./setup-linux-macos.sh
./start-local.sh
```

### **Option 3: Verify Existing Setup**

```bash
python3 verify-setup.py
```

Shows what's installed, what's missing, what's broken.

---

## 📝 Full Workflow

### **First Time Setup**

```bash
# 1. Navigate to project
cd /c/Trade

# 2. Run setup (5-10 minutes)
python3 setup.py

# 3. Start the application
./start-local.sh        # Linux/macOS
.\start-local.ps1       # Windows PowerShell

# 4. Test the API (in new terminal)
curl http://localhost:8000/health

# 5. Open browser
http://localhost:8000/api/docs
```

### **Subsequent Runs**

```bash
# Just start the app (services already running)
./start-local.sh        # or .\start-local.ps1

# In new terminal, test
curl http://localhost:8000/health

# Open browser
http://localhost:8000/api/docs
```

### **Verify Setup**

```bash
# Check everything is working
python3 verify-setup.py

# Should show all green checkmarks
```

---

## 🔍 What Each Script Does

### `setup.py` - One-Command Setup

```bash
python3 setup.py
```

**Automation:**
1. Checks Python 3.11+ installed
2. Creates virtual environment (`venv/`)
3. Upgrades pip
4. Installs all dependencies (60+ packages)
5. Checks PostgreSQL installed
6. Checks Redis installed (optional)
7. Creates `.env` config from template
8. Creates PostgreSQL database
9. Initializes database schema (20 tables)
10. Verifies everything

**Output:**
- Color-coded messages
- Clear next steps
- Error details if anything fails

---

### `setup-windows.ps1` - Windows Setup

```powershell
.\setup-windows.ps1
```

**Same as setup.py, but:**
- Uses PowerShell syntax
- Windows-specific commands
- Handles Windows paths correctly
- Better Windows service detection

---

### `setup-linux-macos.sh` - Unix Setup

```bash
./setup-linux-macos.sh
```

**Same as setup.py, but:**
- Uses Bash syntax
- Unix-specific commands
- brew/apt package manager awareness
- Handles Unix paths correctly

---

### `start-local.ps1` - Start Application (Windows)

```powershell
.\start-local.ps1
```

**Before starting:**
- ✅ Checks virtual environment exists
- ✅ Activates it
- ✅ Checks PostgreSQL running
- ✅ Checks Redis running (optional)
- ✅ Reports any issues

**Then:**
- 🚀 Starts FastAPI backend on http://localhost:8000

---

### `start-local.sh` - Start Application (Unix)

```bash
./start-local.sh
```

**Before starting:**
- ✅ Checks virtual environment exists
- ✅ Activates it
- ✅ Checks PostgreSQL running
- ✅ Checks Redis running (optional)
- ✅ Reports any issues

**Then:**
- 🚀 Starts FastAPI backend on http://localhost:8000

---

### `verify-setup.py` - Verify Installation

```bash
python3 verify-setup.py
```

**Checks:**
- ✅ Python 3.11+ installed
- ✅ Virtual environment exists
- ✅ FastAPI installed
- ✅ All dependencies installed
- ✅ PostgreSQL installed and running
- ✅ Redis installed and running (optional)
- ✅ .env file exists
- ✅ Paper trading enabled
- ✅ Live trading disabled
- ✅ Database exists
- ✅ All project files present

**Output Example:**
```
==================================================
Verifying AI Options Trading Platform Setup
==================================================

1. Python Installation
✅ Python: Python 3.11.x
✅ pip: pip 24.x

2. Virtual Environment
✅ Virtual environment exists
✅ FastAPI installed

3. PostgreSQL Database
✅ PostgreSQL: PostgreSQL 15.x
✅ PostgreSQL service is running
✅ Database 'options_trading' exists

4. Redis Cache
✅ Redis is running

5. Configuration
✅ .env file exists
✅ Paper trading is ENABLED (default)
✅ Live trading is DISABLED (default)

6. Project Files
✅ All project files present

==================================================
Verification Summary
==================================================
✅ Setup verification PASSED!

You can now start the application:
  ./start-local.sh (Linux/macOS)
  .\start-local.ps1 (Windows)
```

---

## 🛠️ Usage Examples

### **Example 1: Fresh Installation (Windows)**

```powershell
# Step 1: Navigate to project
cd c:\Trade

# Step 2: Run setup (automatic)
.\setup-windows.ps1

# Output will show progress...
# When done: "Setup Complete! Ready to run."

# Step 3: Start the app
.\start-local.ps1

# Output: "✅ PostgreSQL is running"
#         "✅ Redis is running"
#         "Starting FastAPI backend..."
#         "INFO: Uvicorn running on http://0.0.0.0:8000"

# Step 4: In new terminal, test
curl http://localhost:8000/health

# Step 5: Open browser
# http://localhost:8000/api/docs
```

### **Example 2: Fresh Installation (macOS/Linux)**

```bash
# Step 1: Navigate to project
cd ~/ai-options-trader

# Step 2: Make scripts executable
chmod +x setup-linux-macos.sh start-local.sh

# Step 3: Run setup (automatic)
./setup-linux-macos.sh

# Output will show progress...
# When done: "Setup Complete! Ready to run."

# Step 4: Start the app
./start-local.sh

# Output: "✅ PostgreSQL is running"
#         "✅ Redis is running"
#         "Starting FastAPI backend..."
#         "INFO: Uvicorn running on http://0.0.0.0:8000"

# Step 5: In new terminal, test
curl http://localhost:8000/health

# Step 6: Open browser
# http://localhost:8000/api/docs
```

### **Example 3: Verify Existing Installation**

```bash
# Check if everything is properly installed
python3 verify-setup.py

# Should show all ✅ marks

# If anything shows ❌, the script tells you how to fix it
```

### **Example 4: Fix Broken Setup**

```bash
# Check what's wrong
python3 verify-setup.py

# If it shows:
# ❌ PostgreSQL service is not running
# Then run:
brew services start postgresql@15  # macOS
# or
sudo systemctl start postgresql    # Linux
# or
# Start from Services.msc (Windows)

# Check again
python3 verify-setup.py

# Now it should show ✅
```

---

## ❌ Troubleshooting

### **"Python 3.11+ not found"**
- Install Python 3.11+ from python.org
- macOS: `brew install python@3.11`
- Linux: `sudo apt-get install python3.11`

### **"PostgreSQL not found"**
- Install PostgreSQL 15+ from postgresql.org
- macOS: `brew install postgresql@15`
- Linux: `sudo apt-get install postgresql postgresql-contrib`

### **"Permission denied" (Bash)**
- Make scripts executable: `chmod +x setup-linux-macos.sh start-local.sh`

### **"Cannot execute script" (PowerShell)**
- Change policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### **"Database connection refused"**
- PostgreSQL not running
- Start it:
  - macOS: `brew services start postgresql@15`
  - Linux: `sudo systemctl start postgresql`
  - Windows: Services.msc → postgresql-x64-15 → Start

### **"Redis not found" (warning)**
- Redis is optional
- Install if needed:
  - macOS: `brew install redis`
  - Linux: `sudo apt-get install redis-server`
  - Windows: Use WSL2 or Docker

---

## 📊 What Gets Set Up

After running setup scripts, you'll have:

```
Project Root (/c/Trade)
├── venv/                          # Python virtual environment
│   └── [60+ packages installed]
│
├── .env                           # Configuration (auto-created)
│   ├── PAPER_TRADING=true         ✅ Safe by default
│   └── LIVE_TRADING_ENABLED=false ✅ Safe by default
│
├── PostgreSQL (localhost:5432)
│   └── options_trading database
│       ├── 20 tables
│       ├── 20+ indexes
│       ├── user: trader
│       └── [schema initialized]
│
├── Redis (localhost:6379)
│   └── [running and ready]
│
└── Backend API (localhost:8000)
    └── [ready to start]
```

---

## 🎯 Next Steps After Setup

1. **Verify:** `python3 verify-setup.py`
2. **Start:** `./start-local.sh` (or `.\start-local.ps1`)
3. **Test:** `curl http://localhost:8000/health`
4. **Browse:** http://localhost:8000/api/docs
5. **Explore:** Test different endpoints
6. **Learn:** Read ARCHITECTURE.md
7. **Develop:** Proceed to Phase 2

---

## ⏱️ Time Breakdown

| Step | Time | Notes |
|------|------|-------|
| Python check | < 1 min | Usually instant |
| Venv creation | 1-2 min | One-time |
| Dependency install | 3-5 min | Largest time sink |
| PostgreSQL check | < 1 min | Usually instant |
| Database setup | 1-2 min | Creates tables |
| Verification | 1 min | Final checks |
| **Total** | **5-10 min** | First run only |

**Subsequent runs:** Just start the app (instant)

---

## 📋 File Locations

| File | Platform | Location |
|------|----------|----------|
| `setup.py` | All | `/c/Trade/setup.py` |
| `setup-windows.ps1` | Windows | `c:\Trade\setup-windows.ps1` |
| `setup-linux-macos.sh` | Unix | `/c/Trade/setup-linux-macos.sh` |
| `start-local.ps1` | Windows | `c:\Trade\start-local.ps1` |
| `start-local.sh` | Unix | `/c/Trade/start-local.sh` |
| `verify-setup.py` | All | `/c/Trade/verify-setup.py` |
| `.env` | All | `/c/Trade/.env` (created automatically) |

---

## ✅ Success Criteria

After setup, you should be able to:

- ✅ Run `python3 verify-setup.py` with all green checkmarks
- ✅ Start app with `./start-local.sh` or `.\start-local.ps1`
- ✅ Access API at http://localhost:8000/api/docs
- ✅ Get health check: `curl http://localhost:8000/health`
- ✅ Get market data: `curl http://localhost:8000/api/market/index/NIFTY`
- ✅ See paper trading enabled
- ✅ See live trading disabled

---

## 📞 Support

If something fails:

1. **Check logs:** Automation scripts show detailed error messages
2. **Verify:** Run `python3 verify-setup.py` to see what's wrong
3. **Fix:** Follow the fix instructions in verify output
4. **Try again:** Re-run the setup script

---

## 🎉 You're Ready!

Once automation completes, you have a fully functional local development environment ready for Phase 2 development.

**Start with:**
```bash
python3 setup.py
./start-local.sh
curl http://localhost:8000/health
```

**Then explore the API at:**
```
http://localhost:8000/api/docs
```

**Happy coding!**
