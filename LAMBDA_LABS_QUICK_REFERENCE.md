# Lambda Labs GPU Deployment - Quick Reference

## 🚀 **One-Command Deployment**

```bash
# Complete deployment with all fixes
chmod +x lambda_deploy_revamped.sh deploy_final_fixed.sh
./lambda_deploy_revamped.sh && ./deploy_final_fixed.sh
```

## 📋 **Essential Commands**

### **Deployment:**
```bash
# Step 1: Initial setup (no system restart)
./lambda_deploy_revamped.sh

# Step 2: Apply all fixes
./deploy_final_fixed.sh

# Step 3: Test everything
./test_frontend_connection.sh
```

### **Starting Services:**
```bash
# Start backend API
./start_chatbot.sh

# Start frontend (in another terminal)
cd frontend
python3 server.py
```

### **Testing:**
```bash
# Test API health
curl http://localhost:8000/health

# Test chat
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question": "What programs does Northeastern offer?"}'

# Test documents
curl http://localhost:8000/documents
```

### **Monitoring:**
```bash
# Monitor GPU usage
./monitor_gpu.sh

# Check GPU status
nvidia-smi

# Check server logs
tail -f /tmp/lambda_gpu_api.log
```

## 🔧 **Quick Fixes**

### **HuggingFace Hub Error:**
```bash
./quick_fix_deployment.sh
```

### **Frontend Connection Error:**
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not running
./start_chatbot.sh
```

### **Service Restart Prompts:**
- **Kernel upgrade**: Click "OK" (don't restart)
- **Service restart**: Uncheck services that might interfere with Jupyter
- **Keep `lambda-jupyter.service` checked**

## 📊 **Expected Results**

- ✅ **Document count**: ~25,000 documents
- ✅ **Response time**: <8 seconds
- ✅ **Frontend URL**: http://localhost:3000
- ✅ **API URL**: http://localhost:8000
- ✅ **GPU utilization**: Visible in nvidia-smi

## 🎯 **Success Checklist**

- [ ] API server running on port 8000
- [ ] Frontend running on port 3000
- [ ] Health endpoint returns 200
- [ ] Documents endpoint shows ~25,000
- [ ] Chat responds in <8 seconds
- [ ] No errors in logs
- [ ] GPU utilization visible

## 🚨 **Emergency Commands**

```bash
# Stop all services
pkill -f "lambda_gpu_api"
pkill -f "python3.*server.py"

# Restart backend
./start_chatbot.sh

# Restart frontend
cd frontend && python3 server.py

# Check what's running
ps aux | grep -E "(lambda_gpu_api|server.py)"
```

## 🎉 **You're Ready!**

All errors have been fixed. Your Lambda Labs GPU chatbot is production-ready! 🚀
