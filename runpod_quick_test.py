"""
Quick test script for RunPod deployment
Tests the optimized handler locally before deployment
"""

import json
import sys
import os

def test_handler():
    """Test the RunPod handler with sample input"""
    
    print("Testing RunPod Handler Locally")
    print("=" * 50)
    
    # Test input
    test_input = {
        "input": {
            "question": "What undergraduate programs does Northeastern offer?"
        }
    }
    
    print(f"Test Question: {test_input['input']['question']}")
    print("\nProcessing...")
    
    try:
        # Test the handler
        from runpod_handler import handler
        result = handler(test_input)
        
        print("\nTest Results:")
        print("=" * 30)
        
        if 'error' in result:
            print(f"Error: {result['error']}")
            return False
        
        print(f"Answer: {result.get('answer', 'No answer')[:200]}...")
        print(f"Confidence: {result.get('confidence', 'Unknown')}")
        print(f"Sources: {len(result.get('sources', []))}")
        print(f"Timing: {result.get('timing', {})}")
        
        return True
        
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Check environment variables
    required_env_vars = ['OPENAI_API_KEY', 'CHROMA_API_KEY', 'CHROMA_TENANT', 'CHROMA_DATABASE']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these variables before running the test.")
        print("\nFor testing, you can set:")
        print("export OPENAI_API_KEY=test-key")
        print("export CHROMA_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW")
        print("export CHROMA_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130")
        print("export CHROMA_DATABASE=newtest")
        sys.exit(1)
    
    # Run test
    success = test_handler()
    
    if success:
        print("\nTest completed successfully!")
        print("Ready for RunPod deployment!")
    else:
        print("\nTest failed!")
        print("Please check your configuration and try again.")
        sys.exit(1)