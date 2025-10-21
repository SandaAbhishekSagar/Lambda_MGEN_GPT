# GitHub Deployment Guide - RunPod Integration

## 🚀 Deploy Your Northeastern University Chatbot via GitHub

This guide will help you deploy your chatbot directly from GitHub to RunPod, eliminating the need for Docker Hub.

## 📋 Prerequisites

- GitHub account
- RunPod account
- OpenAI API key
- ChromaDB cloud instance

## 🏗️ GitHub Integration Benefits

- **No Docker Hub needed** - Direct deployment from GitHub
- **Automatic builds** - RunPod builds your image
- **Version control** - Track changes with Git
- **Easy updates** - Push to GitHub to update
- **CI/CD ready** - GitHub Actions integration

## 📁 Files Created for GitHub Deployment

1. **`Dockerfile`** - Main Dockerfile for GitHub deployment
2. **`.github/workflows/test-and-deploy.yml`** - GitHub Actions workflow
3. **`.github/tests.json`** - Test cases for validation
4. **`GITHUB_DEPLOYMENT_GUIDE.md`** - This guide

## 🚀 Step-by-Step Deployment

### Step 1: Push to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit changes
git commit -m "Add RunPod GitHub deployment setup"

# Add your GitHub repository
git remote add origin https://github.com/your-username/your-repo.git

# Push to GitHub
git push -u origin main
```

### Step 2: Authorize RunPod with GitHub

1. Go to [RunPod Settings](https://console.runpod.io/user/settings)
2. Find **GitHub** under **Connections**
3. Click **Connect**
4. Authorize RunPod to access your repositories
5. Choose repository access:
   - **All repositories** (recommended)
   - **Only select repositories** (choose your chatbot repo)

### Step 3: Deploy from GitHub

1. Go to [RunPod Serverless Console](https://console.runpod.io/serverless)
2. Click **New Endpoint**
3. Under **Import Git Repository**:
   - Select your repository from the dropdown
   - Choose **Branch**: `main`
   - **Dockerfile Path**: `/` (root directory)
4. Click **Next**

### Step 4: Configure Endpoint

**Endpoint Settings:**
- **Name**: `northeastern-university-chatbot`
- **Type**: `Queue` (recommended)
- **GPU Configuration**: 
  - Select **RTX 4090** or **A100** (16GB+)
  - Minimum 16GB VRAM required

**Environment Variables:**
```
OPENAI_API_KEY=your_openai_api_key_here
CHROMA_API_KEY=your_chroma_api_key_here
CHROMA_HOST=your_chroma_host_here
CHROMA_PORT=8000
CHROMA_TENANT=default_tenant
CHROMA_DATABASE=default_database
```

**Advanced Settings:**
- **Workers**: 1
- **Timeout**: 300 seconds
- **Max Concurrent**: 5

### Step 5: Deploy and Test

1. Click **Deploy Endpoint**
2. Wait for build to complete (5-10 minutes)
3. Go to **Requests** tab
4. Test with:
```json
{
    "input": {
        "question": "What undergraduate programs does Northeastern offer?"
    }
}
```

## 🔄 Updating Your Deployment

### Method 1: Push to Main Branch
```bash
# Make changes to your code
git add .
git commit -m "Update chatbot features"
git push origin main
```

### Method 2: Create a Release (Recommended)
1. Go to your GitHub repository
2. Click **Releases** → **Create a new release**
3. Tag version: `v1.0.0`
4. Release title: `Northeastern Chatbot v1.0.0`
5. Click **Publish release**

## 🧪 Testing with GitHub Actions

Your repository includes automated testing:

### Test Cases
- Undergraduate programs question
- Admission requirements question
- Tuition cost question

### Manual Testing
```bash
# Test locally before pushing
python runpod_quick_test.py
```

### GitHub Actions Testing
- Runs on every push to `main`
- Runs on pull requests
- Tests Docker image build
- Validates handler functionality

## 📊 Monitoring Your Deployment

### Build Status
1. Go to your endpoint in RunPod console
2. Click **Builds** tab
3. Monitor build progress:
   - **Pending** → **Building** → **Uploading** → **Testing** → **Completed**

### Request Monitoring
1. Go to **Requests** tab
2. Monitor response times
3. Check for errors
4. View detailed logs

## 🔧 Configuration Files

### Dockerfile
```dockerfile
FROM python:3.11-slim
# GPU-optimized PyTorch installation
# Minimal dependencies
# Security hardening
```

### GitHub Actions Workflow
```yaml
name: Test and Deploy Northeastern Chatbot
# Automated testing
# Docker image building
# Deployment validation
```

### Test Configuration
```json
[
  {
    "input": {
      "question": "What undergraduate programs does Northeastern offer?"
    },
    "expected_output": {
      "status": "COMPLETED"
    }
  }
]
```

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check Dockerfile syntax
   - Verify requirements.txt
   - Check GitHub Actions logs

2. **Deployment Issues**
   - Verify environment variables
   - Check RunPod logs
   - Ensure GPU availability

3. **Performance Issues**
   - Monitor GPU memory usage
   - Check ChromaDB connection
   - Verify OpenAI API limits

### Debug Steps

1. **Check Build Logs**
   - Go to RunPod console
   - Click **Builds** tab
   - Review build logs

2. **Test Locally**
   ```bash
   python runpod_quick_test.py
   ```

3. **Verify Environment**
   - Check all environment variables
   - Verify API keys
   - Test ChromaDB connection

## 📈 Performance Optimization

### Expected Performance
- **Response Time**: 5-8 seconds
- **GPU Memory**: 8-12GB usage
- **Cold Start**: 30-60 seconds
- **Concurrent Requests**: Up to 5

### Optimization Tips
- Use smaller GPU for development
- Implement request caching
- Monitor usage patterns
- Optimize ChromaDB queries

## 🔄 Multiple Environments

### Production Environment
- **Branch**: `main`
- **GPU**: RTX 4090 or A100
- **Workers**: 1-2

### Staging Environment
- **Branch**: `develop`
- **GPU**: RTX 4090 (smaller)
- **Workers**: 1

### Development Environment
- **Branch**: `feature/*`
- **GPU**: RTX 4090
- **Workers**: 1

## 💰 Cost Management

### GPU Selection
- **Development**: RTX 4090 (24GB) - $0.50/hour
- **Production**: A100 (40GB) - $1.50/hour
- **Staging**: RTX 4090 (24GB) - $0.50/hour

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
