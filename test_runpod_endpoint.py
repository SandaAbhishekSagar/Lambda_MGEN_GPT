"""
Test RunPod Endpoint
Tests the deployed Northeastern University Chatbot on RunPod
"""

import requests
import json
import time
import os
from typing import Dict, Any

# Your RunPod endpoint URL (get this after deployment)
RUNPOD_ENDPOINT_URL = os.getenv(
    'RUNPOD_ENDPOINT_URL',
    'https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync'
)

# Your RunPod API key
RUNPOD_API_KEY = os.getenv('RUNPOD_API_KEY', '')


def test_endpoint(question: str) -> Dict[str, Any]:
    """Test the RunPod endpoint with a question"""
    
    print(f"\n{'=' * 80}")
    print(f"🧪 Testing RunPod Endpoint")
    print(f"{'=' * 80}")
    print(f"\n📝 Question: {question}")
    
    # Prepare request
    headers = {
        'Content-Type': 'application/json',
    }
    
    if RUNPOD_API_KEY:
        headers['Authorization'] = f'Bearer {RUNPOD_API_KEY}'
    
    payload = {
        "input": {
            "question": question
        }
    }
    
    # Send request
    print(f"\n⏳ Sending request to RunPod...")
    start_time = time.time()
    
    try:
        response = requests.post(
            RUNPOD_ENDPOINT_URL,
            headers=headers,
            json=payload,
            timeout=120
        )
        
        elapsed_time = time.time() - start_time
        
        print(f"⏱️  Total request time: {elapsed_time:.2f}s")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n{'=' * 80}")
            print(f"✅ SUCCESS")
            print(f"{'=' * 80}")
            
            # Extract answer
            if 'output' in result:
                output = result['output']
            else:
                output = result
            
            print(f"\n💬 Answer:")
            print(f"{'-' * 80}")
            print(output.get('answer', 'No answer found'))
            print(f"{'-' * 80}")
            
            # Show sources
            if 'sources' in output and output['sources']:
                print(f"\n📚 Sources ({len(output['sources'])}):")
                for i, source in enumerate(output['sources'], 1):
                    similarity = source.get('similarity', 0)
                    source_name = source.get('source', 'Unknown')
                    print(f"  {i}. {source_name} (similarity: {similarity:.2%})")
            
            # Show confidence
            confidence = output.get('confidence', 'unknown')
            print(f"\n🎯 Confidence: {confidence.upper()}")
            
            # Show timing breakdown
            if 'timing' in output:
                timing = output['timing']
                print(f"\n⏱️  Timing Breakdown:")
                print(f"  - Search: {timing.get('search', 0)}s")
                print(f"  - Generation: {timing.get('generation', 0)}s")
                print(f"  - Total: {timing.get('total', 0)}s")
            
            # Check if meets 8-second requirement
            total_time = elapsed_time
            if total_time < 8:
                print(f"\n✅ MEETS REQUIREMENT: Response in {total_time:.2f}s (< 8s)")
            else:
                print(f"\n⚠️  WARNING: Response took {total_time:.2f}s (> 8s)")
            
            return result
        
        else:
            print(f"\n❌ ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    except requests.exceptions.Timeout:
        print(f"\n❌ ERROR: Request timed out (> 120s)")
        return None
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return None


def run_test_suite():
    """Run a suite of test questions"""
    
    print(f"\n{'=' * 80}")
    print(f"🧪 RUNPOD ENDPOINT TEST SUITE")
    print(f"{'=' * 80}")
    print(f"\nEndpoint: {RUNPOD_ENDPOINT_URL}")
    
    if 'YOUR_ENDPOINT_ID' in RUNPOD_ENDPOINT_URL:
        print(f"\n❌ ERROR: Please update RUNPOD_ENDPOINT_URL with your actual endpoint ID")
        print(f"\nSet it like this:")
        print(f"export RUNPOD_ENDPOINT_URL='https://api.runpod.ai/v2/YOUR_ACTUAL_ID/runsync'")
        return
    
    # Test questions
    test_questions = [
        "What programs does Northeastern University offer?",
        "Tell me about the co-op program at Northeastern",
        "What are the admission requirements?",
        "Where is Northeastern University located?",
        "What is the student-faculty ratio at Northeastern?"
    ]
    
    results = []
    total_time = 0
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'#' * 80}")
        print(f"TEST {i}/{len(test_questions)}")
        print(f"{'#' * 80}")
        
        result = test_endpoint(question)
        
        if result:
            results.append({
                'question': question,
                'success': True,
                'result': result
            })
            
            # Get timing
            output = result.get('output', result)
            timing = output.get('timing', {})
            total_time += timing.get('total', 0)
        else:
            results.append({
                'question': question,
                'success': False
            })
        
        # Wait between requests
        if i < len(test_questions):
            print(f"\n⏳ Waiting 2s before next test...")
            time.sleep(2)
    
    # Print summary
    print(f"\n{'=' * 80}")
    print(f"📊 TEST SUMMARY")
    print(f"{'=' * 80}")
    
    successful = sum(1 for r in results if r['success'])
    print(f"\n✅ Successful: {successful}/{len(test_questions)}")
    print(f"❌ Failed: {len(test_questions) - successful}/{len(test_questions)}")
    
    if successful > 0:
        avg_time = total_time / successful
        print(f"\n⏱️  Average response time: {avg_time:.2f}s")
        
        if avg_time < 8:
            print(f"✅ MEETS 8-SECOND REQUIREMENT")
        else:
            print(f"⚠️  EXCEEDS 8-SECOND REQUIREMENT")
    
    print(f"\n{'=' * 80}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Test with custom question
        question = ' '.join(sys.argv[1:])
        test_endpoint(question)
    else:
        # Run full test suite
        run_test_suite()

