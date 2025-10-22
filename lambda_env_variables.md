# 🔧 Lambda Labs GPU Environment Variables
## Northeastern University Chatbot - Complete Configuration Guide

This document contains all environment variables needed for the Lambda Labs GPU deployment to achieve sub-8-second response times.

---

## 📋 **Required Environment Variables**

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

# Fallback Local ChromaDB (for development only)
CHROMADB_HOST=localhost
CHROMADB_PORT=8000
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

---

## 🚀 **API Server Configuration**

### **Server Settings**
```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=1

# API Configuration
API_TIMEOUT=30
API_MAX_REQUESTS=1000
API_RATE_LIMIT=100

# CORS Settings
CORS_ORIGINS="*"
CORS_METHODS="GET,POST,PUT,DELETE,OPTIONS"
CORS_HEADERS="*"
```

---

## ⚡ **Performance Optimization**

### **CPU and Memory Settings**
```bash
# CPU Settings
OMP_NUM_THREADS=4
TOKENIZERS_PARALLELISM=false

# Memory Settings
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
TRANSFORMERS_CACHE=/runpod-volume/transformers-cache
HF_HOME=/runpod-volume/huggingface
```

### **Cache Configuration**
```bash
# Cache Settings
CACHE_TTL=3600
MAX_MEMORY_CACHE_SIZE=2147483648
MAX_DISK_CACHE_SIZE=10737418240
CACHE_CLEANUP_INTERVAL=300
```

### **Database Optimization**
```bash
# Search Settings
MAX_COLLECTIONS_PER_SEARCH=150
SEARCH_TIMEOUT=5
PARALLEL_WORKERS=8
BATCH_SIZE=32

# Collection Settings
COLLECTION_CACHE_TTL=300
COLLECTION_REFRESH_INTERVAL=600
```

---

## 🤖 **Embedding Model Configuration**

### **Model Settings**
```bash
# Model Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DEVICE=cuda
EMBEDDING_BATCH_SIZE=32
EMBEDDING_NORMALIZE=true

# Cache Settings
EMBEDDING_CACHE_FILE=lambda_gpu_embeddings_cache.pkl
EMBEDDING_CACHE_SIZE=10000
```

---

## 📊 **Logging and Monitoring**

### **Logging Configuration**
```bash
# Logging Level
LOG_LEVEL=INFO
LOG_FILE=lambda_gpu_api.log
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
HEALTH_CHECK_INTERVAL=30
```

---

## 🔒 **Security Settings**

### **API Security**
```bash
# API Security
API_KEY_REQUIRED=false
API_KEY_HEADER=X-API-Key
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# CORS Security
CORS_ALLOW_CREDENTIALS=false
CORS_MAX_AGE=3600
```

---

## 🏭 **Production Settings**

### **Production Configuration**
```bash
# Production Mode
PRODUCTION=false
SSL_ENABLED=false
SSL_CERT_PATH=
SSL_KEY_PATH=

# Load Balancing
LOAD_BALANCER=false
STICKY_SESSIONS=false
```

---

## 🎮 **Lambda Labs Specific Settings**

### **Instance Configuration**
```bash
# Instance Settings
INSTANCE_TYPE=rtx4090
INSTANCE_REGION=us-west-2
INSTANCE_ZONE=us-west-2a

# Auto-scaling
AUTO_SCALE_ENABLED=false
MIN_INSTANCES=1
MAX_INSTANCES=5
SCALE_UP_THRESHOLD=80
SCALE_DOWN_THRESHOLD=20

# Cost Optimization
SPOT_INSTANCE=false
AUTO_SHUTDOWN=true
SHUTDOWN_TIMEOUT=300
```

---

## 🔧 **Advanced Settings**

### **Model Optimization**
```bash
# Model Optimization
MODEL_OPTIMIZATION=true
QUANTIZATION=false
PRUNING=false

# Memory Management
MEMORY_MANAGEMENT=true
MEMORY_CLEANUP_INTERVAL=300
MEMORY_THRESHOLD=0.8
```

### **Network Settings**
```bash
# Network Configuration
NETWORK_TIMEOUT=30
CONNECTION_POOL_SIZE=10
RETRY_ATTEMPTS=3
```

