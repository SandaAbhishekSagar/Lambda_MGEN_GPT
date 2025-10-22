# 🔧 Lambda Labs GPU Environment Variables - Simplified
## Northeastern University Chatbot - ChromaDB Cloud Configuration

This document contains the **essential environment variables** needed for Lambda Labs GPU deployment with your existing ChromaDB Cloud `newtest` database.

---

## 📋 **Essential Environment Variables (Minimal Setup)**

### **1. Core API Keys (REQUIRED)**
```bash
# OpenAI API Key (REQUIRED)
OPENAI_API_KEY=your_openai_api_key_here

# OpenAI Model Configuration
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3
OPENAI_MAX_TOKENS=3000
OPENAI_TIMEOUT=20
```

### **2. ChromaDB Cloud Configuration (REQUIRED)**
```bash
# ChromaDB Cloud Settings (newtest database)
USE_CLOUD_CHROMA=true
CHROMADB_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW
CHROMADB_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130
CHROMADB_DATABASE=newtest
```

### **3. GPU Configuration (REQUIRED FOR LAMBDA LABS)**
```bash
# CUDA Configuration
CUDA_VISIBLE_DEVICES=0
TORCH_CUDA_ARCH_LIST="7.5;8.0;8.6"

# GPU Performance Settings
GPU_BATCH_SIZE=32
GPU_MEMORY_FRACTION=0.8
GPU_MIXED_PRECISION=true

# Lambda Labs Specific
LAMBDA_LABS_GPU=true
GPU_TYPE=rtx4090
```

### **4. API Server Configuration**
```bash
# Server Settings
HOST=0.0.0.0
PORT=8000
WORKERS=1

# API Configuration
API_TIMEOUT=30
CORS_ORIGINS="*"
```

### **5. Performance Optimization**
```bash
# CPU Settings
OMP_NUM_THREADS=4
TOKENIZERS_PARALLELISM=false

# Memory Settings
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
TRANSFORMERS_CACHE=/runpod-volume/transformers-cache
HF_HOME=/runpod-volume/huggingface

# Cache Settings
CACHE_TTL=3600
MAX_MEMORY_CACHE_SIZE=2147483648
MAX_DISK_CACHE_SIZE=10737418240
```

### **6. Database Optimization**
```bash
# Search Settings
MAX_COLLECTIONS_PER_SEARCH=150
SEARCH_TIMEOUT=5
PARALLEL_WORKERS=8
BATCH_SIZE=32
```

---

## 🚀 **Quick Setup Commands**

### **1. Create Minimal .env File**
```bash
# Create your .env file with these essential variables
cat > .env << 'EOF'
# Core API Keys
OPENAI_API_KEY=your_openai_api_key_here

# ChromaDB Cloud (newtest database)
USE_CLOUD_CHROMA=true
CHROMADB_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW
CHROMADB_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130
CHROMADB_DATABASE=newtest

# GPU Configuration
CUDA_VISIBLE_DEVICES=0
TORCH_CUDA_ARCH_LIST="7.5;8.0;8.6"
GPU_BATCH_SIZE=32
GPU_MEMORY_FRACTION=0.8
GPU_MIXED_PRECISION=true
LAMBDA_LABS_GPU=true
GPU_TYPE=rtx4090

# API Server
HOST=0.0.0.0
PORT=8000
WORKERS=1
API_TIMEOUT=30
CORS_ORIGINS="*"

# Performance Optimization
OMP_NUM_THREADS=4
TOKENIZERS_PARALLELISM=false
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
TRANSFORMERS_CACHE=/runpod-volume/transformers-cache
HF_HOME=/runpod-volume/huggingface
CACHE_TTL=3600
MAX_MEMORY_CACHE_SIZE=2147483648
MAX_DISK_CACHE_SIZE=10737418240

# Database Optimization
MAX_COLLECTIONS_PER_SEARCH=150
SEARCH_TIMEOUT=5
PARALLEL_WORKERS=8
BATCH_SIZE=32
EOF
```

### **2. Set Your OpenAI API Key**
```bash
# Edit the .env file and replace with your actual OpenAI API key
nano .env
# Replace: OPENAI_API_KEY=your_openai_api_key_here
# With: OPENAI_API_KEY=sk-your-actual-openai-key
```

