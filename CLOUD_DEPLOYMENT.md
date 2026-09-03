# Cloud Deployment Guide - GitHub + Railway

Deploy the AI Options Trading Platform to **Railway** (cloud) with automatic market-hours startup.

---

## 🎯 **What You Get**

✅ Platform runs 24/7 in the cloud  
✅ Automatically starts at 09:15 IST (market open)  
✅ Automatically stops at 15:30 IST (market close)  
✅ Accessible from anywhere  
✅ Email/Slack alerts  
✅ Costs ~$5-10/month  

---

## 📋 **Prerequisites**

- ✅ GitHub account (free at github.com)
- ✅ Railway account (free at railway.app)
- ✅ Git installed locally

---

## 🚀 **Step 1: Create GitHub Repository**

### 1.1: Create New Repository

1. Go to [github.com/new](https://github.com/new)
2. Enter repository name: `ai-options-trader`
3. Description: "AI-Powered Intraday Options Trading Platform"
4. Choose **Public** (so Railway can access)
5. Click **Create Repository**

### 1.2: Initialize Local Repository

```bash
cd /c/Trade

# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Phase 1 complete

- FastAPI backend with 15+ endpoints
- PostgreSQL + TimescaleDB database (20 tables)
- Market data simulator
- Configuration management
- Docker containerization
- Comprehensive documentation"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/ai-options-trader.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

✅ Your code is now on GitHub!

---

## 🚂 **Step 2: Deploy to Railway**

### 2.1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Click "Login with GitHub"
3. Authorize Railway
4. Create new project

### 2.2: Connect GitHub Repository

1. In Railway dashboard, click "Create New Project"
2. Select "Deploy from GitHub repo"
3. Select your `ai-options-trader` repository
4. Click "Deploy"

Railway will:
- ✅ Detect Dockerfile
- ✅ Build Docker image
- ✅ Deploy application
- ✅ Assign URL

**Wait 5-10 minutes for deployment to complete.**

### 2.3: Add Database Services

Railway needs PostgreSQL and Redis.

**Add PostgreSQL:**
1. In Railway dashboard, click "Add"
2. Search "PostgreSQL"
3. Click "Add PostgreSQL"
4. Railway automatically links to your app

**Add Redis:**
1. Click "Add" again
2. Search "Redis"
3. Click "Add Redis"
4. Railway automatically links to your app

✅ Railway automatically sets:
- `DATABASE_URL` environment variable
- `REDIS_URL` environment variable

### 2.4: Configure Environment Variables

In Railway dashboard, go to your service and add:

```
ENVIRONMENT=production
PAPER_TRADING=true
LIVE_TRADING_ENABLED=false
DEBUG=false
API_PORT=8000
MAX_ACCOUNT_RISK_PER_TRADE=0.01
MAX_DAILY_LOSS_PERCENT=0.02
```

✅ Your platform is now deployed! Access it at your Railway URL.

---

## ⏰ **Step 3: Set Up Auto-Start at Market Open**

### 3.1: Create GitHub Secrets

For GitHub Actions to control your Railway deployment:

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add secrets:

```
RAILWAY_API_TOKEN=<your-railway-api-token>
RAILWAY_DEPLOYMENT_ID=<your-deployment-id>
SLACK_WEBHOOK=<optional-slack-url>
ALERT_EMAIL=your@email.com
```

**Get Railway API Token:**
1. Go to [Railway Dashboard](https://railway.app)
2. Account settings → API Tokens
3. Create new token
4. Copy and paste into GitHub Secrets

**Get Deployment ID:**
1. Railway dashboard → Your project
2. Click service
3. Settings tab → copy the ID

### 3.2: GitHub Actions Workflow

The workflow file `.github/workflows/deploy.yml` will:

- ✅ Run daily at 08:00 IST (before market opens)
- ✅ Check if market is open
- ✅ Start deployment if market is open
- ✅ Send alerts to Slack/Email
- ✅ Deploy on every code push

✅ No additional setup needed - it works automatically!

---

## 🔔 **Step 4: Set Up Notifications**

### **Slack Notifications (Optional)**

1. Create Slack workspace or use existing
2. Create Incoming Webhook:
   - Go to api.slack.com/apps
   - Create New App → From scratch
   - Choose workspace
   - Activate Incoming Webhooks
   - Create New Webhook URL
3. Add to GitHub Secrets: `SLACK_WEBHOOK`

### **Email Notifications**

The market monitor will show email notifications in logs.

---

## 🧪 **Testing Your Setup**

### **Test Deployment**

```bash
# Access your platform
https://your-railway-url.up.railway.app/api/docs

# Should show Swagger UI with all endpoints
```

### **Test Health Check**

```bash
curl https://your-railway-url.up.railway.app/health

# Should return:
# {"status": "ok", "paper_trading": true, "live_trading_enabled": false}
```

### **Test Market Monitor**

Manually run the market monitor:

```bash
python .github/scripts/market_monitor.py
```

Should show:
```
==================================================
MARKET STATUS REPORT
==================================================
Current Time (IST): 2026-09-03 10:30:00
Day of Week: Wednesday
Market Status: OPEN
Market Hours: 09:15 - 15:30 IST (Mon-Fri)
==================================================

📊 Market is OPEN
✅ Platform should be running
Action: Ensure deployment is active on Railway
```

---

## 📊 **How Market Auto-Start Works**

### **Market Schedule (IST)**

```
Monday-Friday:
- 08:00 IST: GitHub Actions checks market status
- 09:15 IST: Market OPENS → Platform STARTS (if not running)
- 15:30 IST: Market CLOSES → Platform can STOP
- 16:00 IST: After hours (platform stays running, optional)

Saturday-Sunday:
- No trading → Platform can be stopped (optional)
```

### **Automatic Actions**

| Time | Market | Platform | Action |
|------|--------|----------|--------|
| 08:00 | N/A | Any | GitHub Actions runs |
| 09:14 | About to open | Idle | Send Slack alert |
| 09:15 | OPEN | Starts | 🟢 Platform running |
| 15:29 | About to close | Running | Send alert |
| 15:30 | CLOSED | Stops | 🔴 Platform idle |

---

## 💰 **Cost Breakdown**

| Service | Cost | Notes |
|---------|------|-------|
| Railway App | $5-10/month | Based on runtime |
| PostgreSQL | $3-5/month | Included in Railway |
| Redis | $1-2/month | Included in Railway |
| GitHub Actions | Free | 2000 min/month free |
| **Total** | **~$5-10/month** | Very affordable |

**Optimization Tips:**
- Scale down when market is closed
- Use Railway's auto-pause for overnight
- Shared database reduces costs

---

## 🔐 **Security Checklist**

Before going live:

- [ ] Repository is **private** (if using real credentials)
- [ ] Secrets are in GitHub, not in code
- [ ] `.env` file is in `.gitignore`
- [ ] API keys are rotated regularly
- [ ] HTTPS is enabled (Railway does this by default)
- [ ] Firewall rules are configured
- [ ] Database backups are enabled
- [ ] Logs are monitored

---

## 📈 **Monitoring Your Deployment**

### **Railway Dashboard**

- View logs in real-time
- Monitor CPU/memory usage
- Check deployment status
- View recent deploys

### **GitHub Actions**

- Go to Actions tab
- See workflow runs
- View logs from market monitor
- Check deployment status

### **Application Logs**

Railway captures logs from your app:
```
docker logs <container-id>
```

---

## 🔧 **Troubleshooting**

### **Deployment Failed**

1. Check Railway logs
2. Verify Dockerfile builds locally
3. Check environment variables are set
4. Verify GitHub push succeeded

### **Market Monitor Not Running**

1. Check GitHub Actions is enabled
2. Verify secrets are set
3. Check workflow file syntax
4. View workflow run logs

### **Can't Access Platform**

1. Check Railway deployment is running
2. Verify URL is correct
3. Check health endpoint: `/health`
4. Check Railway logs for errors

### **Database Connection Issues**

1. Verify `DATABASE_URL` is set
2. Check database is running in Railway
3. Verify connection string is correct
4. Check network connectivity

---

## 🚀 **Next Steps**

1. ✅ Create GitHub repository
2. ✅ Deploy to Railway
3. ✅ Add database services
4. ✅ Configure auto-start
5. ✅ Test the platform
6. ✅ Proceed to Phase 2 (Technical Indicators)

---

## 📚 **Additional Resources**

- **Railway Docs:** https://docs.railway.app
- **GitHub Actions:** https://docs.github.com/actions
- **Docker Docs:** https://docs.docker.com
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/

---

## 🎯 **Success Criteria**

After setup, you should have:

- ✅ Code on GitHub (public repository)
- ✅ Running on Railway cloud
- ✅ Accessible 24/7 at unique URL
- ✅ PostgreSQL + Redis databases
- ✅ GitHub Actions configured
- ✅ Market monitor checking status
- ✅ Slack/Email alerts working
- ✅ Platform starts at 09:15 IST
- ✅ Platform stops at 15:30 IST
- ✅ Cost: ~$5-10/month

---

## 📞 **Support**

For issues with:

- **Railway:** https://support.railway.app
- **GitHub:** https://support.github.com
- **Your app:** Check logs and debug locally first

---

**You now have a production-grade cloud platform running 24/7! 🎉**

Next: Proceed to **Phase 2 - Technical Indicators**
