# Northeastern University Chatbot - RunPod GitHub Deployment

🚀 **GPU-accelerated RAG chatbot for Northeastern University with 5-8 second response times**

## 🏗️ Architecture

```
User Query → RunPod GPU → OpenAI Embeddings → ChromaDB Search → GPT-4o-mini → Response
```

**Performance Target**: 5-8 seconds response time  
**GPU Requirements**: 16GB+ VRAM (RTX 4090, A100, or V100)

## 🚀 Quick Start

### Prerequisites
- GitHub account
- RunPod account  
- OpenAI API key
- ChromaDB cloud instance

### Deploy via GitHub

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add RunPod GitHub deployment"
   git push origin main
   ```

2. **Authorize RunPod with GitHub**
   - Go to [RunPod Settings](https://console.runpod.io/user/settings)
   - Connect your GitHub account
   - Grant repository access

3. **Deploy from GitHub**
   - Go to [RunPod Serverless Console](https://console.runpod.io/serverless)
   - Click **New Endpoint**
   - Select **Import Git Repository**
   - Choose your repository and branch
   - Configure GPU settings (RTX 4090 or A100)
   - Set environment variables
   - Deploy!

## 📁 Project Structure

```
├── runpod_handler.py              # Main RunPod handler
├── Dockerfile                     # GitHub deployment Dockerfile
├── requirements_runpod.txt        # Optimized dependencies
├── .github/
│   ├── workflows/
│   │   └── test-and-deploy.yml    # GitHub Actions workflow
│   └── tests.json                 # Test cases
├── test_input_runpod.json        # Test input
├── runpod_quick_test.py          # Local testing
└── GITHUB_DEPLOYMENT_GUIDE.md    # Detailed deployment guide
```

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
- Concurrent collection searches (8 threads)

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

### GitHub Actions Testing
- Automated testing on every push
- Docker image validation
- Handler functionality tests

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

## 🔧 Configuration

### Environment Variables
```
OPENAI_API_KEY=your_openai_api_key_here
CHROMA_API_KEY=your_chroma_api_key_here
CHROMA_HOST=your_chroma_host_here
CHROMA_PORT=8000
CHROMA_TENANT=default_tenant
CHROMA_DATABASE=default_database
```

### GPU Settings
- **Minimum**: 16GB VRAM
- **Recommended**: 24GB+ VRAM
- **GPU Types**: RTX 4090, A100, V100

## 📊 Expected Performance

- **Response Time**: 5-8 seconds
- **GPU Memory**: 8-12GB usage
- **Cold Start**: 30-60 seconds
- **Concurrent Requests**: Up to 5

## 🔄 Updates

### Method 1: Push to Main Branch
```bash
git add .
git commit -m "Update chatbot features"
git push origin main
```

### Method 2: Create a Release (Recommended)
1. Go to GitHub repository
2. Click **Releases** → **Create a new release**
3. Tag version: `v1.0.0`
4. Publish release

## 🚨 Troubleshooting

### Common Issues
1. **Build Failures** - Check Dockerfile syntax
2. **Deployment Issues** - Verify environment variables
3. **Performance Issues** - Monitor GPU memory usage

### Debug Steps
1. Check RunPod build logs
2. Test locally with `python runpod_quick_test.py`
3. Verify all environment variables
4. Check ChromaDB connection

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

## 💰 Cost Management

### GPU Selection
- **Development**: RTX 4090 (24GB) - $0.50/hour
- **Production**: A100 (40GB) - $1.50/hour

### Optimization Strategies
- Use smaller GPU for testing
- Implement request caching
- Monitor usage patterns
- Scale based on demand

## 🎯 Next Steps

1. **Deploy to RunPod** using GitHub integration
2. **Test with real queries** to validate performance
3. **Monitor usage** and optimize as needed
4. **Scale up** based on demand
5. **Set up monitoring** and alerts

## 📞 Support

### GitHub Issues
- Create issues in your repository
- Use GitHub Discussions for questions
- Check GitHub Actions logs

### RunPod Support
- Check RunPod documentation
- Contact RunPod support
- Monitor RunPod status page

---

**Ready to deploy? Push your code to GitHub and follow the RunPod console steps!**