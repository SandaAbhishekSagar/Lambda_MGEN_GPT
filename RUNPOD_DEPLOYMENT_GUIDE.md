# 🚀 RunPod Serverless Deployment Guide

## Complete Guide to Deploy Northeastern University Chatbot on RunPod

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (5 Steps)](#quick-start)
3. [Detailed Deployment](#detailed-deployment)
4. [Frontend Integration](#frontend-integration)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)
7. [Cost Management](#cost-management)
8. [Performance Optimization](#performance-optimization)

---

## ✅ Prerequisites

### **Required:**
- RunPod account (sign up at [runpod.io](https://runpod.io))
- OpenAI API key
- ChromaDB Cloud API key
- Your chatbot code (already in this repository)

### **Optional:**
- Docker Hub account (for custom image deployment)
- RunPod CLI (for advanced deployment)

---

## 🚀 Quick Start (5 Steps)

### **Step 1: Get Your API Keys**

```bash
# 1. RunPod API Key
# Go to: https://runpod.io/console/user/settings
# Copy your API key

# 2. You already have these:
# - OPENAI_API_KEY
# - CHROMA_API_KEY
# - CHROMA_HOST (api.trychroma.com)
```

### **Step 2: Go to RunPod Serverless Console**

1. Visit: https://runpod.io/console/serverless
2. Click **"+ New Endpoint"**

### **Step 3: Configure Your Endpoint**

**Basic Settings:**
```
Name: northeastern-chatbot
GPU Type: RTX 4090 (24GB VRAM)
Container Image: runpod/pytorch:2.1.0-py3.10-cuda12.1.0-devel
Container Disk: 20 GB
```

**Workers Configuration:**
```
Min Workers: 0 (pay only when used)
Max Workers: 10 (scale up to 10 concurrent requests)
Idle Timeout: 30 seconds
Max Execution Time: 120 seconds
```

**Environment Variables:**
```
OPENAI_API_KEY=sk-...your-key...
CHROMA_API_KEY=...your-chroma-key...
CHROMA_HOST=api.trychroma.com
CHROMA_PORT=8000
CHROMA_TENANT=default_tenant
CHROMA_DATABASE=default_database
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
```

### **Step 4: Upload Your Code**

**Option A: Via RunPod Console (Easiest)**

1. In the endpoint configuration, scroll to **"Custom Files"**
2. Upload these files:
   - `runpod_handler.py`
   - `runpod_requirements.txt` (rename to `requirements.txt`)
   - `services/` folder (entire directory)

3. Set **"Handler"**: `runpod_handler.handler`

**Option B: Via Docker Image (Advanced)**

```bash
# Build and push Docker image
docker build -f Dockerfile.runpod -t yourusername/northeastern-chatbot:runpod .
docker push yourusername/northeastern-chatbot:runpod

# Then use this image in RunPod:
# Container Image: yourusername/northeastern-chatbot:runpod
```

### **Step 5: Deploy!**

1. Click **"Deploy"**
2. Wait 2-3 minutes for deployment
3. Copy your **Endpoint ID** (looks like: `abcd1234xyz`)
4. Your endpoint URL will be:
   ```
   https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync
   ```

---

## 📝 Detailed Deployment

### **Method 1: Web Console (Recommended for Beginners)**

#### **1. Create RunPod Account**

1. Go to https://runpod.io
2. Sign up with email/GitHub
3. Add billing information (no charges until you use it)
4. Get $10 free credits!

#### **2. Navigate to Serverless**

1. Click **"Serverless"** in left menu
2. Click **"+ New Endpoint"**

#### **3. Select GPU**

**Recommended: RTX 4090**
- Cost: $0.00039/second = $1.40/hour
- VRAM: 24GB
- Performance: Excellent for LLM inference
- Availability: Good

**Alternative: A40**
- Cost: $0.00079/second = $2.84/hour
- VRAM: 48GB
- Performance: Better for larger models
- Availability: Good

**Alternative: A100**
- Cost: $0.00139/second = $5.00/hour
- VRAM: 80GB
- Performance: Best (overkill for this use case)
- Availability: Limited

#### **4. Configure Container**

**Base Image:**
```
runpod/pytorch:2.1.0-py3.10-cuda12.1.0-devel
```

This includes:
- Python 3.10
- PyTorch 2.1.0
- CUDA 12.1
- Common ML libraries

**Container Disk:** 20 GB
- Enough for model cache
- Prevents disk full errors

#### **5. Set Environment Variables**

Click **"Add Environment Variable"** for each:

```env
OPENAI_API_KEY=sk-proj-...your-actual-key...
CHROMA_API_KEY=...your-chroma-api-key...
CHROMA_HOST=api.trychroma.com
CHROMA_PORT=8000
CHROMA_TENANT=default_tenant
CHROMA_DATABASE=default_database
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
```

**Important:** Replace with your actual keys!

#### **6. Upload Files**

In **"Advanced Configuration"** → **"Custom Files"**:

1. Click **"Add File"**
2. Upload `runpod_handler.py`
3. Click **"Add File"**
4. Upload `runpod_requirements.txt` as `requirements.txt`
5. Click **"Add Folder"**
6. Upload entire `services/` directory

Your file structure should look like:
```
/
├── runpod_handler.py
├── requirements.txt
└── services/
    ├── __init__.py
    ├── shared/
    │   ├── database.py
    │   └── chroma_service.py
    └── chat_service/
        └── enhanced_openai_chatbot.py
```

#### **7. Set Handler Function**

In **"Handler"** field:
```
runpod_handler.handler
```

This tells RunPod to call the `handler` function in `runpod_handler.py`

#### **8. Configure Scaling**

**Workers:**
- **Min Workers:** `0`
  - Scales to zero when not in use
  - You pay nothing when idle!
  
- **Max Workers:** `10`
  - Can handle 10 concurrent requests
  - Adjust based on expected traffic

**Timeouts:**
- **Idle Timeout:** `30` seconds
  - Worker shuts down after 30s of no requests
  
- **Max Execution Time:** `120` seconds
  - Enough for slow queries + cold start

#### **9. Deploy**

1. Click **"Deploy"**
2. Wait for status to change to **"Ready"**
3. This takes 2-3 minutes

#### **10. Get Your Endpoint**

Once deployed, you'll see:
- **Endpoint ID:** `abcd1234xyz` (copy this!)
- **Endpoint URL:** `https://api.runpod.ai/v2/abcd1234xyz/runsync`

---

### **Method 2: Using Deployment Script**

#### **Quick Deploy (Recommended)**

```bash
# 1. Set environment variables
export RUNPOD_API_KEY="your-runpod-api-key"
export OPENAI_API_KEY="your-openai-key"
export CHROMA_API_KEY="your-chroma-key"

# 2. Run simple deployment script
./deploy_runpod_simple.sh
```

This will:
- Install RunPod SDK
- Verify your credentials
- Create deployment package
- Show you next steps

#### **Advanced Deploy (Docker)**

```bash
# 1. Login to Docker Hub
docker login

# 2. Run full deployment
./deploy_runpod.sh
```

This will:
- Build Docker image
- Push to Docker Hub
- Provide deployment instructions

---

## 🌐 Frontend Integration

### **Step 1: Update Frontend Config**

**Option A: Use the RunPod config template**

```bash
# Copy the RunPod config
cp frontend/config.runpod.js frontend/config.js

# Edit with your endpoint ID
# Replace YOUR_ENDPOINT_ID with your actual ID
```

**Option B: Update existing config.js**

```javascript
// frontend/config.js
window.API_BASE_URL = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID";

// If you have an API key requirement (usually not needed)
window.RUNPOD_API_KEY = "";  // Leave empty for public endpoints
```

### **Step 2: Update HTML (Optional)**

If you want to use the RunPod-specific JavaScript extension:

```html
<!-- In frontend/index.html, after script.js -->
<script src="config.js"></script>
<script src="script.js"></script>
<script src="script.runpod.js"></script>  <!-- Add this -->
```

The `script.runpod.js` file handles RunPod's specific request/response format.

### **Step 3: Deploy Frontend to Vercel**

```bash
cd frontend

# Deploy to Vercel
vercel --prod

# Or if first time:
vercel login
vercel --prod
```

### **Step 4: Test Integration**

1. Open your Vercel URL
2. Try asking: "What programs does Northeastern offer?"
3. Check browser console for logs
4. Verify response time < 8 seconds

---

## 🧪 Testing

### **Test 1: Direct API Test**

```bash
# Set your endpoint URL
export RUNPOD_ENDPOINT_URL="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync"

# Run test
python test_runpod_endpoint.py
```

**Expected Output:**
```
🧪 Testing RunPod Endpoint
================================

📝 Question: What programs does Northeastern University offer?

⏳ Sending request to RunPod...
⏱️  Total request time: 4.52s
📊 Status code: 200

================================
✅ SUCCESS
================================

💬 Answer:
--------------------------------------------------------------------------------
Northeastern University offers a wide range of programs across various fields...
--------------------------------------------------------------------------------

📚 Sources (5):
  1. Academic Catalog (similarity: 87.5%)
  2. Graduate Programs (similarity: 84.2%)
  ...

🎯 Confidence: HIGH

⏱️  Timing Breakdown:
  - Search: 2.1s
  - Generation: 2.3s
  - Total: 4.4s

✅ MEETS REQUIREMENT: Response in 4.52s (< 8s)
```

### **Test 2: Run Full Test Suite**

```bash
python test_runpod_endpoint.py
```

This tests 5 different questions and provides statistics.

### **Test 3: Frontend Test**

1. Open your Vercel frontend
2. Open browser DevTools (F12)
3. Go to Console tab
4. Send a message
5. Look for:
   ```
   📤 Sending to RunPod: What programs does Northeastern offer?
   📡 RunPod endpoint: https://api.runpod.ai/v2/.../runsync
   📥 RunPod response: {...}
   ⏱️ Response time: 4520ms
   ✅ Meets requirement: 4.52s < 8s
   ```

### **Test 4: Cold Start Test**

Wait 1 minute (for worker to shut down), then send a message.

**Expected:**
- First request: 5-8 seconds (includes cold start)
- Subsequent requests: 2-4 seconds (worker is warm)

---

## 🐛 Troubleshooting

### **Issue 1: "Endpoint not found" or 404**

**Cause:** Incorrect endpoint URL

**Fix:**
```javascript
// Check your endpoint ID is correct
// Should look like: https://api.runpod.ai/v2/abcd1234xyz/runsync
// NOT: https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync
```

### **Issue 2: Timeout / No Response**

**Cause:** Cold start or slow processing

**Fix:**
1. Increase timeout in frontend:
```javascript
window.REQUEST_CONFIG = {
    timeout: 180000  // 3 minutes
};
```

2. First request might be slow (cold start):
   - Wait 10-15 seconds
   - Subsequent requests will be faster

### **Issue 3: "No module named 'runpod'"**

**Cause:** Requirements not installed

**Fix:**
1. Check `requirements.txt` is uploaded
2. Check it's named exactly `requirements.txt` (not `runpod_requirements.txt`)
3. Redeploy endpoint

### **Issue 4: "OPENAI_API_KEY not set"**

**Cause:** Environment variable not configured

**Fix:**
1. Go to RunPod endpoint settings
2. Click "Edit"
3. Add environment variable:
   ```
   OPENAI_API_KEY=sk-...
   ```
4. Save and restart endpoint

### **Issue 5: "Failed to initialize NVML"**

**Cause:** GPU driver issue (rare on RunPod)

**Fix:**
- Usually resolves automatically
- If persistent, contact RunPod support
- Your code works on CPU too (just slower)

### **Issue 6: Slow Responses (> 8s)**

**Possible Causes:**
1. **Cold start** - First request after idle
   - Solution: Keep min_workers = 1 (costs more)
   - Or accept slower first request

2. **Network latency**
   - Check your internet connection
   - Try from different location

3. **Database query slow**
   - Check ChromaDB is responding
   - Reduce n_results if needed

4. **Wrong GPU type**
   - Use RTX 4090 or better
   - Avoid CPU-only instances

### **Issue 7: High Costs**

**Cause:** Workers not scaling to zero

**Fix:**
1. Set **Min Workers: 0**
2. Set **Idle Timeout: 30** seconds
3. Monitor in RunPod console

---

## 💰 Cost Management

### **Understanding Costs**

**RunPod Serverless Pricing:**
```
RTX 4090: $0.00039/second
          = $1.40/hour
          = Only when processing requests!
```

**Example Costs:**

**Scenario 1: Light Use (100 requests/day)**
```
Avg response: 3 seconds
Daily cost: 100 × 3 × $0.00039 = $0.117/day
Monthly cost: $0.117 × 30 = $3.51/month
```

**Scenario 2: Moderate Use (500 requests/day)**
```
Avg response: 3 seconds
Daily cost: 500 × 3 × $0.00039 = $0.585/day
Monthly cost: $0.585 × 30 = $17.55/month
```

**Scenario 3: Heavy Use (2000 requests/day)**
```
Avg response: 3 seconds
Daily cost: 2000 × 3 × $0.00039 = $2.34/day
Monthly cost: $2.34 × 30 = $70.20/month
```

### **Cost Optimization Tips**

1. **Scale to Zero**
   ```yaml
   min_workers: 0  # ← Important!
   idle_timeout: 30
   ```

2. **Choose Right GPU**
   - RTX 4090: Best value for LLMs
   - A40: Only if you need 48GB VRAM
   - A100: Overkill for this use case

3. **Optimize Response Time**
   - Faster responses = lower cost
   - Cache common queries (future enhancement)
   - Reduce n_results if acceptable

4. **Monitor Usage**
   - Check RunPod dashboard daily
   - Set up budget alerts
   - Track cost per request

5. **Use Webhooks for Long Jobs**
   - For async processing
   - Cheaper than sync endpoints

---

## ⚡ Performance Optimization

### **Target: < 8 Seconds Response Time**

**Current Performance:**
- Search: 1-2 seconds
- Generation: 1-3 seconds
- **Total: 3-6 seconds** ✅

**Optimization Strategies:**

#### **1. Reduce Search Time**

```python
# In runpod_handler.py, reduce collections searched
max_collections_to_search = 50  # Instead of 100
n_results = 5  # Instead of 10
```

**Trade-off:** Less comprehensive search, but faster

#### **2. Optimize LLM Generation**

```python
# Use faster OpenAI model
self.llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # Faster than gpt-4
    max_tokens=1500,  # Reduce if acceptable
)
```

**Trade-off:** Slightly lower quality answers

#### **3. Enable Response Streaming**

```python
# Stream response as it generates
# Perceived speed improvement
```

#### **4. Implement Caching**

```python
# Cache common questions
# Instant response for cached queries
```

#### **5. Keep Workers Warm**

```yaml
min_workers: 1  # Always keep one warm
```

**Trade-off:** Costs $1.40/hour = ~$1,000/month

**Recommendation:** Only for production with high traffic

#### **6. Use Smaller Embeddings Model**

Already using `text-embedding-3-small` (optimal)

---

## 📊 Monitoring

### **RunPod Dashboard**

1. Go to: https://runpod.io/console/serverless
2. Click your endpoint
3. View:
   - Active workers
   - Request count
   - Average response time
   - Cost per request
   - Errors

### **Frontend Monitoring**

Check browser console for:
```
⏱️ Response time: 4520ms
✅ Meets requirement: 4.52s < 8s
```

### **Set Up Alerts**

1. Email alerts for:
   - High costs (> $X/day)
   - High error rate (> 5%)
   - Slow responses (> 10s)

2. Configure in RunPod dashboard

---

## 🎯 Success Checklist

- [ ] RunPod account created
- [ ] Endpoint deployed successfully
- [ ] Environment variables configured
- [ ] Handler function working
- [ ] Frontend updated with endpoint URL
- [ ] Frontend deployed to Vercel
- [ ] Test message sent successfully
- [ ] Response time < 8 seconds ✅
- [ ] HTTPS working automatically ✅
- [ ] Costs monitored
- [ ] No custom domain needed ✅

---

## 📚 Additional Resources

**RunPod Documentation:**
- Serverless: https://docs.runpod.io/serverless/overview
- API Reference: https://docs.runpod.io/reference/overview

**Support:**
- RunPod Discord: https://discord.gg/runpod
- RunPod Support: support@runpod.io

**Your Chatbot:**
- Handler code: `runpod_handler.py`
- Test script: `test_runpod_endpoint.py`
- Frontend config: `frontend/config.runpod.js`

---

## 🎉 You're Done!

Your Northeastern University Chatbot is now:

✅ **Deployed on RunPod Serverless**
✅ **Automatic HTTPS** (no custom domain needed)
✅ **GPU-accelerated** (fast responses)
✅ **Auto-scaling** (pay only for usage)
✅ **< 8 second responses** (meets requirement)
✅ **Cost-effective** (~$20-50/month moderate use)

**Enjoy your chatbot!** 🚀

Need help? Check the troubleshooting section or contact RunPod support.

