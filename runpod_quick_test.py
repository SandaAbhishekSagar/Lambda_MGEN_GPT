"""
Quick test script for RunPod deployment
Tests the optimized handler locally before deployment
"""

import json
import sys
import os
from runpod_optimized_handler import handler

def test_handler():
    """Test the RunPod handler with sample input"""
    
    print("🧪 Testing RunPod Handler Locally")
    print("=" * 50)
    
    # Test input
    test_input = {
        "input": {
            "question": "What undergraduate programs does Northeastern University offer?"
        }
    }
    
    print(f"📝 Test Question: {test_input['input']['question']}")
    print("\n🔄 Processing...")
    
    try:
        # Test the handler
        result = handler(test_input)
        
        print("\n✅ Test Results:")
        print("=" * 30)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return False
        
        print(f"📄 Answer: {result.get('answer', 'No answer')[:200]}...")
        print(f"🎯 Confidence: {result.get('confidence', 'Unknown')}")
        print(f"📊 Sources: {len(result.get('sources', []))}")
        print(f"⏱️  Timing: {result.get('timing', {})}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Check environment variables
    required_env_vars = ['OPENAI_API_KEY', 'CHROMA_API_KEY', 'CHROMA_HOST']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these variables before running the test.")
        sys.exit(1)
    
    # Run test
    success = test_handler()
    
    if success:
        print("\n🎉 Test completed successfully!")
        print("Ready for RunPod deployment!")
    else:
        print("\n❌ Test failed!")
        print("Please check your configuration and try again.")
        sys.exit(1)
