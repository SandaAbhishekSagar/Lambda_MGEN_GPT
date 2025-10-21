#!/bin/bash

# RunPod Deployment Script
# Northeastern University Chatbot

set -e  # Exit on error

echo "🚀 RunPod Serverless Deployment Script"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if RunPod CLI is installed
if ! command -v runpodctl &> /dev/null; then
    echo -e "${YELLOW}RunPod CLI not found. Installing...${NC}"
    pip install runpod
fi

# Check if logged in to RunPod
echo -e "${YELLOW}[1/6] Checking RunPod authentication...${NC}"
if ! runpodctl config &> /dev/null; then
    echo -e "${RED}❌ Not logged in to RunPod${NC}"
    echo ""
    echo "Please login to RunPod:"
    echo "1. Get your API key from: https://runpod.io/console/user/settings"
    echo "2. Run: runpodctl config --apiKey YOUR_API_KEY"
    echo ""
    exit 1
fi
echo -e "${GREEN}✅ RunPod authentication verified${NC}"

# Check environment variables
echo -e "${YELLOW}[2/6] Checking environment variables...${NC}"
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${RED}❌ OPENAI_API_KEY not set${NC}"
    echo "Please set: export OPENAI_API_KEY='your-key-here'"
    exit 1
fi
if [ -z "$CHROMA_API_KEY" ]; then
    echo -e "${RED}❌ CHROMA_API_KEY not set${NC}"
    echo "Please set: export CHROMA_API_KEY='your-key-here'"
    exit 1
fi
if [ -z "$CHROMA_HOST" ]; then
    echo -e "${YELLOW}⚠️  CHROMA_HOST not set, using default: api.trychroma.com${NC}"
    export CHROMA_HOST="api.trychroma.com"
fi
echo -e "${GREEN}✅ Environment variables verified${NC}"

# Build Docker image
echo -e "${YELLOW}[3/6] Building Docker image...${NC}"
docker build -f Dockerfile.runpod -t northeastern-chatbot:runpod .
echo -e "${GREEN}✅ Docker image built successfully${NC}"

# Tag image for RunPod
echo -e "${YELLOW}[4/6] Tagging image...${NC}"
DOCKER_USERNAME=$(docker info | grep Username | awk '{print $2}')
if [ -z "$DOCKER_USERNAME" ]; then
    echo -e "${RED}❌ Not logged in to Docker Hub${NC}"
    echo "Please login: docker login"
    exit 1
fi
docker tag northeastern-chatbot:runpod $DOCKER_USERNAME/northeastern-chatbot:runpod
echo -e "${GREEN}✅ Image tagged: $DOCKER_USERNAME/northeastern-chatbot:runpod${NC}"

# Push to Docker Hub
echo -e "${YELLOW}[5/6] Pushing image to Docker Hub...${NC}"
docker push $DOCKER_USERNAME/northeastern-chatbot:runpod
echo -e "${GREEN}✅ Image pushed successfully${NC}"

# Deploy to RunPod
echo -e "${YELLOW}[6/6] Deploying to RunPod...${NC}"

cat << EOF

📋 Manual Deployment Steps:

1. Go to: https://runpod.io/console/serverless

2. Click "New Endpoint"

3. Configure your endpoint:
   
   Basic Settings:
   - Name: northeastern-chatbot
   - Container Image: $DOCKER_USERNAME/northeastern-chatbot:runpod
   - Container Disk: 20 GB
   
   GPU Configuration:
   - GPU Type: RTX 4090 (recommended) or A40/A100
   - Workers: 
     - Min: 0
     - Max: 10
     - Idle Timeout: 30 seconds
   
   Environment Variables:
   - OPENAI_API_KEY: $OPENAI_API_KEY
   - CHROMA_API_KEY: $CHROMA_API_KEY
   - CHROMA_HOST: $CHROMA_HOST
   - CHROMA_PORT: 8000
   - CHROMA_TENANT: default_tenant
   - CHROMA_DATABASE: default_database
   - PYTORCH_CUDA_ALLOC_CONF: max_split_size_mb:512

4. Click "Deploy"

5. Wait for deployment (2-3 minutes)

6. Copy your endpoint URL:
   - It will look like: https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync

7. Update your frontend config.js with the endpoint URL

8. Test your endpoint!

EOF

echo -e "${GREEN}✅ Deployment preparation complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Follow the manual deployment steps above"
echo "2. Copy your RunPod endpoint URL"
echo "3. Update frontend/config.js"
echo "4. Deploy frontend to Vercel"
echo ""
echo "🎉 Your chatbot will be live on RunPod with automatic HTTPS!"

