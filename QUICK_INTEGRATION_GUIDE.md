# 🚀 Quick Lambda + Vercel Integration Guide

## ⚡ 3-Minute Setup

### Step 1: Get Your Lambda IP (on Lambda Labs instance)
```bash
curl ifconfig.me
```
**Example output:** `167.234.215.206`

### Step 2: Run Auto-Setup Script
```bash
chmod +x setup_vercel_integration.sh
./setup_vercel_integration.sh
```

This script will:
- ✅ Detect your public IP
- ✅ Test your API
- ✅ Update frontend config
- ✅ Optionally deploy to Vercel

### Step 3: Manual Config (Alternative)

Edit `frontend/config.js`:
```javascript
window.API_BASE_URL = "http://YOUR_LAMBDA_IP:8000";
```

### Step 4: Deploy to Vercel
```bash
cd frontend
vercel --prod
```

### Step 5: Test
Open your Vercel URL and ask a question!

---

## 🧪 Quick Tests

### Test 1: API Health
```bash
curl http://YOUR_LAMBDA_IP:8000/health
```

### Test 2: GPU Status
```bash
curl http://YOUR_LAMBDA_IP:8000/gpu-info
```

### Test 3: Ask Question
```bash
curl -X POST http://YOUR_LAMBDA_IP:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Northeastern University?"}'
```

---

## 🔧 Troubleshooting

### Problem: Can't connect to API
**Solution:**
```bash
# Check if API is running
ps aux | grep lambda_gpu_api

# Restart if needed
cd ~/Lambda_MGEN_GPT
source lambda_gpu_env/bin/activate
./start_lambda_gpu.sh
```

### Problem: CORS error in browser
**Solution:** Already configured! CORS is enabled for all origins.

### Problem: Firewall blocking
**Solution:**
```bash
sudo ufw allow 8000/tcp
sudo ufw reload
```

---

## 📊 Monitor Your System

### GPU Monitoring
```bash
./monitor_gpu.sh
```

### API Logs
```bash
# If running in terminal, check the terminal output
# Or use journalctl if running as service
journalctl -u chatbot -f
```

### Vercel Logs
```bash
vercel logs
```

---

## 🎯 Your URLs

After setup, you'll have:

- **Lambda API:** `http://YOUR_IP:8000`
- **Health Check:** `http://YOUR_IP:8000/health`
- **GPU Info:** `http://YOUR_IP:8000/gpu-info`
- **Vercel Frontend:** `https://your-app.vercel.app`

---

## 🔒 Production Checklist

For production deployment:

- [ ] Set up custom domain
- [ ] Install SSL certificate (Let's Encrypt)
- [ ] Configure firewall rules
- [ ] Restrict CORS to your domain only
- [ ] Set up monitoring and alerts
- [ ] Configure rate limiting
- [ ] Set up automatic backups

See `LAMBDA_VERCEL_INTEGRATION.md` for detailed instructions.

---

## 💡 Pro Tips

1. **Use HTTPS in production** - Set up Let's Encrypt SSL
2. **Monitor GPU usage** - Run `./monitor_gpu.sh` regularly
3. **Keep API running** - Use systemd service or screen/tmux
4. **Update .env** - Add your OpenAI API key and ChromaDB credentials
5. **Test locally first** - Use `curl` to test before deploying frontend

---

## 🆘 Need Help?

1. Check `LAMBDA_VERCEL_INTEGRATION.md` for detailed guide
2. Check `LAMBDA_LABS_DEPLOYMENT_GUIDE.md` for Lambda setup
3. Check API logs for errors
4. Test each component individually

---

## 🎉 Success Indicators

You know it's working when:

✅ `curl http://YOUR_IP:8000/health` returns healthy status  
✅ GPU info shows NVIDIA A10 with memory stats  
✅ Frontend loads without console errors  
✅ Chatbot responds to questions  
✅ GPU monitoring shows activity when asking questions  

**You're all set! 🚀**

