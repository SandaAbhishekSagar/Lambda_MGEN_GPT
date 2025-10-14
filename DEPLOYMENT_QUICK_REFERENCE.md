# ⚡ Deployment Quick Reference Card

**Print this or keep it handy!**

---

## 🎯 **3-Step Deployment**

### **Step 1: Deploy Backend (Railway)**
```bash
git push origin main
# Wait 2-3 minutes
# Copy Railway URL
```

### **Step 2: Update Frontend Config**
```javascript
// frontend/config.js
window.API_BASE_URL = "https://YOUR-RAILWAY-URL.railway.app";
```

### **Step 3: Deploy Frontend (Vercel)**
```
1. Go to vercel.com/new
2. Import repository
3. Root directory: frontend
4. Deploy
```

---

## 🔗 **Your URLs**

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | `https://[your-project].vercel.app` | User interface |
| **Backend** | `https://[your-app].railway.app` | API server |
| **Health Check** | `https://[your-app].railway.app/health/enhanced` | Status |

---

## 🔑 **Railway Environment Variables**

```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
USE_CLOUD_CHROMA=true
```

---

## ✅ **Quick Test**

### **Test Backend:**
```bash
curl https://your-app.railway.app/health/enhanced
```
**Expected:** `{"status": "healthy"}`

### **Test Frontend:**
1. Visit Vercel URL
2. Press F12 (console)
3. Look for: "Health response status: 200"
4. Ask: "What is Northeastern University?"

---

## 💰 **Monthly Costs**

- Vercel: **$0** (Free)
- Railway: **$5-20** (Usage-based)
- ChromaDB: **$50** (Starter)
- OpenAI: **$5-30** (Per query)
- **Total: $60-100/month**

---

## 🐛 **Common Fixes**

### **CORS Error:**
```javascript
// Check frontend/config.js
window.API_BASE_URL = "https://correct-url.railway.app";  // No trailing /
```

### **404 Error:**
```bash
# Check Railway logs
railway logs
```

### **Timeout:**
```bash
# Verify environment variables in Railway
OPENAI_API_KEY=sk-...
```

---

## 📊 **Dashboards**

- **Vercel:** https://vercel.com/dashboard
- **Railway:** https://railway.app/dashboard
- **OpenAI:** https://platform.openai.com/usage

---

## 📁 **Key Files**

### **Backend:**
- `start.sh` - Startup script
- `railway.json` - Railway config
- `Dockerfile` - Container config
- `requirements.txt` - Dependencies

### **Frontend:**
- `config.js` - API URL
- `vercel.json` - Vercel config
- `index.html` - Main page
- `script.js` - Chat logic

---

## 🔄 **Update Workflow**

```bash
# 1. Make changes
git add .
git commit -m "Update"

# 2. Push
git push origin main

# 3. Auto-deploy
# Vercel: ~30 seconds
# Railway: ~2-3 minutes
```

---

## 🎯 **Success Checklist**

- [ ] Railway shows "Running"
- [ ] Vercel deployment succeeded
- [ ] Health check returns 200
- [ ] Frontend loads without errors
- [ ] Test query returns answer
- [ ] No CORS errors in console

---

## 📞 **Need Help?**

- Railway: https://railway.app/help
- Vercel: https://vercel.com/support
- OpenAI: https://help.openai.com

---

## 🎉 **You're Live!**

**Frontend:** Share your Vercel URL with users!

**Backend:** API is running and ready!

**Database:** 80,000 documents indexed!

**Your chatbot is production-ready! 🚀**

