# Automated Setup Guide

Complete automation scripts to set up the platform with minimal manual effort.

---

## Quick Start (Choose Your Method)

### **Method 1: One-Command Setup (Recommended)**

Works on **Windows, Linux, and macOS**:

```bash
python3 setup.py
```

This single command:
- ✅ Checks Python 3.11+
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Verifies PostgreSQL
- ✅ Checks Redis
- ✅ Creates database
- ✅ Initializes schema
- ✅ Guides you to next steps

**Time: ~5-10 minutes** (mostly dependency download)

---

### **Method 2: Platform-Specific Scripts**

#### **Windows (PowerShell)**

```powershell
.\setup-windows.ps1
```

Then start the app:
```powershell
.\start-local.ps1
```

#### **Linux/macOS (Bash)**

```bash
chmod +x setup-linux-macos.sh
./setup-linux-macos.sh
```

Then start the app:
```bash
chmod +x start-local.sh
./start-local.sh
```

---

### **Method 3: Manual (Step-by-Step)**

See [SETUP.md](./SETUP.md) → Step 1-10 (if you need more control)

---

## Running the Scripts

### **Windows PowerShell**

```powershell
# Open PowerShell as Administrator

cd c:\Trade

# Run setup
.\setup-windows.ps1

# When setup completes, start the app
.\start-local.ps1
```

**If execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup-windows.ps1
```

### **Linux/macOS Terminal**

```bash
cd /path/to/Trade

# Make scripts executable
chmod +x setup-linux-macos.sh start-local.sh

# Run setup
./setup-linux-macos.sh

# When setup completes, start the app
./start-local.sh
```

---

## What Each Script Does

### `setup.py` (Cross-Platform)

**Use this if you want one command that works everywhere.**

```bash
python3 setup.py
```

**Steps:**
1. Checks Python 3.11+
2. Creates virtual environment
3. Installs dependencies
4. Checks PostgreSQL
5. Checks Redis (optional)
6. Creates .env config
7. Creates PostgreSQL database
8. Initializes database schema
9. Verifies everything
10. Prints next steps

**Pros:**
- Single command
- Works on all platforms
- Automatic error detection
- Color-coded output

**Cons:**
- Less control
- May skip some optional steps

---

### `setup-windows.ps1` (Windows Only)

**Use if you want Windows-specific setup.**

```powershell
.\setup-windows.ps1
```

**Steps:**
1-10 (same as setup.py, but Windows-specific)

**Pros:**
- PowerShell integration
- Windows-native paths
- Better error messages
- Integration with Windows services

---

### `setup-linux-macos.sh` (Unix Only)

**Use if you want Linux/macOS-specific setup.**

```bash
./setup-linux-macos.sh
```

**Steps:**
1-10 (same as setup.py, but Unix-specific)

**Pros:**
- Bash integration
- Unix-native paths
- systemctl/brew awareness
- Better error messages

---

### `start-local.ps1` (Windows)

**Starts the application with checks.**

```powershell
.\start-local.ps1
```

**Does:**
- ✅ Activates virtual environment
- ✅ Checks PostgreSQL running
- ✅ Checks Redis running (optional)
- ✅ Starts FastAPI backend
- ✅ Reports any issues

---

### `start-local.sh` (Linux/macOS)

**Starts the application with checks.**

```bash
./start-local.sh
```

**Does:**
- ✅ Activates virtual environment
- ✅ Checks PostgreSQL running
- ✅ Checks Redis running (optional)
- ✅ Starts FastAPI backend
- ✅ Reports any issues

---

### `verify-setup.py` (Cross-Platform)

**Verify that everything is installed and working.**

```python
python verify-setup.py
```

**Checks:**
- ✅ Python 3.11+ installed
- ✅ Virtual environment exists
- ✅ Dependencies installed
- ✅ PostgreSQL installed and running
- ✅ Redis installed and running (optional)
- ✅ Configuration files present
- ✅ Safety defaults in place
- ✅ Database exists
- ✅ All project files present

**Output:**
```
==================================================
Verifying AI Options Trading Platform Setup
==================================================

1. Python Installation
✅ Python: Python 3.11.x
✅ pip: pip X.X.X

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
✅ ✓ backend/main.py
✅ ✓ backend/config/settings.py
...all files...

==================================================
Verification Summary
==================================================
✅ Setup verification PASSED!

You can now start the application:
  ./start-local.sh (Linux/macOS)
  .\start-local.ps1 (Windows)

Then access:
  http://localhost:8000/api/docs
```

---

## Complete Setup Workflow

### **Windows**

```powershell
# 1. Open PowerShell, navigate to project
cd c:\Trade

# 2. Run setup (one time)
.\setup-windows.ps1

# Follow the prompts, install any missing dependencies if needed

# 3. Start the app
.\start-local.ps1

# 4. In a new terminal, verify
python verify-setup.py

# 5. Test the API (in another new terminal)
curl http://localhost:8000/health

# 6. Open browser to see interactive API docs
# http://localhost:8000/api/docs
```

### **Linux/macOS**

```bash
# 1. Navigate to project
cd /path/to/Trade

# 2. Make scripts executable (one time)
chmod +x setup-linux-macos.sh start-local.sh verify-setup.py

# 3. Run setup (one time)
./setup-linux-macos.sh

# Follow the prompts

# 4. Start the app
./start-local.sh

# 5. In a new terminal, verify
python3 verify-setup.py

