# ✅ Custom Domain + SSL Setup Checklist

## 📋 Complete Setup Guide

Follow these steps in order for a professional, permanent HTTPS solution.

---

## 🤔 Why Do We Need This?

### **The Problem:**

Your current setup has a critical issue:

```
❌ Vercel Frontend: HTTPS (https://lambda-mgen-gpt.vercel.app/)
❌ Lambda Backend: HTTP (http://167.234.215.206:8000)
```

**Result:** Browser blocks the connection with "Mixed Content Error"

```
Mixed Content: The page at 'https://...' was loaded over HTTPS,
but requested an insecure resource 'http://...'.
This request has been blocked; the content must be served over HTTPS.
```

### **Why Browsers Block This:**

Modern browsers **block HTTP requests from HTTPS pages** for security reasons:

1. **Security Risk:** HTTP traffic is unencrypted and can be intercepted
2. **Data Integrity:** Attackers could modify HTTP responses
3. **Privacy:** Sensitive data (API keys, user queries) exposed
4. **Browser Policy:** Chrome, Firefox, Safari all enforce this

### **What This Solution Provides:**

✅ **HTTPS for Backend** - Encrypted communication  
✅ **SSL Certificate** - Verified secure connection  
✅ **Professional Domain** - Your own branded URL  
✅ **Browser Compatibility** - No more "Mixed Content" errors  
✅ **Production Ready** - Meets modern security standards  

### **The Benefits:**

#### 1. **Security** 🔒
- **Encrypted traffic:** All data between frontend and backend is encrypted
- **No man-in-the-middle attacks:** SSL prevents interception
- **Secure API keys:** Your OpenAI API key is protected
- **User privacy:** User queries are encrypted in transit

#### 2. **Professional** 💼
- **Custom domain:** `https://chatbot.yourdomain.com` vs `http://167.234.215.206:8000`
- **Trust indicators:** Browser shows padlock icon 🔒
- **Brand identity:** Your own domain name
- **Credibility:** Users trust HTTPS sites more

#### 3. **Performance** ⚡
- **HTTP/2 support:** Faster than HTTP/1.1
- **Browser caching:** Better caching with HTTPS
- **CDN compatibility:** Can add Cloudflare later
- **No security warnings:** No browser blocking

#### 4. **Compliance** ✅
- **GDPR compliant:** Encrypted data transmission required
- **PCI DSS:** If handling any payments in future
- **Best practices:** Follows modern web standards
- **SEO benefits:** Google ranks HTTPS sites higher

#### 5. **Reliability** 🎯
- **Permanent URL:** Domain doesn't change
- **Auto-renewal:** SSL certificate renews automatically
- **No rate limits:** Unlike free tunneling services
- **24/7 availability:** Professional hosting

### **Without This Solution:**

❌ Frontend can't connect to backend  
❌ Chatbot doesn't work on Vercel  
❌ "Mixed Content" errors in console  
❌ Users see security warnings  
❌ Can't use HTTPS features  
❌ Not production-ready  

### **With This Solution:**

✅ Frontend connects securely to backend  
✅ Chatbot works perfectly on Vercel  
✅ No browser errors or warnings  
✅ Professional, branded experience  
✅ Production-ready deployment  
✅ 10-50x GPU performance maintained  

### **Cost vs. Value:**

**Investment:** $7-15/year for domain + $0 for SSL (free)  
**Return:** Professional, secure, production-ready chatbot

**Alternative costs:**
- Ngrok Pro: $8/month = $96/year (still temporary URLs)
- Cloud providers with SSL: $20-50/month = $240-600/year
- **This solution: $7-15/year** ⭐

### **Real-World Impact:**

**Before (HTTP):**
```javascript
// Console errors
❌ Mixed Content: blocked
❌ device: "cpu" (using Railway fallback)
❌ Chatbot not working
❌ Users can't access
```

**After (HTTPS):**
```javascript
// Console success
✅ device: "cuda" (GPU acceleration!)
✅ gpu_embeddings: 'enabled'
✅ Response time: 2-5 seconds
✅ Professional HTTPS URL
✅ No errors or warnings
```

