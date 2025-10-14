# Lambda Labs + Vercel Integration Guide

## 🎯 Overview

This guide will help you integrate your Lambda Labs GPU backend with your Vercel frontend deployment.

## 📋 Prerequisites

- ✅ Lambda Labs instance running with GPU chatbot API
- ✅ Vercel account with frontend deployed
- ✅ Lambda Labs instance with public IP or domain

---

## 🔧 Step 1: Get Your Lambda Labs Public URL

### Option A: Using Lambda Labs Public IP

1. **Get your Lambda Labs instance IP:**
   ```bash
   # On your Lambda Labs instance
   curl ifconfig.me
   ```
   
   Example output: `167.234.215.206`

2. **Your API URL will be:**
   ```
   http://167.234.215.206:8000
   ```

### Option B: Using a Custom Domain (Recommended for Production)

1. **Set up a reverse proxy with Nginx:**
   ```bash
   sudo apt install nginx -y
   ```

2. **Configure Nginx:**
   ```bash
   sudo nano /etc/nginx/sites-available/chatbot
   ```
   
   Add this configuration:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Enable the site:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

4. **Set up SSL with Let's Encrypt (Recommended):**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com
   ```

---

## 🌐 Step 2: Update Frontend Configuration

### Update `frontend/config.js`

Replace the Railway URL with your Lambda Labs URL:

```javascript
// Production API Configuration
// Lambda Labs GPU Backend
window.API_BASE_URL = "http://YOUR_LAMBDA_IP:8000";

// Or with custom domain:
// window.API_BASE_URL = "https://your-domain.com";
```

**Example:**
```javascript
window.API_BASE_URL = "http://167.234.215.206:8000";
```

---

## 🔐 Step 3: Configure CORS (Already Done!)

Your Lambda GPU API already has CORS configured to accept requests from any origin:

```python
# In services/chat_service/lambda_gpu_api.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Accepts all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For Production Security**, update to specific origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-vercel-app.vercel.app",
        "https://your-custom-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🚀 Step 4: Deploy Frontend to Vercel

### Option A: Using Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy from your local machine:**
   ```bash
   cd frontend
   vercel --prod
   ```

### Option B: Using Vercel Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository
4. Set the root directory to `frontend`
5. Click "Deploy"

---

## 🧪 Step 5: Test the Integration

### Test 1: Health Check

```bash
# Test Lambda backend directly
curl http://YOUR_LAMBDA_IP:8000/health

# Expected response:
{
  "status": "healthy",
  "message": "Lambda GPU Northeastern University Chatbot API is running",
  "response_time": 0.001,
  "model": "gpt-4o-mini",
  "device": "cuda",
  "gpu_available": true,
  "gpu_memory": "22.1 GB",
  "system_memory": "64.0 GB",
  "uptime": 123.45,
  "version": "2.0.0-lambda-gpu"
}
```

### Test 2: GPU Info

```bash
curl http://YOUR_LAMBDA_IP:8000/gpu-info

# Expected response:
{
  "gpu_available": true,
  "gpu_count": 1,
  "gpu_name": "NVIDIA A10",
  "gpu_memory_total": "22.1 GB",
  "gpu_memory_allocated": "2.3 GB",
  "gpu_memory_reserved": "2.5 GB",
  "cuda_version": "12.1"
}
```

### Test 3: Chat Endpoint

```bash
curl -X POST http://YOUR_LAMBDA_IP:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What programs does Northeastern University offer?"}'
```

### Test 4: Frontend Integration

1. Open your Vercel URL: `https://your-app.vercel.app`
2. Open browser console (F12)
3. Check for any CORS errors
4. Try asking a question
5. Verify the response comes from Lambda Labs

---

## 🔒 Step 6: Security Hardening (Production)

### 1. Firewall Configuration

```bash
# On Lambda Labs instance
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS (if using SSL)
sudo ufw allow 8000/tcp  # API (or restrict to specific IPs)
sudo ufw enable
```

