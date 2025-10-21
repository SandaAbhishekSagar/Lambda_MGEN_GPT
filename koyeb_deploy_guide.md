# Koyeb Deployment Guide - Northeastern University Chatbot

## 🚀 **Why Koyeb?**

- **Easier than RunPod** - No complex GPU configuration needed
- **GitHub integration** - Direct deployment from your repository
- **Automatic scaling** - Handles traffic spikes automatically
- **Cost-effective** - Pay only for what you use
- **Fast deployment** - Deploy in minutes

## 📋 **Prerequisites**

- Koyeb account (free tier available)
- GitHub repository with your code
- OpenAI API key
- ChromaDB Cloud credentials

## 🔧 **Koyeb Deployment Steps**

### **Step 1: Create Koyeb Account**
1. Go to [Koyeb Console](https://app.koyeb.com/)
2. Sign up with GitHub (recommended)
3. Connect your GitHub account

### **Step 2: Deploy from GitHub**
1. **Click "Create App"** in Koyeb console
2. **Select "GitHub"** as source
3. **Choose your repository**: `Lambda_MGEN_GPT` or `MGENGPT`
4. **Select branch**: `main`
5. **Configure settings**:
   - **Name**: `northeastern-chatbot`
   - **Region**: Choose closest to your users
   - **Instance Type**: `Starter` (free tier) or `Professional` (paid)

### **Step 3: Configure Environment Variables**
In Koyeb console, set these environment variables:

```
OPENAI_API_KEY=your_openai_api_key_here
CHROMA_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW
CHROMA_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130
CHROMA_DATABASE=newtest
CHROMA_HOST=localhost
CHROMA_PORT=8000
```

### **Step 4: Configure Build Settings**
- **Build Command**: `pip install -r requirements_minimal.txt`
- **Start Command**: `python runpod_handler.py`
- **Port**: `8000` (or let Koyeb auto-detect)

## 🎯 **Koyeb vs RunPod Comparison**

| Feature | Koyeb | RunPod |
|---------|-------|--------|
| **Setup** | ✅ Easy | ❌ Complex |
| **GitHub Integration** | ✅ Native | ❌ Issues |
| **GPU Support** | ❌ CPU only | ✅ GPU available |
| **Cost** | ✅ Pay per use | ❌ Fixed pricing |
| **Scaling** | ✅ Automatic | ❌ Manual |
| **Deployment Time** | ✅ 2-3 minutes | ❌ 10-15 minutes |

## 🚀 **Expected Performance on Koyeb**

- **Response Time**: 8-12 seconds (CPU-based)
- **Concurrent Requests**: Up to 10
- **Cold Start**: 30-60 seconds
- **Uptime**: 99.9%

## 📊 **Cost Estimation**

### **Koyeb Pricing**
- **Starter**: Free (limited resources)
- **Professional**: $0.10/hour (~$72/month)
- **Enterprise**: Custom pricing

### **RunPod Pricing**
- **RTX 4090**: $0.50/hour (~$360/month)
- **A100**: $1.50/hour (~$1080/month)

**Koyeb is 5-15x cheaper than RunPod!**

## 🔧 **Optimization for Koyeb**

### **CPU Optimization**
Since Koyeb doesn't have GPU, we'll optimize for CPU:

1. **Use CPU-only PyTorch** (already in Dockerfile)
2. **Optimize model size** - Use smaller models
3. **Implement caching** - Cache responses
4. **Connection pooling** - Reuse connections

### **Performance Tips**
- **Warm-up requests** - Send periodic requests to keep instance warm
- **Response caching** - Cache common responses
- **Connection reuse** - Reuse ChromaDB connections
- **Async processing** - Use async/await for better performance

## 🧪 **Testing Your Koyeb Deployment**

### **Test Endpoint**
Once deployed, your chatbot will be available at:
```
https://your-app-name.koyeb.app
```

### **Test Input**
```json
{
    "input": {
        "question": "What undergraduate programs does Northeastern offer?"
    }
}
```

### **Expected Response**
```json
{
    "answer": "Northeastern University offers a wide range of undergraduate programs...",
    "sources": [...],
    "confidence": "high",
    "timing": {
        "search": 2.5,
        "generation": 5.2,
        "total": 7.7
    }
}
```

## 🎯 **Next Steps**

1. **Create Koyeb account**
2. **Deploy from GitHub**
3. **Set environment variables**
4. **Test the deployment**
5. **Monitor performance**
6. **Scale as needed**

## 📞 **Support**

- **Koyeb Documentation**: https://docs.koyeb.com/
- **Koyeb Community**: https://community.koyeb.com/
- **Koyeb Support**: Available in console

---

**Koyeb is the perfect choice for your chatbot - easier, cheaper, and more reliable than RunPod!**
