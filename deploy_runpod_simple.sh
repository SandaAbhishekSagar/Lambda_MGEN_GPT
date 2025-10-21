#!/bin/bash

# Simple RunPod Deployment (No Docker Hub Required)
# Uses RunPod's built-in image registry

set -e

echo "🚀 Simple RunPod Deployment"
echo "============================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Install RunPod Python SDK
echo -e "${YELLOW}[1/3] Installing RunPod SDK...${NC}"
pip install -q runpod
echo -e "${GREEN}✅ RunPod SDK installed${NC}"

# Check environment variables
echo -e "${YELLOW}[2/3] Checking environment variables...${NC}"

if [ -z "$RUNPOD_API_KEY" ]; then
    echo -e "${RED}❌ RUNPOD_API_KEY not set${NC}"
    echo ""
    echo "Get your API key from: https://runpod.io/console/user/settings"
    echo "Then run: export RUNPOD_API_KEY='your-runpod-api-key'"
    exit 1
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${RED}❌ OPENAI_API_KEY not set${NC}"
    echo "Run: export OPENAI_API_KEY='your-openai-key'"
    exit 1
fi

if [ -z "$CHROMA_API_KEY" ]; then
    echo -e "${RED}❌ CHROMA_API_KEY not set${NC}"
    echo "Run: export CHROMA_API_KEY='your-chroma-key'"
    exit 1
fi

echo -e "${GREEN}✅ Environment variables verified${NC}"

# Create deployment package
echo -e "${YELLOW}[3/3] Creating deployment package...${NC}"

# Create a deployment directory
mkdir -p runpod_deploy
cp runpod_handler.py runpod_deploy/
cp runpod_requirements.txt runpod_deploy/requirements.txt
cp -r services runpod_deploy/ 2>/dev/null || true

cd runpod_deploy

echo -e "${GREEN}✅ Deployment package created${NC}"
echo ""
echo "================================================================"
echo "📋 DEPLOYMENT INSTRUCTIONS"
echo "================================================================"
echo ""
echo "Option A: Deploy via RunPod Web Console (RECOMMENDED)"
echo "------------------------------------------------------"
echo ""
echo "1. Go to: https://runpod.io/console/serverless"
echo ""
echo "2. Click '+ New Endpoint'"
echo ""
echo "3. Select Template: 'RunPod Pytorch 2.1'"
echo ""
echo "4. Configure:"
echo "   - Name: northeastern-chatbot"
echo "   - GPU: RTX 4090 (24GB) - \$0.00039/sec"
echo "   - Workers: Min=0, Max=10, Idle=30s"
echo "   - Container Disk: 20GB"
echo ""
echo "5. Add Environment Variables:"
echo "   OPENAI_API_KEY=$OPENAI_API_KEY"
echo "   CHROMA_API_KEY=$CHROMA_API_KEY"
echo "   CHROMA_HOST=api.trychroma.com"
echo "   CHROMA_PORT=8000"
echo ""
echo "6. In 'Advanced' section:"
echo "   - Upload these files:"
echo "     • runpod_handler.py"
echo "     • requirements.txt"
echo "     • services/ folder"
echo ""
echo "7. Click 'Deploy'"
echo ""
echo "8. Copy your endpoint URL (looks like):"
echo "   https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync"
echo ""
echo "================================================================"
echo ""
echo "Option B: Deploy via Python Script"
echo "-----------------------------------"
echo ""
echo "Create and run this Python script:"
echo ""
cat > deploy.py << 'PYTHON_SCRIPT'
import runpod
import os

# Set your RunPod API key
runpod.api_key = os.environ.get('RUNPOD_API_KEY')

# Create serverless endpoint
endpoint = runpod.Endpoint.create(
    name="northeastern-chatbot",
    template_id="runpod-pytorch-21",  # PyTorch 2.1 template
    gpu_type_id="AMPERE_16",  # RTX 4090
    handler="runpod_handler.handler",
    env={
        "OPENAI_API_KEY": os.environ.get('OPENAI_API_KEY'),
        "CHROMA_API_KEY": os.environ.get('CHROMA_API_KEY'),
        "CHROMA_HOST": "api.trychroma.com",
        "CHROMA_PORT": "8000"
    },
    worker_min=0,
    worker_max=10,
    idle_timeout=30,
    container_disk_in_gb=20
)

print(f"✅ Endpoint created!")
print(f"🔗 Endpoint ID: {endpoint.id}")
print(f"🌐 Endpoint URL: https://api.runpod.ai/v2/{endpoint.id}/runsync")
PYTHON_SCRIPT

echo "python deploy.py"
echo ""
echo "================================================================"
echo ""
echo -e "${GREEN}📦 Files ready in: runpod_deploy/${NC}"
echo ""
echo "Next steps:"
echo "1. Choose deployment option above"
echo "2. Get your endpoint URL"
echo "3. Update frontend/config.js"
echo "4. Test your chatbot!"
echo ""

