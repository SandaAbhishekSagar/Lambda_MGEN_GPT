# 🔍 Verify Lambda Labs Connection

## ✅ What Was Fixed

**Problem:** Frontend was connecting to Railway (CPU) instead of Lambda Labs (GPU)

**Solution:** Updated `frontend/config.js` to point to Lambda Labs IP: `167.234.215.206:8000`

---

## 🧪 Test the Connection

### Quick Test (In Browser)

1. **Clear browser cache:**
   - Press `Ctrl + Shift + Delete` (Windows/Linux)
   - Press `Cmd + Shift + Delete` (Mac)
   - Clear cached files and reload

2. **Open your frontend** (refresh the page)

3. **Open browser console** (F12)

4. **Look for these indicators:**

   **✅ Connected to Lambda Labs GPU:**
   ```javascript
   device: "cuda"                    // Should be "cuda", not "cpu"
   gpu_embeddings: 'enabled'         // Should be 'enabled'
   message: "Lambda GPU..."          // Should mention Lambda GPU
   ```

   **❌ Still on Railway (CPU):**
   ```javascript
   device: "cpu"                     // Wrong - still on Railway
   gpu_embeddings: 'disabled'        // Wrong - GPU not being used
   message: "Enhanced OpenAI..."     // Wrong - Railway message
   ```

---

## 🔧 Manual Verification

### Test 1: Check Config File

```bash
# On your local machine
cat frontend/config.js
```

**Should show:**
```javascript
window.API_BASE_URL = "http://167.234.215.206:8000";
```

**NOT:**
```javascript
window.API_BASE_URL = "https://northeasternuniversitychatbot-production.up.railway.app";
```

### Test 2: Test Lambda API Directly

```bash
# Test health endpoint
curl http://167.234.215.206:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "device": "cuda",                    // ✅ GPU!
  "gpu_available": true,               // ✅ GPU detected
  "gpu_memory": "22.1 GB",            // ✅ NVIDIA A10
  "model": "gpt-4o-mini",
  "message": "Lambda GPU Northeastern University Chatbot API is running"
}
```

### Test 3: Check GPU Info

```bash
curl http://167.234.215.206:8000/gpu-info
```

**Expected response:**
```json
{
  "gpu_available": true,
  "gpu_name": "NVIDIA A10",           // ✅ GPU name
  "gpu_memory_total": "22.1 GB",      // ✅ GPU memory
  "cuda_version": "12.1"              // ✅ CUDA version
}
```

---

## 🚀 Deploy Updated Frontend to Vercel

Now that `config.js` is updated, deploy to Vercel:

```bash
cd frontend
vercel --prod
```

After deployment:
1. Open your Vercel URL
2. Clear browser cache
3. Test the chatbot
4. Check console logs for `device: "cuda"`

---

## 📊 Performance Comparison

### Railway (CPU) - OLD:
- Device: `cpu`
- Embedding time: ~2-5 seconds
- Total response: ~5-10 seconds
- GPU: ❌ Not available

### Lambda Labs (GPU) - NEW:
- Device: `cuda`
- Embedding time: ~0.2-0.5 seconds (10x faster!)
- Total response: ~2-5 seconds
- GPU: ✅ NVIDIA A10

---

## 🎯 Success Indicators

You'll know it's working when you see in the console:

```javascript
// Health check response
{
  device: "cuda",                     // ✅ Using GPU
  gpu_available: true,                // ✅ GPU detected
  gpu_memory: "22.1 GB",             // ✅ A10 memory
  features: {
    gpu_embeddings: 'enabled',        // ✅ GPU embeddings
    llm_provider: 'OpenAI',
    query_expansion: 'enabled',
    hybrid_search: 'enabled'
  }
}
```

---

## 🐛 Troubleshooting

### Issue 1: Still showing "cpu"

**Solution:**
1. Hard refresh browser: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
2. Clear browser cache completely
3. Open in incognito/private window
4. Check `config.js` file again

### Issue 2: "Connection refused" or timeout

**Possible causes:**
1. Lambda Labs API not running
2. Firewall blocking port 8000
3. Wrong IP address

**Solution:**
```bash
# On Lambda Labs instance, check if API is running
ps aux | grep lambda_gpu_api

# If not running, start it
cd ~/Lambda_MGEN_GPT
source lambda_gpu_env/bin/activate
./start_lambda_gpu.sh

# Check firewall
sudo ufw status
sudo ufw allow 8000/tcp
```

### Issue 3: CORS error

**Solution:** Already configured in Lambda API, but verify:
```python
# In lambda_gpu_api.py
allow_origins=["*"]  # Should allow all origins
```

---

## 📝 Checklist

Before testing:
- [ ] `frontend/config.js` updated with Lambda IP
- [ ] Lambda Labs API is running
- [ ] Port 8000 is accessible
- [ ] Browser cache cleared

After testing:
- [ ] Console shows `device: "cuda"`
- [ ] Console shows `gpu_embeddings: 'enabled'`
- [ ] Health check returns GPU info
- [ ] Chatbot responds faster than before
- [ ] No CORS errors in console

---

## 🎉 Next Steps

Once verified:
1. Deploy to Vercel with updated config
2. Test from Vercel URL
3. Monitor GPU usage on Lambda Labs
4. Enjoy 10x faster embeddings! 🚀

---

## 📞 Quick Commands

```bash
# Test Lambda API health
curl http://167.234.215.206:8000/health

# Test GPU info
curl http://167.234.215.206:8000/gpu-info

# Check if API is running (on Lambda Labs)
ps aux | grep lambda_gpu_api

# Start API (on Lambda Labs)
cd ~/Lambda_MGEN_GPT && source lambda_gpu_env/bin/activate && ./start_lambda_gpu.sh

# Deploy to Vercel
cd frontend && vercel --prod
```

---

**Your frontend is now configured to use Lambda Labs GPU backend! 🎊**

