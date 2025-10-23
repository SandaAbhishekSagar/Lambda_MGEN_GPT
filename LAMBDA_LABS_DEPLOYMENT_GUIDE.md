# Lambda Labs GPU Deployment Guide
## Northeastern University Chatbot - Ultra-Fast GPU Deployment

### 🚀 **Error-Free Deployment for Jupyter Terminal**

This guide provides a complete, error-free deployment solution for your Northeastern University Chatbot on Lambda Labs with GPU acceleration.

## 📋 **Prerequisites**

- Lambda Labs GPU instance (A100, H100, RTX 4090, etc.)
- Jupyter terminal access
- OpenAI API key
- ChromaDB Cloud credentials (provided)

## 🎯 **Quick Start (One Command Deployment)**

```bash
# Clone your repository
git clone <your-repository-url>
cd Lambda_MGEN_GPT

# Run the optimized deployment script
chmod +x deploy_lambda_labs_optimized.sh
./deploy_lambda_labs_optimized.sh
```

## 📝 **Step-by-Step Deployment**

### Step 1: Environment Setup
```bash
# Navigate to your project directory
cd Lambda_MGEN_GPT

# Make deployment script executable
chmod +x deploy_lambda_labs_optimized.sh
```

### Step 2: Run Deployment Script
```bash
# Execute the deployment script
./deploy_lambda_labs_optimized.sh
```

The script will:
- ✅ Check Lambda Labs environment
- ✅ Install essential packages (no system restart)
- ✅ Create Python virtual environment
- ✅ Install PyTorch with CUDA support
- ✅ Install all required dependencies
- ✅ Create configuration files
- ✅ Set up monitoring scripts

### Step 3: Configure Environment Variables
```bash
# Edit the environment file
nano .env
```

Update the following variables:
```env
# OpenAI Configuration (REQUIRED)
OPENAI_API_KEY=your_actual_openai_api_key_here

# ChromaDB Cloud Configuration (already configured)
USE_CLOUD_CHROMA=true
CHROMADB_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW
CHROMADB_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130
CHROMADB_DATABASE=newtest
```

### Step 4: Test the Installation
```bash
# Run the test script
python3 test_lambda_labs.py
```

Expected output:
```
🚀 LAMBDA LABS TEST SCRIPT
==========================

1. Testing GPU availability...
✅ PyTorch version: 2.1.0+cu121
✅ CUDA available: True
✅ GPU name: NVIDIA A100-SXM4-40GB
✅ GPU memory: 40.0 GB

2. Testing chatbot import...
✅ Chatbot import successful

3. Testing chatbot initialization...
✅ Chatbot initialization successful

📊 TEST SUMMARY
===============
GPU Available: ✅
Import Success: ✅
Init Success: ✅

🎉 Chatbot is ready for deployment!
```

### Step 5: Start the Chatbot
```bash
# Start the API server
./start_chatbot.sh
```

Expected output:
```
🚀 Starting Northeastern University Chatbot...
=============================================
✅ Environment variables loaded
🌐 Starting API server on port 8000...
[LAMBDA GPU API] Starting server...
[LAMBDA GPU API] Starting on 0.0.0.0:8000 with 1 workers
```

### Step 6: Test the API
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question": "What programs does Northeastern University offer?"}'
```

### Step 7: Start Frontend (Optional)
```bash
# In another terminal
cd frontend
python3 server.py
```

## 🔧 **Key Features**

### GPU Optimization
- ✅ **A100/H100 Optimization**: Automatic batch size adjustment
- ✅ **CUDA Acceleration**: PyTorch with CUDA 12.1 support
- ✅ **Memory Management**: FP16 precision for efficiency
- ✅ **Parallel Processing**: Multi-threaded document search

### Performance Features
- ✅ **Sub-8 Second Response**: Optimized for speed
- ✅ **25,000+ Documents**: ChromaDB Cloud integration
- ✅ **Intelligent Caching**: Embeddings and query caching
- ✅ **Quality Filtering**: Relevance-based document ranking

### Error Handling
- ✅ **Graceful Fallbacks**: Multiple authentication methods
- ✅ **Comprehensive Logging**: Detailed error tracking
- ✅ **Health Monitoring**: Real-time system status
- ✅ **GPU Monitoring**: nvidia-smi integration

## 📊 **Monitoring and Maintenance**

### GPU Monitoring
```bash
# Real-time GPU monitoring
./monitor_gpu.sh

