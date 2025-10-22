#!/usr/bin/env python3
"""
Lambda Labs Quick Start and Test Script
Northeastern University Chatbot - GPU Optimized
Ultra-fast deployment and testing for sub-8-second response times
"""

import os
import sys
import time
import asyncio
import requests
import subprocess
from typing import Dict, Any, List, Optional
import json

def print_header():
    """Print deployment header"""
    print("🚀 LAMBDA LABS GPU QUICK START")
    print("==============================")
    print("Northeastern University Chatbot - Ultra-Fast GPU Deployment")
    print("Target: Sub-8-second response times")
    print("")

def test_system_requirements():
    """Test system requirements"""
    print("1. Testing system requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print(f"✅ Python {python_version.major}.{python_version.minor} detected")
    else:
        print(f"❌ Python {python_version.major}.{python_version.minor} detected (requires 3.8+)")
        return False
    
    # Check available memory
    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        if memory_gb >= 16:
            print(f"✅ Memory: {memory_gb:.1f}GB (sufficient)")
        else:
            print(f"⚠️ Memory: {memory_gb:.1f}GB (recommended: 16GB+)")
    except ImportError:
        print("⚠️ psutil not available - cannot check memory")
    
    # Check disk space
    try:
        disk = psutil.disk_usage('.')
        disk_gb = disk.free / (1024**3)
        if disk_gb >= 50:
            print(f"✅ Disk space: {disk_gb:.1f}GB (sufficient)")
        else:
            print(f"⚠️ Disk space: {disk_gb:.1f}GB (recommended: 50GB+)")
    except:
        print("⚠️ Cannot check disk space")
    
    return True

def test_gpu_availability():
    """Test GPU availability and performance"""
    print("\n2. Testing GPU availability...")
    
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        print(f"✅ CUDA available: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            cuda_version = torch.version.cuda
            
            print(f"✅ GPU name: {gpu_name}")
            print(f"✅ GPU memory: {gpu_memory:.1f} GB")
            print(f"✅ CUDA version: {cuda_version}")
            
            # Test GPU performance
            print("Testing GPU performance...")
            start_time = time.time()
            
            # Create test tensors
            device = torch.device('cuda')
            a = torch.randn(1000, 1000, device=device)
            b = torch.randn(1000, 1000, device=device)
            
            # Perform matrix multiplication
            c = torch.matmul(a, b)
            torch.cuda.synchronize()
            
            gpu_time = time.time() - start_time
            print(f"✅ GPU matrix multiplication: {gpu_time:.3f}s")
            
            # Test memory allocation
            allocated = torch.cuda.memory_allocated(0) / 1024**3
            cached = torch.cuda.memory_reserved(0) / 1024**3
            print(f"✅ GPU memory allocated: {allocated:.2f}GB")
            print(f"✅ GPU memory cached: {cached:.2f}GB")
            
            return True
        else:
            print("⚠️ No GPU available - running on CPU")
            return False
            
    except Exception as e:
        print(f"❌ GPU test failed: {e}")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\n3. Testing dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'openai',
        'langchain',
        'chromadb',
        'sentence_transformers',
        'transformers',
        'numpy',
        'torch'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements_lambda.txt")
        return False
    
    return True

def test_chatbot_import():
    """Test chatbot import and initialization"""
    print("\n4. Testing chatbot import...")
    
    try:
        # Add project root to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from services.chat_service.lambda_gpu_chatbot import get_chatbot
        print("✅ Chatbot import successful")
        return True
    except Exception as e:
        print(f"❌ Chatbot import failed: {e}")
        return False

def test_chatbot_initialization():
    """Test chatbot initialization"""
    print("\n5. Testing chatbot initialization...")
    
    try:
        from services.chat_service.lambda_gpu_chatbot import get_chatbot
        
        # Check environment variables
        required_env = ['OPENAI_API_KEY']
        missing_env = [var for var in required_env if not os.getenv(var)]
        
        if missing_env:
            print(f"⚠️ Missing environment variables: {', '.join(missing_env)}")
            print("Please set these in your .env file")
            return False
        
        # Initialize chatbot
        chatbot = get_chatbot()
        print("✅ Chatbot initialization successful")
        
        # Test GPU info
        gpu_info = chatbot.get_gpu_info()
        print(f"✅ GPU info: {gpu_info}")
        
        return True
        
    except Exception as e:
        print(f"❌ Chatbot initialization failed: {e}")
        return False

def test_api_server():
    """Test API server functionality"""
    print("\n6. Testing API server...")
    
    try:
        # Check if server is running
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"❌ API server returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️ API server not running - start with: python services/chat_service/lambda_gpu_api.py")
        return False
    except Exception as e:
        print(f"❌ API server test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n7. Testing API endpoints...")
    
    base_url = "http://localhost:8000"
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/gpu-info", "GPU information"),
        ("/documents", "Document statistics")
    ]
    
    success_count = 0
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {description}")
                success_count += 1
            else:
                print(f"❌ {description} - status {response.status_code}")
        except Exception as e:
            print(f"❌ {description} - error: {e}")
    
    return success_count == len(endpoints)