### **Technical Comparison:**

| Aspect | HTTP (Current) | HTTPS (This Solution) |
|--------|----------------|----------------------|
| **Security** | ❌ Unencrypted | ✅ Encrypted |
| **Browser Support** | ❌ Blocked | ✅ Fully supported |
| **Professional** | ❌ IP address | ✅ Custom domain |
| **SSL Certificate** | ❌ None | ✅ Free (Let's Encrypt) |
| **Production Ready** | ❌ No | ✅ Yes |
| **Cost** | Free | $7-15/year |
| **Maintenance** | Manual | Auto-renewal |
| **Performance** | Same | Same + HTTP/2 |

### **Why Not Use Alternatives?**

#### **Option: Ngrok (Temporary)**
- ❌ URL changes on restart
- ❌ Rate limits (40 req/min free)
- ❌ Not suitable for production
- ❌ $8/month for stable URLs
- ✅ Good for quick testing only

#### **Option: Cloudflare Tunnel**
- ✅ Free HTTPS
- ⚠️ More complex setup
- ⚠️ Requires Cloudflare account
- ⚠️ Additional configuration
- ✅ Good alternative if you prefer

#### **Option: Custom Domain + SSL (This Solution)**
- ✅ Professional and permanent
- ✅ Simple setup (one script)
- ✅ Free SSL (Let's Encrypt)
- ✅ Auto-renewal
- ✅ **Best for production** ⭐

### **Summary:**

**You need this because:**
1. **Browsers require HTTPS** - Mixed content is blocked
2. **Security matters** - Protect your API keys and user data
3. **Professional appearance** - Custom domain builds trust
4. **Production readiness** - Meets modern web standards
5. **Long-term solution** - Permanent, not temporary
6. **Cost-effective** - Only $7-15/year
7. **GPU performance** - Maintains 10-50x speed advantage

**Bottom line:** Without HTTPS, your chatbot won't work on Vercel. With this solution, you get a professional, secure, production-ready deployment for less than $15/year.

---

## **Phase 1: Domain Purchase (5-10 minutes)**

### ☐ **Step 1.1: Choose a Domain Provider**

Recommended providers:
- [ ] **Namecheap** - https://www.namecheap.com (~$8-12/year)
- [ ] **Cloudflare** - https://www.cloudflare.com/products/registrar/ (~$9/year)
- [ ] **Porkbun** - https://porkbun.com (~$7-10/year)

### ☐ **Step 1.2: Purchase Domain**

Choose a domain name:
- [ ] `chatbot-yourdomain.com`
- [ ] `api-yourdomain.com`
- [ ] Use existing domain with subdomain

**Cost:** $7-15/year

---

## **Phase 2: DNS Configuration (5 minutes + wait time)**

### ☐ **Step 2.1: Add A Record**

In your domain provider's DNS settings:

```
Type: A Record
Name: @ (for root) or api/chatbot (for subdomain)
Value: 167.234.215.206
TTL: 300 or Auto
```

**Screenshots for common providers:**

#### Namecheap:
1. Domain List → Manage
2. Advanced DNS
3. Add New Record → A Record

#### Cloudflare:
1. DNS → Add Record
2. Type: A
3. Proxy status: DNS only (gray cloud)

#### GoDaddy:
1. My Products → DNS
2. Add → A Record

### ☐ **Step 2.2: Wait for DNS Propagation**

```bash
# Check DNS propagation
dig +short your-domain.com

# Should return: 167.234.215.206
```

Online checker: https://dnschecker.org/

**Wait time:** 5-30 minutes (can take up to 48 hours)

---

## **Phase 3: SSL Setup on Lambda Labs (10 minutes)**

### ☐ **Step 3.1: Verify Lambda Labs API is Running**

```bash
# On Lambda Labs instance
ps aux | grep lambda_gpu_api

# If not running:
cd ~/Lambda_MGEN_GPT
source lambda_gpu_env/bin/activate
./start_lambda_gpu.sh
```

### ☐ **Step 3.2: Run SSL Setup Script**

```bash
# Make script executable
chmod +x setup_ssl_lambda.sh

# Run setup (replace with your domain)
./setup_ssl_lambda.sh your-domain.com

# Examples:
# ./setup_ssl_lambda.sh chatbot.mydomain.com
# ./setup_ssl_lambda.sh api.mydomain.com
```

**What the script does:**
1. ✅ Installs Nginx
2. ✅ Configures reverse proxy
3. ✅ Installs Certbot
4. ✅ Obtains SSL certificate
5. ✅ Sets up auto-renewal

### ☐ **Step 3.3: Verify SSL Certificate**

```bash
# Test HTTPS endpoint
curl https://your-domain.com/health

# Should return JSON with no SSL errors
```

**Expected response:**
```json
{
  "status": "healthy",
  "device": "cuda",
  "gpu_available": true,
  "model": "gpt-4o-mini"
}
```

---

## **Phase 4: Update Frontend (5 minutes)**

### ☐ **Step 4.1: Update config.js**

Edit `frontend/config.js`:

```javascript
// Replace with your actual domain
window.API_BASE_URL = "https://your-domain.com";
```

**Examples:**
```javascript
window.API_BASE_URL = "https://chatbot.mydomain.com";
window.API_BASE_URL = "https://api.mydomain.com";
window.API_BASE_URL = "https://mydomain.com";
```

### ☐ **Step 4.2: Test Locally**

```bash
# Open frontend locally
cd frontend
python -m http.server 8080

# Open: http://localhost:8080
# Check console (F12) for errors
```

### ☐ **Step 4.3: Deploy to Vercel**

```bash
cd frontend
vercel --prod
```

---

## **Phase 5: Verification (5 minutes)**

### ☐ **Step 5.1: Test API Directly**

```bash
# Health check
curl https://your-domain.com/health

# GPU info
curl https://your-domain.com/gpu-info

# Documents count
curl https://your-domain.com/documents
```

### ☐ **Step 5.2: Test Frontend**

1. Open Vercel URL: `https://lambda-mgen-gpt.vercel.app/`
2. Open browser console (F12)
3. Check for:
   - [ ] No "Mixed Content" errors
   - [ ] `device: "cuda"` in health response
   - [ ] `gpu_embeddings: 'enabled'`
   - [ ] No SSL certificate errors

### ☐ **Step 5.3: Test Chatbot**

1. Ask a question
2. Verify response appears
3. Check response time (should be fast with GPU)
4. Verify sources are displayed

---

## **Phase 6: Monitoring & Maintenance**

### ☐ **Step 6.1: Set Up Monitoring**

```bash
# On Lambda Labs, monitor GPU
./monitor_gpu.sh

# Check Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Check SSL certificate expiry
sudo certbot certificates
```

### ☐ **Step 6.2: Verify Auto-Renewal**

```bash
# Check certbot timer
sudo systemctl status certbot.timer

# Test renewal (dry run)
sudo certbot renew --dry-run
```

**SSL certificates auto-renew every 90 days** ✅

---

## **Troubleshooting**

### Issue 1: DNS Not Resolving

**Check:**
```bash
dig +short your-domain.com
# Should return: 167.234.215.206
```

**Solution:**
- Wait longer (DNS can take up to 48 hours)
- Verify A record is correct in DNS settings
- Try different DNS checker: https://dnschecker.org/

### Issue 2: SSL Certificate Failed

**Error:** `Failed to obtain certificate`

**Common causes:**
1. Domain doesn't resolve to Lambda IP yet
2. Port 80 is blocked
3. Another service using port 80

**Solution:**
```bash
# Check if port 80 is open
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check what's using port 80
sudo netstat -tlnp | grep :80

# Stop conflicting service
sudo systemctl stop apache2  # if Apache is running
```

### Issue 3: Nginx Configuration Error

**Solution:**
```bash
# Test Nginx config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Check Nginx status
sudo systemctl status nginx
```

### Issue 4: Still Getting "Mixed Content" Error

**Solution:**
1. Clear browser cache: `Ctrl + Shift + Delete`
2. Hard refresh: `Ctrl + Shift + R`
3. Verify `config.js` uses `https://` not `http://`
4. Check browser console for actual URL being called
5. Redeploy to Vercel

---

## **Cost Breakdown**

| Item | Cost | Frequency |
|------|------|-----------|
| Domain | $7-15 | Per year |
| SSL Certificate | **FREE** | Auto-renews |
| Lambda Labs GPU | ~$0.50-1/hr | When running |
| Vercel Hosting | **FREE** | Unlimited |
| **Total** | **$7-15/year** | **+ GPU usage** |

---

## **Performance Metrics**

After setup, you should see:

### API Response Times:
- Health check: < 10ms
- GPU info: < 50ms
- Chat query: 2-5 seconds

### Frontend:
- Page load: < 1 second (Vercel CDN)
- First response: 2-5 seconds (GPU acceleration)
- Subsequent responses: 2-5 seconds

### GPU Utilization:
- Idle: 0-5%
- Processing query: 30-80%
- Memory usage: 2-4 GB (out of 22.1 GB)

---

## **Security Checklist**

- [x] HTTPS enabled (SSL certificate)
- [x] Auto-renewal configured
- [ ] Firewall configured (optional but recommended)
- [ ] Rate limiting (optional but recommended)
- [ ] API authentication (optional for private use)

**Optional: Add Firewall Rules**
```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP (for SSL renewal)
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

---

## **Maintenance Schedule**

### Daily:
- [ ] Check API health: `curl https://your-domain.com/health`

### Weekly:
- [ ] Monitor GPU usage: `./monitor_gpu.sh`
- [ ] Check Nginx logs for errors

### Monthly:
- [ ] Verify SSL certificate: `sudo certbot certificates`
- [ ] Update system: `sudo apt update && sudo apt upgrade`
- [ ] Check disk space: `df -h`

### Every 3 Months:
- [ ] Review and optimize ChromaDB
- [ ] Update Python dependencies
- [ ] Review API usage and costs

---

## **Success Criteria**

You'll know everything is working when:

✅ **DNS:**
- `dig +short your-domain.com` returns `167.234.215.206`

✅ **SSL:**
- `curl https://your-domain.com/health` works without errors
- Browser shows padlock icon 🔒

✅ **Frontend:**
- No "Mixed Content" errors in console
- Console shows `device: "cuda"`
- Chatbot responds to questions

✅ **Performance:**
- Response times: 2-5 seconds
- GPU memory usage visible in logs
- No timeouts or errors

---

## **Quick Reference Commands**

```bash
# Check DNS
dig +short your-domain.com

# Test API
curl https://your-domain.com/health

# Check SSL certificate
sudo certbot certificates

# Restart Nginx
sudo systemctl restart nginx

# Monitor GPU
./monitor_gpu.sh

# Check API logs
sudo tail -f /var/log/nginx/access.log

# Deploy frontend
cd frontend && vercel --prod
```

---

## **Support Resources**

- **Domain Setup:** Your registrar's documentation
- **SSL Issues:** https://letsencrypt.org/docs/
- **Nginx:** https://nginx.org/en/docs/
- **Lambda Labs:** https://lambdalabs.com/service/gpu-cloud
- **Vercel:** https://vercel.com/docs

---

## **Next Steps After Setup**

1. **Monitor Performance:**
   - Set up uptime monitoring (e.g., UptimeRobot)
   - Monitor GPU usage and costs
   - Track API response times

2. **Optimize:**
   - Add caching if needed
   - Implement rate limiting
   - Add API authentication for private use

3. **Scale:**
   - Add load balancing if traffic increases
   - Consider multiple Lambda instances
   - Implement CDN for static assets

---

**Your production-ready, GPU-accelerated chatbot with HTTPS! 🚀🔒**

**Estimated Total Setup Time:** 30-60 minutes (including DNS wait)
**Monthly Cost:** ~$1-2 for domain + GPU usage
**Performance:** 10-50x faster than CPU with professional HTTPS