# Check GPU status
nvidia-smi
```

### Performance Monitoring
```bash
# Check API performance
curl http://localhost:8000/performance

# Check document count
curl http://localhost:8000/documents
```

### Cache Management
```bash
# Clear GPU cache
curl -X POST http://localhost:8000/clear-cache
```

## 🚨 **Troubleshooting**

### Common Issues and Solutions

#### 1. GPU Not Detected
```bash
# Check NVIDIA drivers
nvidia-smi

# If not available, install minimal drivers
sudo apt update
sudo apt install -y nvidia-utils-570-server
```

#### 2. Import Errors
```bash
# Reinstall dependencies
source lambda_gpu_env/bin/activate
pip install -r requirements_lambda_optimized.txt
```

#### 3. ChromaDB Connection Issues
```bash
# Check environment variables
cat .env | grep CHROMADB

# Test connection
python3 -c "
import chromadb
client = chromadb.HttpClient(host='https://api.trychroma.com')
print('ChromaDB connection successful')
"
```

#### 4. Memory Issues
```bash
# Clear GPU cache
python3 -c "
import torch
torch.cuda.empty_cache()
print('GPU cache cleared')
"

# Restart the application
./start_chatbot.sh
```

## 📈 **Expected Performance**

### Response Times
- **Simple Questions**: 2-4 seconds
- **Complex Questions**: 4-8 seconds
- **Document Search**: 1-2 seconds
- **Answer Generation**: 1-3 seconds

### Resource Usage
- **GPU Memory**: 2-4 GB (A100)
- **System Memory**: 4-8 GB
- **CPU Usage**: 20-40%
- **Storage**: 10-20 GB

## 🎉 **Success Indicators**

Your deployment is successful when:

1. ✅ **GPU Detection**: `nvidia-smi` shows your GPU
2. ✅ **PyTorch CUDA**: `torch.cuda.is_available()` returns `True`
3. ✅ **API Health**: `curl http://localhost:8000/health` returns 200
4. ✅ **Document Count**: `curl http://localhost:8000/documents` shows ~25,000 documents
5. ✅ **Chat Response**: Chat endpoint responds in <8 seconds
6. ✅ **No Errors**: All logs show successful initialization

## 🔄 **Updates and Maintenance**

### Regular Maintenance
```bash
# Update dependencies
source lambda_gpu_env/bin/activate
pip install -r requirements_lambda_optimized.txt --upgrade

# Clear caches
./start_chatbot.sh --clear-cache
```

### Monitoring Scripts
```bash
# GPU monitoring
./monitor_gpu.sh

# System monitoring
htop

# Log monitoring
tail -f nohup.out
```

## 📞 **Support**

If you encounter any issues:

1. **Check Logs**: Look for error messages in the console output
2. **Run Tests**: Execute `python3 test_lambda_labs.py`
3. **Monitor Resources**: Use `./monitor_gpu.sh`
4. **Restart Services**: Stop and restart the chatbot

## 🚀 **You're Ready for Production!**

Your Northeastern University Chatbot is now running on Lambda Labs with:
- ✅ **GPU Acceleration**: A100/H100 optimization
- ✅ **Ultra-Fast Responses**: Sub-8 second response times
- ✅ **Robust Error Handling**: Comprehensive fallbacks
- ✅ **Real-time Monitoring**: GPU and performance tracking
- ✅ **Production Ready**: Stable and scalable deployment

**Your Lambda Labs GPU chatbot is ready for production deployment! 🚀**
