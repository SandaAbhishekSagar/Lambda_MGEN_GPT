# Railway Port Environment Variable Fix

## 🚨 **Problem**

Railway's `railway.json` `startCommand` doesn't expand environment variables like `$PORT` or `${PORT:-8000}`.

**Error:**
```
Error: Invalid value for '--port': '$PORT' is not a valid integer.
```

---

## ✅ **Solution: Shell Wrapper Script**

Created `start.sh` to properly handle the `PORT` environment variable:

```bash
#!/bin/bash
PORT=${PORT:-8000}
echo "🚀 Starting Enhanced OpenAI API on port $PORT..."
uvicorn services.chat_service.enhanced_openai_api:app --host 0.0.0.0 --port $PORT
```

---

## 📋 **Changes Made**

### **1. Created `start.sh`**
- Handles PORT environment variable expansion
- Provides default value (8000) if PORT not set
- Starts the correct API (OpenAI, not GPU)

### **2. Updated `railway.json`**
```json
{
  "deploy": {
    "startCommand": "bash start.sh",  // ← Uses shell script
    ...
  }
}
```

### **3. Updated `.dockerignore`**
- Removed `*.sh` exclusion
- Ensures `start.sh` is included in Docker build

### **4. Updated `Dockerfile`**
```dockerfile
# Make startup script executable
RUN chmod +x start.sh
```

---

## 🚀 **Deploy Commands**

```bash
git add start.sh railway.json .dockerignore Dockerfile
git commit -m "Fix Railway port issue with shell wrapper script"
git push origin main
```

---

## 🎯 **Expected Result**

After deployment, you should see:

```
🚀 Starting Enhanced OpenAI API on port 8080...
[ENHANCED OPENAI API] Initializing enhanced OpenAI chatbot...
INFO: Uvicorn running on http://0.0.0.0:8080
✅ Enhanced OpenAI API initialized successfully!
```

---

## 📊 **Why This Works**

1. **Railway sets `PORT` environment variable** (e.g., `8080`)
2. **`bash start.sh` executes the shell script**
3. **Shell expands `${PORT:-8000}`** to the actual port number
4. **uvicorn receives a valid integer** (not a string like `$PORT`)

---

## 🔄 **Alternative Solutions (Not Used)**

### **Option A: Remove railway.json**
Let Dockerfile handle everything (but Dockerfile CMD also had issues)

### **Option B: Use Procfile**
Railway prioritizes `railway.json` over `Procfile`

### **Option C: Python wrapper script**
More complex than needed; shell script is simpler

---

## ✅ **This Fix Also Ensures:**

1. ✅ **Correct API starts** (OpenAI, not GPU/Ollama)
2. ✅ **Port is dynamic** (Railway can assign any port)
3. ✅ **Fallback to 8000** (for local testing)
4. ✅ **Clean startup logs** (shows which port is used)

---

## 🎉 **Ready to Deploy!**

Push these changes and Railway will:
1. Build using Dockerfile
2. Execute `bash start.sh`
3. Start Enhanced OpenAI API on Railway's assigned port
4. Health check at `/health/enhanced`

**Your app will finally run! 🚀**

