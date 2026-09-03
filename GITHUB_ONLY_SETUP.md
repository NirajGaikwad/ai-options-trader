# GitHub-Only Setup Guide

Complete platform deployment using **only GitHub** - no external services needed.

---

## 🎯 **What You Get**

✅ Code hosted on GitHub  
✅ CI/CD pipeline with GitHub Actions  
✅ Automatic testing on every push  
✅ Docker image built and stored on GitHub  
✅ Market monitor runs daily  
✅ Run platform in GitHub Codespaces (free tier)  
✅ Zero external dependencies  
✅ Free (except optional Codespaces upgrade)  

---

## 📋 **GitHub-Only Infrastructure**

```
GitHub Repository
    ↓
.github/workflows/deploy.yml (CI/CD)
    ↓
✅ Tests & Lint
✅ Build Docker Image
✅ Market Monitor
✅ Alerts
    ↓
GitHub Container Registry (GHCR)
    ↓
GitHub Codespaces (Run platform)
```

---

## 🚀 **Quick Setup (3 Steps)**

### **Step 1: Create GitHub Repository**

```bash
cd /c/Trade
git init
git add .
git commit -m "Initial commit: AI Options Trading Platform Phase 1"
```

### **Step 2: Push to GitHub**

1. Go to [github.com/new](https://github.com/new)
2. Name: `ai-options-trader`
3. Click "Create Repository"
4. Copy the URL

```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-options-trader.git
git branch -M main
git push -u origin main
```

### **Step 3: GitHub Actions Runs Automatically**

Your workflow runs automatically:
- ✅ **On every push** - Test and build
- ✅ **Daily at 08:00 IST** - Market monitor
- ✅ **Manual trigger** - Run via Actions tab

Done! ✅

---

## 🖥️ **Run Platform in GitHub Codespaces**

### **Option 1: Free Tier (Recommended)**

1. Go to your GitHub repository
2. Click **"Code"** → **"Codespaces"** tab
3. Click **"Create codespace on main"**
4. Wait 2-3 minutes for setup
5. In terminal:

```bash
# Setup (first time only)
python setup.py

# Start platform
./start-local.sh

# Access
http://localhost:8000/api/docs
```

✅ Platform running in cloud!

### **Option 2: Local Docker**

Use the Docker image built by GitHub Actions:

```bash
# Login to GitHub Container Registry
docker login ghcr.io -u USERNAME

# Pull image
docker pull ghcr.io/YOUR_USERNAME/ai-options-trader:main

# Run
docker run -p 8000:8000 ghcr.io/YOUR_USERNAME/ai-options-trader:main
```

---

## 📊 **How It Works**

### **Daily Market Monitor**

```
Every day at 08:00 IST:
├── GitHub Actions wakes up
├── Runs market_monitor.py
├── Checks market status
├── Sends alerts (if Slack configured)
└── Reports in workflow logs
```

### **Market Status**

| Status | Action | Alert |
|--------|--------|-------|
| **OPEN** (09:15-15:30) | Platform is running | ✅ Green alert |
| **About to open** (~60 min) | Start platform | 🟡 Yellow alert |
| **About to close** (~30 min) | Close positions | 🟠 Orange alert |
| **CLOSED** | Platform idle | 🔴 Red alert |

---

## 📈 **Workflow Features**

### **1. Continuous Integration**

On every push:
- ✅ Lint code (flake8)
- ✅ Type check (mypy)
- ✅ Security scan (bandit)
- ✅ Build Docker image
- ✅ Push to GitHub Container Registry

### **2. Daily Market Monitor**

Daily at 08:00 IST:
- ✅ Check if market is open/closing/opening
- ✅ Send Slack alerts (optional)
- ✅ Create GitHub Issues (optional)
- ✅ Log in workflow

### **3. Deployment Status**

After every build:
- ✅ Show build status
- ✅ List Docker images
- ✅ Provide Codespaces link
- ✅ Send Slack notification

---

## 🔧 **Configure Alerts (Optional)**

### **Slack Notifications**

1. Create Slack workspace or use existing
2. Get incoming webhook:
   - Go to [api.slack.com/apps](https://api.slack.com/apps)
   - Create New App
   - Activate Incoming Webhooks
   - Copy Webhook URL
3. Add GitHub Secret:
   - Go to repository → Settings → Secrets
   - Click "New repository secret"
   - Name: `SLACK_WEBHOOK`
   - Value: (paste webhook URL)

✅ Slack alerts now active!

### **GitHub Issues**

Automatically creates issues when market is about to open:
- No setup needed
- Reminder to start platform
- Linked to workflow run

---

## 📁 **What's in the Workflow**

### **`.github/workflows/deploy.yml`**

**Jobs:**
- `test-and-lint` - Quality checks
- `build-docker` - Build Docker image
- `market-monitor` - Market status check
- `deployment-check` - Verify deployment
- `notify` - Send alerts

**Triggers:**
- Push to main/develop
- Pull requests
- Schedule (daily 08:00 IST)
- Manual workflow_dispatch

### **`.github/scripts/market_monitor.py`**

**Detects:**
- Market open/close times
- About to open/close
- Weekends (no trading)

**Alerts:**
- Slack notifications
- GitHub Issues
- Workflow logs

---

## 📊 **View Your Workflows**

1. Go to your GitHub repository
2. Click **"Actions"** tab
3. See all workflow runs
4. Click a run to see details
5. View logs from each job

**Example workflow output:**
```
✅ test-and-lint - PASSED
✅ build-docker - PASSED (image: ghcr.io/.../main)
✅ market-monitor - Market is OPEN
✅ deployment-check - Ready
✅ notify - Slack notified
```

---

## 🎯 **Daily Workflow**

### **Morning (Before Market)**

```
08:00 IST → GitHub Actions runs
    ↓
Market opening in ~1 hour
    ↓
Alert: "Start your platform"
    ↓
You: Open GitHub Codespace
You: Run `python setup.py && ./start-local.sh`
    ↓
09:15 IST → Market open
    ↓
Platform ready for trading
```

### **During Market**

```
Your code changes
    ↓
Git push to GitHub
    ↓
Workflow runs automatically
    ↓
✅ Tests pass
✅ Docker image built
✅ Alerts sent
    ↓
New code deployed (next Codespace run)
```

### **Evening (Market Close)**

```
15:00 IST → Market about to close
    ↓
Alert: "Close positions"
    ↓
You: Close all trades
You: Record P&L
    ↓
15:30 IST → Market closed
    ↓
You: Stop platform
You: Git push any changes
```

---

## 💰 **Cost**

| Service | Cost |
|---------|------|
| GitHub | Free |
| GitHub Actions | Free (2000 min/month) |
| GitHub Container Registry | Free |
| Codespaces Free Tier | Free (60 hours/month) |
| Codespaces beyond free | ~$0.18/hour |
| **Total** | **Free** |

**Codespaces Pricing:**
- Free: 60 hours/month per user
- Beyond free: $0.18/hour
- For trading: ~20 hours/month = always free tier

---

## 🔒 **Security**

✅ Never commit secrets (`.gitignore` prevents it)  
✅ Use GitHub Secrets for sensitive data  
✅ Container registry is private by default  
✅ SSH access to Codespaces  
✅ GitHub Actions logs are secure  

**Best Practices:**
- Store API keys in GitHub Secrets
- Use `.gitignore` for `.env` files
- Review workflow logs for sensitive data
- Keep repository private if using real credentials

---

## 📚 **Using Docker Image**

### **From GitHub Container Registry**

```bash
# Login
docker login ghcr.io -u YOUR_USERNAME

# Pull latest image
docker pull ghcr.io/YOUR_USERNAME/ai-options-trader:main

# Pull specific version
docker pull ghcr.io/YOUR_USERNAME/ai-options-trader:latest
docker pull ghcr.io/YOUR_USERNAME/ai-options-trader:develop

# Run locally
docker run -p 8000:8000 -e PAPER_TRADING=true ghcr.io/YOUR_USERNAME/ai-options-trader:main

# Run with database
docker run -p 8000:8000 -e DATABASE_URL=postgresql://... ghcr.io/YOUR_USERNAME/ai-options-trader:main
```

---

## 🚀 **Production Deployment**

If you want to run on external hosting:

### **Option 1: AWS**
```bash
# Push image to AWS ECR
aws ecr get-login-password | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com
docker tag ghcr.io/YOUR_USERNAME/ai-options-trader:main YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/ai-options-trader:latest
docker push YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/ai-options-trader:latest

# Deploy to ECS/EKS
```

### **Option 2: Any Docker Registry**
```bash
# All Docker registries support GitHub container images
# Just pull and push to your registry
docker pull ghcr.io/YOUR_USERNAME/ai-options-trader:main
docker tag ghcr.io/YOUR_USERNAME/ai-options-trader:main YOUR_REGISTRY/ai-options-trader:latest
docker push YOUR_REGISTRY/ai-options-trader:latest
```

---

## ✅ **Verification Checklist**

- [ ] Repository created on GitHub
- [ ] Code pushed to main branch
- [ ] Workflows tab shows successful runs
- [ ] Docker image in GitHub Container Registry
- [ ] Market monitor runs daily
- [ ] (Optional) Slack webhook configured
- [ ] GitHub Codespaces can start
- [ ] Platform runs in Codespaces
- [ ] API docs accessible at `/api/docs`

---

## 🎯 **Next Steps**

1. **Set up GitHub repository** (5 min)
2. **Push code to GitHub** (2 min)
3. **Verify workflows run** (2 min)
4. **Test in Codespaces** (10 min)
5. **Proceed to Phase 2** (Technical Indicators)

---

## 📞 **Support**

- **GitHub Actions Docs:** https://docs.github.com/actions
- **Codespaces:** https://github.com/features/codespaces
- **Container Registry:** https://docs.github.com/packages/working-with-a-github-packages-registry/working-with-the-container-registry
- **Workflows:** https://docs.github.com/en/actions/using-workflows

---

## 🎉 **You Now Have**

✅ **GitHub-hosted codebase**  
✅ **Automatic CI/CD pipeline**  
✅ **Daily market monitoring**  
✅ **Docker image in GitHub registry**  
✅ **Free cloud environment (Codespaces)**  
✅ **Production-ready setup**  
✅ **Zero external dependencies**  

**Start trading from GitHub! 🚀**