---

## 📈 **Monitoring and Alerting**

### **Performance Monitoring**
```bash
# Performance Monitoring
PERFORMANCE_MONITORING=true
METRICS_COLLECTION=true
ALERT_THRESHOLDS=true

# Alert Settings
ALERT_EMAIL=
ALERT_WEBHOOK=
ALERT_SLACK_WEBHOOK=

# Thresholds
RESPONSE_TIME_THRESHOLD=8
GPU_UTILIZATION_THRESHOLD=90
MEMORY_USAGE_THRESHOLD=85
ERROR_RATE_THRESHOLD=5
```

---

## 🎛️ **Feature Flags**

### **Feature Toggles**
```bash
# Feature Toggles
ENABLE_GPU_ACCELERATION=true
ENABLE_CACHING=true
ENABLE_PARALLEL_SEARCH=true
ENABLE_BATCH_PROCESSING=true
ENABLE_MEMORY_OPTIMIZATION=true

# Experimental Features
EXPERIMENTAL_FEATURES=false
BETA_FEATURES=false
ALPHA_FEATURES=false
```

---

## 📝 **Complete .env File Template**

Create a `.env` file with the following content:

```bash
# =============================================================================
# CORE API KEYS (REQUIRED)
# =============================================================================
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3
OPENAI_MAX_TOKENS=3000
OPENAI_TIMEOUT=20

# =============================================================================
# CHROMADB CLOUD CONFIGURATION (REQUIRED)
# =============================================================================
USE_CLOUD_CHROMA=true
CHROMADB_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW
CHROMADB_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130
CHROMADB_DATABASE=newtest
CHROMADB_HOST=localhost
CHROMADB_PORT=8000

# =============================================================================
# GPU CONFIGURATION (REQUIRED FOR LAMBDA LABS)
# =============================================================================
CUDA_VISIBLE_DEVICES=0
TORCH_CUDA_ARCH_LIST="7.5;8.0;8.6"
GPU_BATCH_SIZE=32
GPU_MEMORY_FRACTION=0.8
GPU_MIXED_PRECISION=true
LAMBDA_LABS_GPU=true
GPU_TYPE=rtx4090

# =============================================================================
# API SERVER CONFIGURATION
# =============================================================================
HOST=0.0.0.0
PORT=8000
WORKERS=1
API_TIMEOUT=30
API_MAX_REQUESTS=1000
API_RATE_LIMIT=100
CORS_ORIGINS="*"
CORS_METHODS="GET,POST,PUT,DELETE,OPTIONS"
CORS_HEADERS="*"

# =============================================================================
# PERFORMANCE OPTIMIZATION
# =============================================================================
OMP_NUM_THREADS=4
TOKENIZERS_PARALLELISM=false
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
TRANSFORMERS_CACHE=/runpod-volume/transformers-cache
HF_HOME=/runpod-volume/huggingface
CACHE_TTL=3600
MAX_MEMORY_CACHE_SIZE=2147483648
MAX_DISK_CACHE_SIZE=10737418240
CACHE_CLEANUP_INTERVAL=300

# =============================================================================
# DATABASE OPTIMIZATION
# =============================================================================
MAX_COLLECTIONS_PER_SEARCH=150
SEARCH_TIMEOUT=5
PARALLEL_WORKERS=8
BATCH_SIZE=32
COLLECTION_CACHE_TTL=300
COLLECTION_REFRESH_INTERVAL=600

# =============================================================================
# EMBEDDING MODEL CONFIGURATION
# =============================================================================
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DEVICE=cuda
EMBEDDING_BATCH_SIZE=32
EMBEDDING_NORMALIZE=true
EMBEDDING_CACHE_FILE=lambda_gpu_embeddings_cache.pkl
EMBEDDING_CACHE_SIZE=10000

# =============================================================================
# LOGGING AND MONITORING
# =============================================================================
LOG_LEVEL=INFO
LOG_FILE=lambda_gpu_api.log
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5
ENABLE_METRICS=true
METRICS_PORT=9090
HEALTH_CHECK_INTERVAL=30

# =============================================================================
# SECURITY SETTINGS
# =============================================================================
API_KEY_REQUIRED=false
API_KEY_HEADER=X-API-Key
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
CORS_ALLOW_CREDENTIALS=false
CORS_MAX_AGE=3600

# =============================================================================
# PRODUCTION SETTINGS
# =============================================================================
PRODUCTION=false
SSL_ENABLED=false
SSL_CERT_PATH=
SSL_KEY_PATH=
LOAD_BALANCER=false
STICKY_SESSIONS=false

# =============================================================================
# LAMBDA LABS SPECIFIC SETTINGS
# =============================================================================
INSTANCE_TYPE=rtx4090
INSTANCE_REGION=us-west-2
INSTANCE_ZONE=us-west-2a
AUTO_SCALE_ENABLED=false
MIN_INSTANCES=1
MAX_INSTANCES=5
SCALE_UP_THRESHOLD=80
SCALE_DOWN_THRESHOLD=20
SPOT_INSTANCE=false
AUTO_SHUTDOWN=true
SHUTDOWN_TIMEOUT=300

# =============================================================================
# ADVANCED SETTINGS
# =============================================================================
MODEL_OPTIMIZATION=true
QUANTIZATION=false
PRUNING=false
MEMORY_MANAGEMENT=true
MEMORY_CLEANUP_INTERVAL=300
MEMORY_THRESHOLD=0.8
NETWORK_TIMEOUT=30
CONNECTION_POOL_SIZE=10
RETRY_ATTEMPTS=3

# =============================================================================
# MONITORING AND ALERTING
# =============================================================================
PERFORMANCE_MONITORING=true
METRICS_COLLECTION=true
ALERT_THRESHOLDS=true
ALERT_EMAIL=
ALERT_WEBHOOK=
ALERT_SLACK_WEBHOOK=
RESPONSE_TIME_THRESHOLD=8
GPU_UTILIZATION_THRESHOLD=90
MEMORY_USAGE_THRESHOLD=85
ERROR_RATE_THRESHOLD=5

# =============================================================================
# FEATURE FLAGS
# =============================================================================
ENABLE_GPU_ACCELERATION=true
ENABLE_CACHING=true
ENABLE_PARALLEL_SEARCH=true
ENABLE_BATCH_PROCESSING=true
ENABLE_MEMORY_OPTIMIZATION=true
EXPERIMENTAL_FEATURES=false
BETA_FEATURES=false
ALPHA_FEATURES=false
```

