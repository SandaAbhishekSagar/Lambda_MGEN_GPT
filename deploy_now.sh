#!/bin/bash

# Deploy Northeastern University Chatbot to RunPod via Docker Hub
# Using Docker Hub username: abhisheksagar308

echo "Deploying Northeastern University Chatbot to RunPod"
echo "=================================================="

# Configuration
DOCKER_USERNAME="abhisheksagar308"
IMAGE_NAME="northeastern-chatbot"
VERSION="latest"

echo "Configuration:"
echo "  Docker Username: $DOCKER_USERNAME"
echo "  Image Name: $IMAGE_NAME"
echo "  Version: $VERSION"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "Step 1: Building Docker image..."
docker build -t $IMAGE_NAME:$VERSION .

if [ $? -ne 0 ]; then
    echo "Error: Docker build failed!"
    exit 1
fi

echo "Step 2: Testing Docker image..."
docker run --rm $IMAGE_NAME:$VERSION python -c "print('Docker image test successful')"

if [ $? -ne 0 ]; then
    echo "Error: Docker image test failed!"
    exit 1
fi

echo "Step 3: Tagging for Docker Hub..."
docker tag $IMAGE_NAME:$VERSION $DOCKER_USERNAME/$IMAGE_NAME:$VERSION

echo "Step 4: Pushing to Docker Hub..."
docker push $DOCKER_USERNAME/$IMAGE_NAME:$VERSION

if [ $? -ne 0 ]; then
    echo "Error: Docker push failed!"
    echo "Make sure you're logged into Docker Hub: docker login"
    exit 1
fi

echo ""
echo "Deployment Complete!"
echo "===================="
echo "Image: $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
echo ""
echo "Next steps:"
echo "1. Go to https://console.runpod.io/serverless"
echo "2. Click 'New Endpoint'"
echo "3. Select 'Import from Docker Registry'"
echo "4. Enter: docker.io/abhisheksagar308/northeastern-chatbot:latest"
echo "5. Configure GPU settings (recommend 16GB+ GPU)"
echo "6. Set environment variables:"
echo "   - OPENAI_API_KEY=your_openai_key"
echo "   - CHROMA_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW"
echo "   - CHROMA_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130"
echo "   - CHROMA_DATABASE=newtest"
echo "   - CHROMA_HOST=localhost"
echo "   - CHROMA_PORT=8000"
echo "7. Deploy and test!"
echo ""
echo "Test input for RunPod:"
echo '{"input": {"question": "What undergraduate programs does Northeastern offer?"}}'
