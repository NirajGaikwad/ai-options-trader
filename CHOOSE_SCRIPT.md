# Which Script Should You Use?

Quick decision guide for choosing the right automation script.

---

## 🤔 Decision Tree

### **Question 1: What's your operating system?**

#### **Windows**
- Go to → **Windows Decision**

#### **macOS or Linux**
- Go to → **Unix Decision**

---

## **Windows Decision**

### **Question: Do you prefer PowerShell or one command?**

#### **I want PowerShell scripts (Windows-native)**
```powershell
.\setup-windows.ps1
.\start-local.ps1
```
✅ Best for: Windows users who like PowerShell integration

#### **I want one command that works everywhere**
```bash
python3 setup.py
.\start-local.ps1
```
✅ Best for: Simplicity, cross-platform compatibility

---

## **Unix Decision (macOS/Linux)**

### **Question: Do you prefer Bash or one command?**

#### **I want Bash scripts (Unix-native)**
```bash
./setup-linux-macos.sh
./start-local.sh
```
✅ Best for: Linux/macOS users who like Bash integration

#### **I want one command that works everywhere**
```bash
python3 setup.py
./start-local.sh
```
✅ Best for: Simplicity, cross-platform compatibility

---

## 📊 Quick Comparison

| Use Case | Script | Speed | Complexity | Platform |
|----------|--------|-------|-----------|----------|
| **One command** | `setup.py` | 5-10 min | Easiest | All |
| **Windows PowerShell** | `setup-windows.ps1` | 5-10 min | Easy | Windows |
| **Linux/macOS Bash** | `setup-linux-macos.sh` | 5-10 min | Easy | Unix |
| **Verify setup** | `verify-setup.py` | 1 min | Very Easy | All |

---

## 🎯 My Recommendation

### **If you're new**: Use `setup.py`
```bash
python3 setup.py
```
- One command
- Works on Windows, Mac, Linux
- Guides you through everything
- Shows clear next steps

### **If you know your OS**: Use platform-specific
- **Windows**: `.\setup-windows.ps1`
- **macOS/Linux**: `./setup-linux-macos.sh`

### **If you want to verify**: Use `verify-setup.py`
```bash
python3 verify-setup.py
```

---

## 📍 Current Location

You're running on: **Windows** (based on paths like `c:/Trade`)

### **Recommended for you:**

**Option 1: Easiest (Recommended)**
```bash
python3 setup.py
```

**Option 2: Windows-native**
```powershell
.\setup-windows.ps1
```

Both will take ~5-10 minutes and handle all setup automatically.

---

## 🚀 Complete Setup → Run Sequence

### **Option A: Recommended (One Command)**

```bash
# 1. Setup (first time only)
python3 setup.py

# 2. Start application (every time you want to code)
.\start-local.ps1

# 3. Verify (optional)
python3 verify-setup.py
```

### **Option B: Windows PowerShell Way**

```powershell
# 1. Setup (first time only)
.\setup-windows.ps1

# 2. Start application (every time you want to code)
.\start-local.ps1

# 3. Verify (optional)
python3 verify-setup.py
```

---

## ⏱️ Time Commitment

| Stage | Time | Action |
|-------|------|--------|
| **Setup** (first time) | 5-10 min | Run setup script |
| **Subsequent starts** | Instant | Run start script |
| **Verification** | 1 min | Run verify script |

---

## ✅ What Happens

### **Setup Script Does:**
1. ✅ Checks Python 3.11+
2. ✅ Creates virtual environment
3. ✅ Installs 60+ packages
4. ✅ Checks/creates database
5. ✅ Initializes 20 tables
6. ✅ Verifies everything
7. ✅ Tells you next steps

### **Start Script Does:**
1. ✅ Activates virtual environment
2. ✅ Checks services are running
3. ✅ Starts FastAPI backend
4. ✅ Reports any issues

### **Verify Script Does:**
1. ✅ Checks all components
2. ✅ Reports what's working/missing
3. ✅ Suggests fixes if needed

---

## 🎓 Script Usage Patterns

### **Pattern 1: First-Time Setup**
```bash
# First time? Run setup
python3 setup.py

# Then verify
python3 verify-setup.py

# Then start
.\start-local.ps1
```

### **Pattern 2: Every Day Development**
```bash
# You already did setup, just start
.\start-local.ps1

# Or if services aren't running, verify
python3 verify-setup.py
```

### **Pattern 3: Troubleshooting**
```bash
# Something broke? Check
python3 verify-setup.py

# See what's wrong, follow fix suggestions

# Verify fixed
python3 verify-setup.py

# Continue
.\start-local.ps1
```

---

## 🚨 Common Questions

### **Q: Which script do I run first?**
**A:** Setup script (one time):
- `python3 setup.py` (recommended), or
- `.\setup-windows.ps1` (Windows)

### **Q: Which script do I run every day?**
**A:** Start script:
- `.\start-local.ps1` (Windows), or
- `./start-local.sh` (macOS/Linux)

### **Q: What if something fails?**
**A:** Run verify script:
- `python3 verify-setup.py`
- It tells you what's wrong and how to fix it

### **Q: Can I use setup.py on Windows?**
**A:** Yes! It works on all platforms:
```bash
python3 setup.py
```

### **Q: Can I use setup-windows.ps1 on macOS?**
**A:** No, it's Windows-only. Use:
```bash
python3 setup.py  # or
./setup-linux-macos.sh
```

---

## 🎯 Start Here

**You need to run ONE of these:**

### **Easiest Way (Works on Windows, Mac, Linux)**
```bash
python3 setup.py
```

### **Windows Way**
```powershell
.\setup-windows.ps1
```

### **Mac/Linux Way**
```bash
./setup-linux-macos.sh
```

**Pick one and run it. It will handle everything else.**

---

## 📋 After Setup

You'll be able to:

1. **Start the app:**
   ```bash
   .\start-local.ps1        # Windows
   ./start-local.sh         # Mac/Linux
   ```

2. **Test the API:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **View documentation:**
   ```
   http://localhost:8000/api/docs
   ```

4. **Proceed to Phase 2:**
   Build technical indicators and start developing!

---

## 🎉 Ready?

**Choose your script from above and run it!**

Most first-time users choose:
```bash
python3 setup.py
```

**Then:**
```bash
.\start-local.ps1
```

**That's it!**
