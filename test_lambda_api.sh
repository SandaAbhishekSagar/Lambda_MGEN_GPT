#!/bin/bash
# Quick test script for Lambda Labs API

LAMBDA_IP="167.234.215.206"
API_URL="http://${LAMBDA_IP}:8000"

echo "🧪 Testing Lambda Labs GPU API"
echo "================================"
echo ""

# Test 1: Health Check
echo "Test 1: Health Check"
echo "--------------------"
curl -s "${API_URL}/health" | python -m json.tool 2>/dev/null || curl -s "${API_URL}/health"
echo ""
echo ""

# Test 2: GPU Info
echo "Test 2: GPU Information"
echo "-----------------------"
curl -s "${API_URL}/gpu-info" | python -m json.tool 2>/dev/null || curl -s "${API_URL}/gpu-info"
echo ""
echo ""

# Test 3: Documents Count
echo "Test 3: Documents Count"
echo "-----------------------"
curl -s "${API_URL}/documents" | python -m json.tool 2>/dev/null || curl -s "${API_URL}/documents"
echo ""
echo ""

# Test 4: Chat (Quick Test)
echo "Test 4: Chat Endpoint"
echo "---------------------"
curl -s -X POST "${API_URL}/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Northeastern University?"}' | python -m json.tool 2>/dev/null || \
curl -s -X POST "${API_URL}/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Northeastern University?"}'
echo ""
echo ""

echo "✅ Tests complete!"
echo ""
echo "Expected Results:"
echo "- Health: device should be 'cuda', not 'cpu'"
echo "- GPU Info: Should show NVIDIA A10"
echo "- Documents: Should show 80,000 documents"
echo "- Chat: Should return an answer with sources"

