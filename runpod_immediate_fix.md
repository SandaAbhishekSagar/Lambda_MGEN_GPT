# RunPod Immediate Fix - Tag Format Issue

## 🚨 **Root Cause**
The error `invalid tag "registry.runpod.net/sandaabhisheksagar-mgengpt-main-:af9ca9280"` shows that RunPod is generating malformed Docker tags with an empty repository name before the colon.

## 🔧 **Immediate Solutions**

### **Option 1: Use Docker Hub Deployment (Fastest)**

1. **Build and push to Docker Hub:**
   ```bash
   # Set your Docker Hub username
   export DOCKER_USERNAME="your-docker-username"
   
   # Build the image
   docker build -t northeastern-chatbot:latest .
   
   # Tag for Docker Hub
   docker tag northeastern-chatbot:latest $DOCKER_USERNAME/northeastern-chatbot:latest
   
   # Push to Docker Hub
   docker push $DOCKER_USERNAME/northeastern-chatbot:latest
   ```

2. **Deploy from Docker Hub in RunPod:**
   - Go to [RunPod Console](https://console.runpod.io/serverless)
   - Click **New Endpoint**
   - Select **Import from Docker Registry**
   - Enter: `docker.io/your-username/northeastern-chatbot:latest`
   - Configure settings and deploy

### **Option 2: Fix Repository Name (Alternative)**

Try a completely different repository name:

1. **Create new repository** with a simple name:
   - Name: `northeastern-chatbot`
   - Description: `Northeastern University Chatbot for RunPod`
   - Make it public

2. **Push your code to the new repository:**
   ```bash
   git remote add origin https://github.com/your-username/northeastern-chatbot.git
   git push -u origin main
   ```

3. **Deploy from the new repository in RunPod**

### **Option 3: Manual Docker Build (If GitHub continues to fail)**

1. **Build locally:**
   ```bash
   docker build -t northeastern-chatbot:latest .
   ```

2. **Test locally:**
   ```bash
   docker run --rm northeastern-chatbot:latest python -c "print('Test successful')"
   ```

3. **Push to Docker Hub:**
   ```bash
   docker tag northeastern-chatbot:latest your-username/northeastern-chatbot:latest
   docker push your-username/northeastern-chatbot:latest
   ```

## 🎯 **Recommended Immediate Action**

### **Step 1: Use Docker Hub (Fastest)**
This bypasses the GitHub integration issue entirely:

1. **Build and push to Docker Hub** (see commands above)
2. **Deploy from Docker Hub** in RunPod console
3. **Set environment variables** in RunPod
4. **Test the deployment**

### **Step 2: Environment Variables for RunPod**
Set these in your RunPod endpoint:

```
OPENAI_API_KEY=your_openai_api_key_here
CHROMA_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW
CHROMA_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130
CHROMA_DATABASE=newtest
CHROMA_HOST=localhost
CHROMA_PORT=8000
```

## 🔍 **Why This Happens**

The issue is with RunPod's tag generation algorithm:
- **Repository name parsing** fails with certain formats
- **Tag format** becomes malformed: `registry.runpod.net/username-repo-branch-:commit`
- **Empty repository name** before the colon causes Docker build failure

## 📋 **Quick Fix Checklist**

- [ ] Build Docker image locally
- [ ] Push to Docker Hub
- [ ] Create RunPod endpoint from Docker Hub
- [ ] Set environment variables
- [ ] Test deployment

## 🚀 **Expected Results**

After using Docker Hub deployment:
- ✅ Bypasses GitHub integration issues
- ✅ Clean Docker tag format
- ✅ Successful build and deployment
- ✅ Ready for testing

---

**The fastest solution is to use Docker Hub deployment to bypass the GitHub integration issue entirely!**