---

## 🚀 **Quick Setup Commands**

### **1. Create Environment File**
```bash
# Copy the template
cp lambda_env_variables.md .env

# Edit with your values
nano .env
```

### **2. Set Required Variables**
```bash
# Set your API keys
export OPENAI_API_KEY="your_actual_openai_key"
export CHROMADB_HOST="your_actual_chromadb_host"
export CHROMADB_API_KEY="your_actual_chromadb_key"
```

### **3. Validate Configuration**
```bash
# Test the configuration
python3 lambda_quick_start.py
```

---

## 📊 **Environment Variable Categories**

| Category | Variables | Purpose |
|----------|-----------|---------|
| **Core API** | 5 variables | OpenAI and ChromaDB connections |
| **GPU Config** | 7 variables | GPU acceleration settings |
| **Performance** | 12 variables | Optimization and caching |
| **Security** | 8 variables | API security and CORS |
| **Monitoring** | 10 variables | Logging and alerting |
| **Lambda Labs** | 8 variables | Instance and scaling settings |
| **Advanced** | 15 variables | Model optimization and networking |
| **Feature Flags** | 8 variables | Feature toggles and experiments |

**Total: 73 environment variables** for complete configuration control.

---

## ✅ **Validation Checklist**

- [ ] OpenAI API key set and valid
- [ ] ChromaDB connection configured
- [ ] GPU settings optimized for your instance
- [ ] Performance settings tuned
- [ ] Security settings configured
- [ ] Monitoring enabled
- [ ] Feature flags set appropriately

**Your Lambda Labs GPU deployment is now fully configured for sub-8-second response times! 🚀**