# 6. Test the API (in another new terminal)
curl http://localhost:8000/health

# 7. Open browser to see interactive API docs
# http://localhost:8000/api/docs
```

---

## Common Scenarios

### **Scenario 1: Fresh Installation**

First time setting up:

```bash
# One command setup
python3 setup.py

# Start app
./start-local.sh  (or .\start-local.ps1 on Windows)

# Verify
python3 verify-setup.py
```

### **Scenario 2: Already Have Python & Dependencies**

```bash
# Just initialize database
python3 scripts/init_db.py

# Start app
./start-local.sh
```

### **Scenario 3: Want to Verify Setup**

```bash
# Check everything
python3 verify-setup.py

# Fix any issues shown in report

# Start app
./start-local.sh
```

### **Scenario 4: Restart Services**

```bash
# If PostgreSQL isn't running:
# macOS: brew services start postgresql@15
# Linux: sudo systemctl start postgresql
# Windows: Start service from Services.msc

# If Redis isn't running:
# macOS: brew services start redis
# Linux: sudo systemctl start redis-server
# Windows: redis-server (if installed)

# Then start app
./start-local.sh
```

### **Scenario 5: Something Broke**

```bash
# Check what's wrong
python3 verify-setup.py

# See which component is missing/broken

# Fix it:
# - PostgreSQL not running? Start it
# - Dependency missing? pip install -r requirements.txt
# - Database issue? python3 scripts/init_db.py

# Verify again
python3 verify-setup.py

# Start app
./start-local.sh
```

---

## Troubleshooting Automated Setup

### **"Python 3.11+ not found"**

**Solution:** Install Python 3.11+
- Download: https://www.python.org/downloads/
- macOS: `brew install python@3.11`
- Linux: `sudo apt-get install python3.11`

### **"PostgreSQL not found"**

**Solution:** Install PostgreSQL 15+
- Download: https://www.postgresql.org/download/
- macOS: `brew install postgresql@15`
- Linux: `sudo apt-get install postgresql postgresql-contrib`

### **"Virtual environment already exists"**

**Solution:** Delete and recreate it
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

### **"Failed to install dependencies"**

**Solution:** Install pip packages manually
```bash
# Upgrade pip first
pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

### **"Database connection refused"**

**Solution:** Start PostgreSQL
```bash
# macOS
brew services start postgresql@15

# Linux
sudo systemctl start postgresql

# Windows
# Start from Services.msc or PostgreSQL installer
```

### **"Cannot execute script" (PowerShell)**

**Solution:** Change execution policy
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **"Permission denied" (Bash)**

**Solution:** Make scripts executable
```bash
chmod +x setup-linux-macos.sh start-local.sh verify-setup.py
```

---

## Verification Checklist

After running setup, verify with `python3 verify-setup.py`:

```
✅ Python 3.11+ installed
✅ Virtual environment exists
✅ Dependencies installed
✅ PostgreSQL 15+ installed
✅ PostgreSQL running
✅ Redis installed (optional)
✅ .env file exists
✅ Paper trading enabled
✅ Live trading disabled
✅ Database exists
✅ All project files present
```

If all checks pass, you're ready to run!

---

## What Next?

Once setup is complete:

1. **Start the app:**
   ```bash
   ./start-local.sh  # or .\start-local.ps1
   ```

2. **Test the API:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **View API documentation:**
   ```
   http://localhost:8000/api/docs
   ```

4. **Test endpoints:**
   - Click on any endpoint in Swagger UI
   - Click "Try it out"
   - Click "Execute"
   - See response

5. **Proceed to Phase 2:**
   - Build technical indicators
   - Add chart rendering
   - Create signal generation

---

## Script Reference

| Script | Platform | Purpose |
|--------|----------|---------|
| `setup.py` | All | One-command cross-platform setup |
| `setup-windows.ps1` | Windows | Windows-specific setup |
| `setup-linux-macos.sh` | Linux/macOS | Unix-specific setup |
| `start-local.ps1` | Windows | Start app with checks |
| `start-local.sh` | Linux/macOS | Start app with checks |
| `verify-setup.py` | All | Verify setup is complete |

---

## Time Estimates

| Method | Time | Complexity |
|--------|------|-----------|
| `python3 setup.py` | 5-10 min | Easiest |
| Platform-specific scripts | 5-10 min | Easy |
| Manual step-by-step | 15-20 min | Medium |

---

## Getting Help

If setup fails:

1. **Run verification:**
   ```bash
   python3 verify-setup.py
   ```
   This will show exactly what's missing.

2. **Check specific component:**
   - Python: `python3 --version`
   - pip: `pip --version`
   - PostgreSQL: `psql --version`
   - Redis: `redis-cli --version`

3. **Review logs:**
   - Setup scripts show detailed output
   - Save output if reporting issues

4. **Read main guides:**
   - [SETUP.md](./SETUP.md) - Detailed manual setup
   - [README.md](./README.md) - Project overview
   - [QUICKSTART.md](./QUICKSTART.md) - Quick reference

---

**Ready? Run one of these:**

```bash
# Easiest
python3 setup.py

# Or platform-specific
./setup-linux-macos.sh      # Linux/macOS
.\setup-windows.ps1         # Windows PowerShell
```

Then:
```bash
./start-local.sh            # Linux/macOS
.\start-local.ps1           # Windows

# In browser
http://localhost:8000/api/docs
```

**That's it! The platform will be running.**