### **3. Test Configuration**
```bash
# Test the configuration
python3 lambda_quick_start.py
```

---

## 📊 **Environment Variable Categories (Simplified)**

| Category | Variables | Purpose |
|----------|-----------|---------|
| **Core API** | 5 variables | OpenAI configuration |
| **ChromaDB Cloud** | 4 variables | newtest database connection |
| **GPU Config** | 7 variables | GPU acceleration settings |
| **API Server** | 5 variables | Server configuration |
| **Performance** | 8 variables | Optimization settings |
| **Database** | 4 variables | Search optimization |

**Total: 33 essential variables** for minimal Lambda Labs GPU deployment.

---

## ✅ **Validation Checklist**

- [ ] OpenAI API key set and valid
- [ ] ChromaDB Cloud connection configured (newtest database)
- [ ] GPU settings optimized for your instance
- [ ] Performance settings tuned
- [ ] API server configuration complete

---

## 🔍 **Key Differences from Standard Setup**

### **ChromaDB Cloud vs Local:**
- ✅ **No HOST/PORT needed** - Uses ChromaDB Cloud
- ✅ **Pre-configured credentials** - Your existing newtest database
- ✅ **1,000 collections ready** - Already populated with data
- ✅ **24,875 documents** - Ready for search

### **Environment Variables You DON'T Need:**
- ❌ `CHROMADB_HOST` - Not needed for cloud
- ❌ `CHROMADB_PORT` - Not needed for cloud
- ❌ `CHROMADB_API_KEY` - Already configured in code
- ❌ `CHROMADB_TENANT` - Already configured in code
- ❌ `CHROMADB_DATABASE` - Already configured as 'newtest'

### **What You DO Need:**
- ✅ `OPENAI_API_KEY` - Your OpenAI API key
- ✅ `USE_CLOUD_CHROMA=true` - Enable cloud mode
- ✅ GPU configuration variables
- ✅ Performance optimization variables

---

## 🚀 **Deployment Commands**

### **1. Quick Deploy**
```bash
# 1. Launch Lambda Labs instance
# 2. Connect via SSH
ssh ubuntu@YOUR_INSTANCE_IP

# 3. Clone and deploy
git clone https://github.com/your-username/Lambda_MGEN_GPT.git
cd Lambda_MGEN_GPT
chmod +x lambda_deploy.sh
./lambda_deploy.sh

# 4. Create minimal .env file
cat > .env << 'EOF'
OPENAI_API_KEY=your_actual_openai_key_here
USE_CLOUD_CHROMA=true
CHROMADB_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW
CHROMADB_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130
CHROMADB_DATABASE=newtest
CUDA_VISIBLE_DEVICES=0
TORCH_CUDA_ARCH_LIST="7.5;8.0;8.6"
GPU_BATCH_SIZE=32
GPU_MEMORY_FRACTION=0.8
GPU_MIXED_PRECISION=true
LAMBDA_LABS_GPU=true
GPU_TYPE=rtx4090
HOST=0.0.0.0
PORT=8000
WORKERS=1
API_TIMEOUT=30
CORS_ORIGINS="*"
OMP_NUM_THREADS=4
TOKENIZERS_PARALLELISM=false
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
TRANSFORMERS_CACHE=/runpod-volume/transformers-cache
HF_HOME=/runpod-volume/huggingface
CACHE_TTL=3600
MAX_MEMORY_CACHE_SIZE=2147483648
MAX_DISK_CACHE_SIZE=10737418240
MAX_COLLECTIONS_PER_SEARCH=150
SEARCH_TIMEOUT=5
PARALLEL_WORKERS=8
BATCH_SIZE=32
EOF

# 5. Test and start
python3 lambda_quick_start.py
source lambda_gpu_env/bin/activate
python services/chat_service/lambda_gpu_api.py
```

---

## 🎯 **Summary**

Your Lambda Labs GPU deployment is now configured to use:
- ✅ **ChromaDB Cloud** with your existing `newtest` database
- ✅ **1,000 collections** ready for search
- ✅ **24,875 documents** available
- ✅ **No host/port configuration** needed
- ✅ **Pre-configured credentials** for immediate use

**You only need to set your `OPENAI_API_KEY` and you're ready to deploy! 🚀**
