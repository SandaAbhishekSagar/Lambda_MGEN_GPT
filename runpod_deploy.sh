#!/bin/bash

# RunPod Deployment Script for Northeastern University Chatbot
# Optimized for GPU acceleration and 5-8 second response times

echo "🚀 RunPod Deployment Script - Northeastern University Chatbot"
echo "=============================================================="

# Configuration
DOCKER_USERNAME=${DOCKER_USERNAME:-"your-docker-username"}
WORKER_NAME="northeastern-chatbot"
VERSION="v1.0.0"
PLATFORM="linux/amd64"

echo "📋 Configuration:"
echo "  Docker Username: $DOCKER_USERNAME"
echo "  Worker Name: $WORKER_NAME"
echo "  Version: $VERSION"
echo "  Platform: $PLATFORM"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if user is logged into Docker Hub
if ! docker info | grep -q "Username"; then
    echo "⚠️  Warning: You may not be logged into Docker Hub."
    echo "   Run 'docker login' if you encounter authentication issues."
fi

echo "🔧 Building Docker image..."
docker build --platform $PLATFORM -t $DOCKER_USERNAME/$WORKER_NAME:$VERSION -f Dockerfile.runpod .

if [ $? -ne 0 ]; then
    echo "❌ Error: Docker build failed!"
    exit 1
fi

echo "✅ Docker image built successfully!"

echo "📤 Pushing image to Docker Hub..."
docker push $DOCKER_USERNAME/$WORKER_NAME:$VERSION

if [ $? -ne 0 ]; then
    echo "❌ Error: Docker push failed!"
    echo "   Make sure you're logged into Docker Hub: docker login"
    exit 1
fi

echo "✅ Image pushed successfully!"

echo ""
echo "🎉 Deployment Complete!"
echo "=========================="
echo "Image: $DOCKER_USERNAME/$WORKER_NAME:$VERSION"
echo ""
echo "Next steps:"
echo "1. Go to https://console.runpod.io/serverless"
echo "2. Click 'New Endpoint'"
echo "3. Select 'Import from Docker Registry'"
echo "4. Enter: docker.io/$DOCKER_USERNAME/$WORKER_NAME:$VERSION"
echo "5. Configure GPU settings (recommend 16GB+ GPU)"
echo "6. Set environment variables:"
echo "   - OPENAI_API_KEY=your_openai_key"
echo "   - CHROMA_API_KEY=your_chroma_key"
echo "   - CHROMA_HOST=your_chroma_host"
echo "   - CHROMA_PORT=8000"
echo "7. Deploy and test!"
echo ""
echo "For local testing:"
echo "python runpod_optimized_handler.py"
