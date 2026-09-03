# Cloud Deployment - Quick Start (5 Steps)

Deploy to GitHub + Railway in 30 minutes.

---

## ⚡ **5-Step Quick Setup**

### **Step 1: Initialize Git (5 min)**

```bash
cd /c/Trade

# Initialize repository
git init
git add .
git commit -m "Initial commit: AI Options Trading Platform Phase 1"
```

### **Step 2: Create GitHub Repository (5 min)**

1. Go to [github.com/new](https://github.com/new)
2. Name: `ai-options-trader`
3. Description: "AI Options Trading Platform"
4. Choose **Public**
5. Click **Create Repository**

### **Step 3: Push to GitHub (2 min)**

```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-options-trader.git
git branch -M main
git push -u origin main
```

✅ Your code is on GitHub!

### **Step 4: Deploy to Railway (10 min)**

1. Go to [railway.app](https://railway.app)
2. Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `ai-options-trader`
6. Click "Deploy"

**Wait for build to complete (~5-10 min)**

### **Step 5: Add Databases (5 min)**

1. In Railway dashboard, click "Add"
2. Add **PostgreSQL**
3. Click "Add" again
4. Add **Redis**

✅ Your platform is live in the cloud!

---

## 🌐 **Access Your Platform**

After deployment:

```
API Docs: https://your-railway-url.up.railway.app/api/docs
Health Check: https://your-railway-url.up.railway.app/health
```

---

## ⏰ **Auto-Start at Market Hours**

The platform automatically starts when market opens:

1. **Set up GitHub Secrets:**
   - `RAILWAY_API_TOKEN`
   - `RAILWAY_DEPLOYMENT_ID`

2. **GitHub Actions runs daily at 08:00 IST**

3. **Market opens at 09:15 IST → Platform starts automatically**

---

## 📊 **Cost**

- **Railway**: ~$5-10/month
- **GitHub Actions**: Free
- **Total**: Very affordable

---

## 🎯 **Result**

✅ Platform runs 24/7 in cloud  
✅ Auto-starts at market open (09:15 IST)  
✅ Auto-stops at market close (15:30 IST)  
✅ Accessible from anywhere  
✅ Email/Slack alerts  

---

## 📚 **Full Setup Guide**

See [CLOUD_DEPLOYMENT.md](./CLOUD_DEPLOYMENT.md) for detailed instructions.

---

## 🚀 **Next: Phase 2**

After cloud deployment works:
1. Verify platform is running
2. Test endpoints at `/api/docs`
3. Proceed to Phase 2: Technical Indicators

---

**Done! Your platform is in the cloud and running 24/7! 🎉**
