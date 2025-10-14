# ⚡ Quick HTTPS Fix (5 Minutes with Ngrok)

## 🚨 Current Issue
```
Mixed Content Error: HTTPS page trying to load HTTP resource
```

## ✅ Fastest Solution: Ngrok (5 Minutes)

### On Lambda Labs Instance:

```bash
# 1. Install Ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/
rm ngrok-v3-stable-linux-amd64.tgz

# 2. Sign up at: https://dashboard.ngrok.com/signup
#    Get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken

# 3. Configure Ngrok (replace YOUR_TOKEN with your actual token)
ngrok config add-authtoken YOUR_TOKEN

# 4. Start Ngrok tunnel
ngrok http 8000
```

### You'll see output like:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

### Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

---

### On Your Local Machine:

```bash
# Update frontend/config.js
cd frontend
```

Edit `config.js`:
```javascript
// Replace with your ngrok URL
window.API_BASE_URL = "https://abc123.ngrok.io";
```

```bash
# Deploy to Vercel
vercel --prod
```

---

## 🧪 Test

1. Open your Vercel URL: `https://lambda-mgen-gpt.vercel.app/`
2. Open console (F12)
3. Should see: `device: "cuda"` ✅
4. No more "Mixed Content" errors! ✅

---

## ⚠️ Important Notes

**Ngrok Free Tier Limitations:**
- URL changes every time you restart ngrok
- 40 requests/minute limit
- Tunnel closes when you close terminal

**To keep tunnel running:**
```bash
# Use screen or tmux
screen -S ngrok
ngrok http 8000
# Press Ctrl+A then D to detach
```

**To reconnect:**
```bash
screen -r ngrok
```

---

## 🎯 For Production

After testing with Ngrok, set up a permanent solution:

1. **Buy a domain** ($10-15/year)
2. **Point to Lambda IP:** `167.234.215.206`
3. **Run SSL setup:**
   ```bash
   ./setup_ssl_lambda.sh your-domain.com
   ```

See `HTTPS_SOLUTIONS.md` for detailed instructions.

---

## 📞 Quick Commands

```bash
# Start ngrok
ngrok http 8000

# Check if ngrok is running
ps aux | grep ngrok

# Stop ngrok
pkill ngrok

# View ngrok dashboard
# Open: http://localhost:4040
```

---

**Get HTTPS working in 5 minutes! 🚀**