### 2. Rate Limiting

Add rate limiting to your Lambda GPU API:

```python
# Install slowapi
pip install slowapi

# In lambda_gpu_api.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/chat")
@limiter.limit("10/minute")  # 10 requests per minute
async def chat(request: Request, chat_request: ChatRequest):
    # ... existing code
```

### 3. API Key Authentication (Optional)

```python
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@app.post("/chat")
async def chat(
    chat_request: ChatRequest,
    api_key: str = Depends(verify_api_key)
):
    # ... existing code
```

---

## 📊 Step 7: Monitor Your Deployment

### GPU Monitoring

```bash
# On Lambda Labs instance
./monitor_gpu.sh
```

### Application Logs

```bash
# View logs
journalctl -u chatbot -f

# Or if running in terminal
tail -f /var/log/chatbot.log
```

### Vercel Logs

```bash
vercel logs
```

---

## 🎯 Complete Integration Checklist

- [ ] Lambda Labs API running on port 8000
- [ ] Public IP or domain configured
- [ ] CORS enabled for Vercel domain
- [ ] `frontend/config.js` updated with Lambda URL
- [ ] Frontend deployed to Vercel
- [ ] Health check endpoint working
- [ ] Chat endpoint tested
- [ ] Frontend can communicate with backend
- [ ] SSL certificate installed (production)
- [ ] Firewall configured
- [ ] Monitoring setup

---

## 🐛 Troubleshooting

### Issue 1: CORS Error

**Error:** `Access to fetch at 'http://...' from origin 'https://...' has been blocked by CORS policy`

**Solution:**
1. Check CORS configuration in `lambda_gpu_api.py`
2. Add your Vercel domain to `allow_origins`
3. Restart the API server

### Issue 2: Connection Timeout

**Error:** `net::ERR_CONNECTION_TIMED_OUT`

**Solution:**
1. Check if Lambda Labs instance is running
2. Verify firewall allows port 8000
3. Test with `curl http://YOUR_IP:8000/health`
4. Check if API is bound to `0.0.0.0` not `127.0.0.1`

### Issue 3: SSL Certificate Error

**Error:** `Mixed Content: The page was loaded over HTTPS, but requested an insecure resource`

**Solution:**
1. Set up SSL on Lambda Labs with Let's Encrypt
2. Use HTTPS URL in `config.js`
3. Or deploy frontend without HTTPS (not recommended)

### Issue 4: API Not Responding

**Solution:**
```bash
# Check if API is running
ps aux | grep lambda_gpu_api

# Restart API
cd ~/Lambda_MGEN_GPT
source lambda_gpu_env/bin/activate
./start_lambda_gpu.sh
```

---

## 🚀 Quick Start Commands

### On Lambda Labs Instance:

```bash
# Start the API
cd ~/Lambda_MGEN_GPT
source lambda_gpu_env/bin/activate
./start_lambda_gpu.sh

# Monitor GPU
./monitor_gpu.sh

# Check API health
curl http://localhost:8000/health
```

### On Your Local Machine:

```bash
# Update frontend config
cd frontend
nano config.js  # Update API_BASE_URL

# Deploy to Vercel
vercel --prod

# Test integration
curl https://your-app.vercel.app
```

---

## 📚 Additional Resources

- [Lambda Labs Documentation](https://lambdalabs.com/service/gpu-cloud)
- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI CORS Guide](https://fastapi.tiangolo.com/tutorial/cors/)
- [Let's Encrypt SSL Setup](https://letsencrypt.org/getting-started/)

---

## 🎉 Success!

Once everything is set up, you'll have:

✅ **GPU-accelerated backend** on Lambda Labs (10-50x faster embeddings)  
✅ **Global CDN frontend** on Vercel (instant page loads worldwide)  
✅ **Production-ready** deployment with SSL and monitoring  
✅ **Cost-effective** solution using cloud GPU only when needed  

Your chatbot is now ready for production use! 🚀