def test_chat_functionality():
    """Test chat functionality with performance measurement"""
    print("\n8. Testing chat functionality...")
    
    try:
        base_url = "http://localhost:8000"
        
        test_questions = [
            "What programs does Northeastern University offer?",
            "Tell me about the co-op program at Northeastern",
            "What are the admission requirements for Northeastern?"
        ]
        
        total_time = 0
        successful_tests = 0
        
        for i, question in enumerate(test_questions, 1):
            print(f"Testing question {i}: {question[:50]}...")
            
            start_time = time.time()
            response = requests.post(
                f"{base_url}/chat",
                json={"question": question},
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                answer_length = len(data.get('answer', ''))
                sources_count = len(data.get('sources', []))
                timing = data.get('timing', {})
                
                print(f"✅ Response time: {response_time:.2f}s")
                print(f"   Answer length: {answer_length} characters")
                print(f"   Sources: {sources_count}")
                print(f"   Internal timing: {timing}")
                
                total_time += response_time
                successful_tests += 1
                
                # Check if response time meets sub-8-second target
                if response_time < 8:
                    print(f"✅ Meets sub-8-second target!")
                else:
                    print(f"⚠️ Response time exceeds 8 seconds")
            else:
                print(f"❌ Chat test failed: {response.status_code}")
        
        if successful_tests > 0:
            avg_time = total_time / successful_tests
            print(f"\n📊 Average response time: {avg_time:.2f}s")
            
            if avg_time < 8:
                print("🎉 SUCCESS: Sub-8-second response time achieved!")
            else:
                print("⚠️ WARNING: Response time exceeds 8 seconds")
        
        return successful_tests > 0
        
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False

def test_performance_benchmarks():
    """Test performance benchmarks"""
    print("\n9. Running performance benchmarks...")
    
    try:
        base_url = "http://localhost:8000"
        
        # Test multiple concurrent requests
        import concurrent.futures
        
        def make_request(question):
            start_time = time.time()
            try:
                response = requests.post(
                    f"{base_url}/chat",
                    json={"question": question},
                    timeout=30
                )
                response_time = time.time() - start_time
                return response_time, response.status_code == 200
            except Exception as e:
                return time.time() - start_time, False
        
        # Test concurrent requests
        test_questions = [
            "What is Northeastern University?",
            "Tell me about co-op programs",
            "What are the admission requirements?",
            "How much does tuition cost?",
            "What majors are available?"
        ]
        
        print("Testing concurrent requests...")
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request, q) for q in test_questions]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        total_time = time.time() - start_time
        successful_requests = sum(1 for _, success in results if success)
        response_times = [time for time, _ in results if time > 0]
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            print(f"✅ Concurrent requests: {successful_requests}/{len(test_questions)}")
            print(f"✅ Total time: {total_time:.2f}s")
            print(f"✅ Average response time: {avg_response_time:.2f}s")
            print(f"✅ Min response time: {min_response_time:.2f}s")
            print(f"✅ Max response time: {max_response_time:.2f}s")
            
            if max_response_time < 8:
                print("🎉 SUCCESS: All responses under 8 seconds!")
            else:
                print("⚠️ WARNING: Some responses exceed 8 seconds")
        
        return successful_requests > 0
        
    except Exception as e:
        print(f"❌ Performance benchmark failed: {e}")
        return False

def generate_report(results):
    """Generate test report"""
    print("\n" + "="*60)
    print("📊 TEST REPORT")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
    print("")
    
    print("Test Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    print("")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("Your Lambda Labs GPU deployment is ready for production!")
        print("")
        print("Next steps:")
        print("1. Start the API server: python services/chat_service/lambda_gpu_api.py")
        print("2. Monitor performance: ./monitor_gpu.sh")
        print("3. Test with real users")
    else:
        print("⚠️ SOME TESTS FAILED")
        print("Please check the errors above and fix them before deployment")
        print("")
        print("Common fixes:")
        print("1. Install missing dependencies: pip install -r requirements_lambda.txt")
        print("2. Set environment variables in .env file")
        print("3. Start the API server: python services/chat_service/lambda_gpu_api.py")

def main():
    """Main test function"""
    print_header()
    
    # Run all tests
    results = {}
    
    results["System Requirements"] = test_system_requirements()
    results["GPU Availability"] = test_gpu_availability()
    results["Dependencies"] = test_dependencies()
    results["Chatbot Import"] = test_chatbot_import()
    results["Chatbot Initialization"] = test_chatbot_initialization()
    results["API Server"] = test_api_server()
    results["API Endpoints"] = test_api_endpoints()
    results["Chat Functionality"] = test_chat_functionality()
    results["Performance Benchmarks"] = test_performance_benchmarks()
    
    # Generate report
    generate_report(results)
    
    # Return exit code
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    if passed_tests == total_tests:
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())