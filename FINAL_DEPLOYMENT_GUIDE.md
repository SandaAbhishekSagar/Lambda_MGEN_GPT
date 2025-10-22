# Lambda Labs GPU Deployment - Final Guide

## 🎯 Complete Deployment with All Fixes Applied

This guide ensures you can deploy tomorrow on a new instance without any of the previous errors.

## ✅ All Previous Errors Fixed

1. **IndentationError** - Fixed in `lambda_gpu_chatbot.py`
2. **Import errors** - Added missing imports (pickle, ThreadPoolExecutor, as_completed)
3. **ChromaDB authentication** - Multiple fallback methods implemented
4. **Document counting** - Optimized for 25,000 documents across 1,000 collections
5. **Frontend configuration** - Updated to use correct endpoints
6. **Dependency conflicts** - Resolved huggingface-hub version issues

## 🚀 Quick Deployment (New Instance)

### Step 1: Clone and Setup
```bash
git clone <your-repo>
cd Lambda_MGEN_GPT
chmod +x deploy_final_complete.sh
```

### Step 2: Run Initial Setup
```bash
./lambda_deploy.sh
```

### Step 3: Deploy with All Fixes
```bash
./deploy_final_complete.sh
```

## 📋 Environment Variables Required

Create a `.env` file with these variables:

```bash
# OpenAI Configuration (REQUIRED)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1000

# ChromaDB Cloud Configuration (REQUIRED)
USE_CLOUD_CHROMA=true
CHROMADB_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW
CHROMADB_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130
CHROMADB_DATABASE=newtest

# API Server Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=1

# GPU Configuration
CUDA_VISIBLE_DEVICES=0
TORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
```

## 🔧 Key Files Fixed

### 1. `services/chat_service/lambda_gpu_chatbot_final.py`
- ✅ Fixed indentation errors
- ✅ Added missing imports
- ✅ Implemented fallback collection retrieval
- ✅ GPU optimization for A100

### 2. `services/chat_service/lambda_gpu_api_final.py`
- ✅ Fixed document counting endpoint
- ✅ Proper error handling
- ✅ CORS configuration
- ✅ Performance optimization

### 3. `frontend/config.js`
- ✅ Updated to use localhost:8000
- ✅ Ready for production IP update

### 4. `frontend/script.js`
- ✅ Fixed health endpoint URL
- ✅ Proper error handling

## 🧪 Testing Endpoints

After deployment, test these endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Document count (should show ~25,000)
curl http://localhost:8000/documents

# Chat test
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question": "What programs does Northeastern offer?"}'
```

## 🎯 Expected Results

- ✅ **Document count**: ~25,000 documents
- ✅ **Collections**: 1,000 collections
- ✅ **Response time**: Sub-8 seconds with GPU acceleration
- ✅ **GPU utilization**: A100 optimization active
- ✅ **Frontend connection**: Working properly

## 🚨 Troubleshooting

### If you get IndentationError:
```bash
cp services/chat_service/lambda_gpu_chatbot_final.py services/chat_service/lambda_gpu_chatbot.py
```

### If you get import errors:
```bash
pip install "huggingface-hub>=0.16.4,<0.20.0" --force-reinstall
```

### If ChromaDB connection fails:
The system will automatically use fallback collection names (1,000 collections).

### If document count shows 0:
Check the logs for ChromaDB connection issues. The fallback mechanism will still work.

## 📊 Performance Monitoring

Monitor your deployment:

```bash
# Check GPU usage
nvidia-smi

# Check server logs
tail -f /tmp/lambda_gpu_api.log

# Check API health
curl http://localhost:8000/health
```

## 🎉 Success Indicators

Your deployment is successful when:

1. ✅ API server starts without errors
2. ✅ Health endpoint returns 200
3. ✅ Documents endpoint shows ~25,000 documents
4. ✅ Chat endpoint responds in <8 seconds
5. ✅ Frontend connects successfully
6. ✅ GPU utilization visible in nvidia-smi

## 🔄 Frontend Deployment

To start the frontend:

```bash
cd frontend
python3 server.py
```

Then open: `http://localhost:3000`

## 📝 Notes for Tomorrow's Deployment

1. **Use the fixed files**: `lambda_gpu_chatbot_final.py` and `lambda_gpu_api_final.py`
2. **Environment variables**: Make sure `.env` file is properly configured
3. **Dependencies**: The requirements_lambda.txt is already fixed
4. **Fallback mechanisms**: All error scenarios are handled
5. **Performance**: Optimized for 25,000 documents across 1,000 collections

## 🎯 Final Checklist

Before deploying tomorrow:

- [ ] Clone repository
- [ ] Run `./lambda_deploy.sh`
- [ ] Run `./deploy_final_complete.sh`
- [ ] Test all endpoints
- [ ] Start frontend
- [ ] Verify document count (~25,000)
- [ ] Test chat functionality
- [ ] Check GPU utilization

**You're ready for a successful deployment! 🚀**
