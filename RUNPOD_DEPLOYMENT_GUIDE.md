# RunPod Deployment Guide - Northeastern University Chatbot

## 🚀 Quick Start

This guide will help you deploy your Northeastern University chatbot to RunPod with GPU acceleration for 5-8 second response times.

## 📋 Prerequisites

- RunPod account
- Docker Hub account
- OpenAI API key
- ChromaDB cloud instance
- Docker installed locally

## 🏗️ Architecture

```
User Query → RunPod GPU → OpenAI Embeddings → ChromaDB Search → GPT-4o-mini → Response
```

**Performance Target**: 5-8 seconds response time
**GPU Requirements**: 16GB+ VRAM (RTX 4090, A100, or V100)

## 📁 Files Created

1. **`runpod_optimized_handler.py`** - Optimized handler with GPU acceleration
2. **`Dockerfile.runpod`** - Optimized Docker configuration
3. **`requirements_runpod.txt`** - Minimal dependencies
4. **`test_input_runpod.json`** - Test input for local testing
5. **`runpod_deploy.sh`** - Deployment script
6. **`runpod_config.yaml`** - Configuration template
7. **`runpod_quick_test.py`** - Local testing script

## 🚀 Deployment Steps

### Step 1: Set Environment Variables

```bash
export DOCKER_USERNAME="your-docker-username"
export OPENAI_API_KEY="your-openai-key"
export CHROMA_API_KEY="your-chroma-key"
export CHROMA_HOST="your-chroma-host"
export CHROMA_PORT="8000"
```

### Step 2: Test Locally

```bash
# Install dependencies
pip install -r requirements_runpod.txt

# Test the handler
python runpod_quick_test.py
```

### Step 3: Build and Deploy

```bash
# Make deployment script executable
chmod +x runpod_deploy.sh

# Run deployment
./runpod_deploy.sh
```

### Step 4: Configure RunPod Endpoint

1. Go to [RunPod Serverless Console](https://console.runpod.io/serverless)
2. Click **New Endpoint**
3. Select **Import from Docker Registry**
4. Enter your Docker image: `docker.io/your-username/northeastern-chatbot:v1.0.0`
5. Configure settings:
   - **GPU Type**: RTX 4090 or A100 (16GB+)
   - **Workers**: 1
   - **Timeout**: 300 seconds
6. Set environment variables:
   - `OPENAI_API_KEY`
   - `CHROMA_API_KEY`
   - `CHROMA_HOST`
   - `CHROMA_PORT`
7. Deploy!

## ⚡ Performance Optimizations

### GPU Acceleration
- PyTorch with CUDA support
- Optimized embedding generation
- Concurrent document searches
- Cached collection metadata

### Response Time Optimizations
- Limited to 6 documents per query
- Top 3 documents for context
- Reduced prompt length
- Faster OpenAI model (gpt-4o-mini)
- Concurrent collection searches

### Memory Optimizations
- Minimal dependencies
- Efficient ChromaDB queries
- Collection caching (5-minute TTL)
- Optimized batch processing

## 🧪 Testing

### Local Testing
```bash
python runpod_quick_test.py
```

### RunPod Testing
1. Go to your endpoint in RunPod console
2. Click **Requests** tab
3. Use test input:
```json
{
    "input": {
        "question": "What undergraduate programs does Northeastern offer?"
    }
}
```

## 📊 Expected Performance

- **Response Time**: 5-8 seconds
- **GPU Memory**: 8-12GB usage
- **Concurrent Requests**: Up to 5
- **Cold Start**: ~30-60 seconds

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY` - Your OpenAI API key
- `CHROMA_API_KEY` - Your ChromaDB API key
- `CHROMA_HOST` - ChromaDB host URL
- `CHROMA_PORT` - ChromaDB port (default: 8000)
- `CHROMA_TENANT` - ChromaDB tenant (optional)
- `CHROMA_DATABASE` - ChromaDB database (optional)

### GPU Settings
- **Minimum**: 16GB VRAM
- **Recommended**: 24GB+ VRAM
- **GPU Types**: RTX 4090, A100, V100

## 🚨 Troubleshooting

### Common Issues

1. **Slow Response Times**
   - Check GPU availability
   - Verify ChromaDB connection
   - Check collection count

2. **Memory Errors**
   - Reduce concurrent searches
   - Limit document count
   - Use smaller GPU

3. **Connection Errors**
   - Verify ChromaDB credentials
   - Check network connectivity
   - Validate API keys

### Debug Mode
```bash
# Enable debug logging
export PYTHONUNBUFFERED=1
python runpod_optimized_handler.py
```

## 📈 Monitoring

### Key Metrics
- Response time per request
- GPU memory usage
- ChromaDB query time
- OpenAI API latency

### Logs
- Handler initialization
- Search performance
- Generation timing
- Error tracking

## 🔄 Updates

To update your deployment:

1. Modify code
2. Update version in `runpod_deploy.sh`
3. Rebuild and push image
4. Update endpoint in RunPod console

## 💰 Cost Optimization

- Use smaller GPU for development
- Implement request caching
- Optimize ChromaDB queries
- Monitor usage patterns

## 🎯 Next Steps

1. Deploy to RunPod
2. Test with real queries
3. Monitor performance
4. Optimize based on usage
5. Scale as needed

## 📞 Support

For issues:
1. Check RunPod logs
2. Verify environment variables
3. Test locally first
4. Contact RunPod support

---

**Ready to deploy? Run `./runpod_deploy.sh` and follow the prompts!**