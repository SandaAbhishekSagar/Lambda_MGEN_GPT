#!/bin/bash

# RunPod Deployment via Docker Hub
# This script builds and pushes your image to Docker Hub for RunPod

set -e

echo "🚀 RunPod Docker Hub Deployment"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Step 1: Check Docker login
echo -e "${YELLOW}[1/5] Checking Docker Hub login...${NC}"
if ! docker info | grep -q "Username"; then
    echo -e "${RED}❌ Not logged in to Docker Hub${NC}"
    echo "Please login first:"
    echo "  docker login"
    exit 1
fi

DOCKER_USERNAME=$(docker info | grep Username | awk '{print $2}')
echo -e "${GREEN}✅ Logged in as: $DOCKER_USERNAME${NC}"

# Step 2: Build image
echo -e "${YELLOW}[2/5] Building Docker image...${NC}"
docker build -f Dockerfile.runpod -t northeastern-chatbot:runpod .
echo -e "${GREEN}✅ Image built${NC}"

# Step 3: Tag image
echo -e "${YELLOW}[3/5] Tagging image...${NC}"
IMAGE_NAME="$DOCKER_USERNAME/northeastern-chatbot:runpod"
docker tag northeastern-chatbot:runpod $IMAGE_NAME
echo -e "${GREEN}✅ Tagged as: $IMAGE_NAME${NC}"

# Step 4: Push to Docker Hub
echo -e "${YELLOW}[4/5] Pushing to Docker Hub...${NC}"
docker push $IMAGE_NAME
echo -e "${GREEN}✅ Pushed successfully${NC}"

# Step 5: Show RunPod instructions
echo ""
echo "================================================================"
echo -e "${GREEN}✅ DOCKER IMAGE READY!${NC}"
echo "================================================================"
echo ""
echo "📋 RunPod Serverless Configuration:"
echo ""
echo "1. Go to: https://runpod.io/console/serverless"
echo ""
echo "2. Click '+ New Endpoint'"
echo ""
echo "3. Configure:"
echo ""
echo "   Container Image:"
echo "   ┌─────────────────────────────────────────────────┐"
echo "   │ $IMAGE_NAME"
echo "   └─────────────────────────────────────────────────┘"
echo ""
echo "   GPU Type: RTX 4090 (24GB)"
echo "   Container Disk: 20 GB"
echo ""
echo "   Workers:"
echo "   - Min: 0"
echo "   - Max: 10"
echo "   - Idle Timeout: 30s"
echo ""
echo "4. Add Environment Variables:"
echo ""
echo "   OPENAI_API_KEY=sk-your-key-here"
echo "   CHROMA_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW"
echo "   CHROMA_HOST=api.trychroma.com"
echo "   CHROMA_PORT=8000"
echo "   CHROMA_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130"
echo "   CHROMA_DATABASE=newtest"
echo "   PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512"
echo ""
echo "5. Click 'Deploy'"
echo ""
echo "6. Copy your endpoint URL:"
echo "   https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync"
echo ""
echo "================================================================"
echo ""
echo -e "${GREEN}🎉 Ready to deploy on RunPod!${NC}"
echo ""

