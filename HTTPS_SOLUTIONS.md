# 🔒 HTTPS Solutions for Lambda Labs + Vercel

## 🚨 Problem

Your Vercel frontend uses **HTTPS**, but Lambda Labs backend uses **HTTP**, causing a "Mixed Content" error:

```
Mixed Content: The page at 'https://lambda-mgen-gpt.vercel.app/' was loaded over HTTPS,
but requested an insecure resource 'http://167.234.215.206:8000/health/enhanced'.
This request has been blocked; the content must be served over HTTPS.
```

**Browsers block HTTP requests from HTTPS pages for security.**

---

## ✅ Solution Options

### **Option 1: Custom Domain + SSL (Best for Production)** ⭐

**Pros:**
- ✅ Professional and permanent
- ✅ Free SSL certificate (Let's Encrypt)
- ✅ Auto-renewal
- ✅ Best security

**Cons:**
- ❌ Requires domain purchase ($10-15/year)
- ❌ DNS setup needed (5-30 min wait)

**Steps:**

1. **Buy a domain** (e.g., from Namecheap, GoDaddy, etc.)

2. **Point domain to Lambda IP:**
   ```
   Type: A Record
   Name: @ (or your subdomain)
   Value: 167.234.215.206
   TTL: 300
   ```

3. **Run SSL setup on Lambda Labs:**
   ```bash
   chmod +x setup_ssl_lambda.sh
   ./setup_ssl_lambda.sh your-domain.com
   ```

4. **Update frontend config:**
   ```javascript
   window.API_BASE_URL = "https://your-domain.com";
   ```

5. **Deploy to Vercel:**
   ```bash
   cd frontend && vercel --prod
   ```

**Cost:** ~$10-15/year for domain

---

### **Option 2: Ngrok Tunnel (Quick Testing)** ⚡

**Pros:**
- ✅ Instant HTTPS
- ✅ No domain needed
- ✅ Free tier available

**Cons:**
- ❌ Temporary URL (changes on restart)
- ❌ Rate limits (40 req/min on free tier)
- ❌ Not suitable for production

**Steps:**

1. **Sign up at:** https://dashboard.ngrok.com/signup

2. **Get authtoken:** https://dashboard.ngrok.com/get-started/your-authtoken

3. **Configure ngrok on Lambda Labs:**
   ```bash
   ngrok config add-authtoken YOUR_TOKEN
   ```

4. **Run ngrok setup:**
   ```bash
   chmod +x setup_ngrok_lambda.sh
   ./setup_ngrok_lambda.sh
   ```

5. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

6. **Update frontend config:**
   ```javascript
   window.API_BASE_URL = "https://abc123.ngrok.io";
   ```

7. **Deploy to Vercel:**
   ```bash
   cd frontend && vercel --prod
   ```

**Cost:** Free (with limitations)

---

### **Option 3: Cloudflare Tunnel (Free Alternative)** 🌐

**Pros:**
- ✅ Free HTTPS
- ✅ Better than Ngrok for production
- ✅ DDoS protection
- ✅ Can use custom domain

**Cons:**
- ❌ Requires Cloudflare account
- ❌ More complex setup

**Steps:**

1. **Install cloudflared on Lambda Labs:**
   ```bash
   wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
   sudo dpkg -i cloudflared-linux-amd64.deb
   ```

2. **Login to Cloudflare:**
   ```bash
   cloudflared tunnel login
   ```

3. **Create tunnel:**
   ```bash
   cloudflared tunnel create lambda-chatbot
   ```

4. **Configure tunnel:**
   ```bash
   cat > ~/.cloudflared/config.yml << EOF
   tunnel: lambda-chatbot
   credentials-file: /home/ubuntu/.cloudflared/TUNNEL_ID.json
   
   ingress:
     - hostname: your-subdomain.your-domain.com
       service: http://localhost:8000
     - service: http_status:404
   EOF
   ```

5. **Run tunnel:**
   ```bash
   cloudflared tunnel run lambda-chatbot
   ```

6. **Update frontend config with Cloudflare URL**

**Cost:** Free

---

### **Option 4: Test Locally Without HTTPS** 🧪

**For testing only - NOT for production**

**Steps:**

1. **Test locally without Vercel:**
   ```bash
   cd frontend
   python -m http.server 8080
   ```

2. **Open:** `http://localhost:8080`

3. **This works because both are HTTP**

**Note:** This doesn't solve the Vercel deployment issue.

---

## 🎯 Recommended Solution

### **For Quick Testing (Today):**
Use **Option 2: Ngrok** - Get HTTPS in 5 minutes

### **For Production (Long-term):**
Use **Option 1: Custom Domain + SSL** - Professional and permanent

---

## 📋 Quick Start: Ngrok (5 Minutes)

```bash
# On Lambda Labs instance:

# 1. Install ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/

# 2. Sign up and get token from: https://dashboard.ngrok.com/signup

# 3. Configure ngrok
ngrok config add-authtoken YOUR_TOKEN

# 4. Start tunnel
ngrok http 8000

# 5. Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
```

```javascript
// On your local machine:
// Update frontend/config.js:
window.API_BASE_URL = "https://abc123.ngrok.io";
```

```bash
# Deploy to Vercel:
cd frontend
vercel --prod
```

**Done! Your frontend now connects via HTTPS** ✅

---

## 📋 Quick Start: Custom Domain (30 Minutes)

```bash
# 1. Buy domain (e.g., chatbot.yourdomain.com)

# 2. Point A record to: 167.234.215.206

# 3. Wait for DNS propagation (5-30 minutes)
dig +short chatbot.yourdomain.com

# 4. On Lambda Labs, run:
chmod +x setup_ssl_lambda.sh
./setup_ssl_lambda.sh chatbot.yourdomain.com
```

```javascript
// Update frontend/config.js:
window.API_BASE_URL = "https://chatbot.yourdomain.com";
```

```bash
# Deploy to Vercel:
cd frontend
vercel --prod
```

**Done! Professional HTTPS setup** ✅

---

## 🧪 Testing Your HTTPS Setup

### Test 1: Direct API Call
```bash
# Should work without errors
curl https://YOUR_URL/health
```

### Test 2: Browser Console
```javascript
// Open https://lambda-mgen-gpt.vercel.app/
// Console should show:
device: "cuda"  // ✅ No mixed content error
```

### Test 3: Chat Functionality
- Ask a question
- Should get response without errors
- Check console for any HTTPS errors

---

## 🐛 Troubleshooting

### Issue 1: "Mixed Content" still appears

**Solution:**
1. Clear browser cache: `Ctrl + Shift + Delete`
2. Hard refresh: `Ctrl + Shift + R`
3. Check `config.js` uses `https://` not `http://`
4. Redeploy to Vercel

### Issue 2: "SSL certificate error"

**Solution:**
1. Wait for DNS propagation (up to 48 hours, usually 5-30 min)
2. Verify domain points to correct IP: `dig +short your-domain.com`
3. Re-run SSL setup script

### Issue 3: Ngrok "tunnel not found"

**Solution:**
1. Make sure ngrok is running: `ps aux | grep ngrok`
2. Restart ngrok: `ngrok http 8000`
3. Update config.js with new URL

---

## 💰 Cost Comparison

| Option | Setup Time | Monthly Cost | Best For |
|--------|------------|--------------|----------|
| Custom Domain + SSL | 30 min | $1-2 | Production |
| Ngrok Free | 5 min | $0 | Testing |
| Ngrok Pro | 5 min | $8 | Development |
| Cloudflare Tunnel | 20 min | $0 | Production (free) |

---

## 🎉 Success Checklist

After setup, verify:
- [ ] No "Mixed Content" errors in console
- [ ] Console shows `device: "cuda"`
- [ ] API URL uses `https://` not `http://`
- [ ] Chatbot responds to questions
- [ ] No CORS errors
- [ ] Response times are fast (GPU acceleration working)

---

## 📚 Additional Resources

- **Let's Encrypt:** https://letsencrypt.org/
- **Ngrok:** https://ngrok.com/docs
- **Cloudflare Tunnels:** https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- **Vercel HTTPS:** https://vercel.com/docs/concepts/edge-network/encryption

---

**Choose your solution and get HTTPS working! 🚀**

