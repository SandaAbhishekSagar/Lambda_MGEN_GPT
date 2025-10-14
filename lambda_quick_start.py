#!/usr/bin/env python3
"""
Lambda Labs Quick Start Script
Automated setup and testing for Northeastern University Chatbot on Lambda GPU
"""

import os
import sys
import time
import subprocess
import requests
import torch
from pathlib import Path


class LambdaQuickStart:
    """Quick start automation for Lambda Labs deployment"""
    
    def __init__(self):
        self.base_dir = Path.cwd()
        self.venv_dir = self.base_dir / "lambda_gpu_env"
        self.api_url = "http://localhost:8000"
        
    def print_status(self, message, status="INFO"):
        """Print colored status message"""
        colors = {
            "INFO": "\033[94m",
            "SUCCESS": "\033[92m", 
            "WARNING": "\033[93m",
            "ERROR": "\033[91m"
        }
        reset = "\033[0m"
        color = colors.get(status, colors["INFO"])
        print(f"{color}[{status}]{reset} {message}")
    
    def check_gpu(self):
        """Check GPU availability and information"""
        self.print_status("Checking GPU availability...")
        
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            cuda_version = torch.version.cuda
            
            self.print_status(f"✅ GPU Available: {gpu_name}", "SUCCESS")
            self.print_status(f"✅ GPU Memory: {gpu_memory:.1f} GB", "SUCCESS")
            self.print_status(f"✅ CUDA Version: {cuda_version}", "SUCCESS")
            
            return True
        else:
            self.print_status("⚠️ GPU not available - will use CPU", "WARNING")
            return False
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        self.print_status("Checking dependencies...")
        
        required_packages = [
            "fastapi", "uvicorn", "torch", "transformers", 
            "sentence-transformers", "chromadb", "openai"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
                self.print_status(f"✅ {package}", "SUCCESS")
            except ImportError:
                missing_packages.append(package)
                self.print_status(f"❌ {package}", "ERROR")
        
        if missing_packages:
            self.print_status(f"Missing packages: {', '.join(missing_packages)}", "ERROR")
            return False
        
        return True
    
    def check_environment(self):
        """Check environment configuration"""
        self.print_status("Checking environment configuration...")
        
        # Check for .env file
        env_file = self.base_dir / ".env"
        if not env_file.exists():
            self.print_status("❌ .env file not found", "ERROR")
            self.create_env_template()
            return False
        
        # Check for required environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ["OPENAI_API_KEY"]
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            self.print_status(f"Missing environment variables: {', '.join(missing_vars)}", "ERROR")
            return False
        
        self.print_status("✅ Environment configuration valid", "SUCCESS")
        return True
    
    def create_env_template(self):
        """Create .env template file"""
        env_template = """# Lambda Labs GPU Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# ChromaDB Configuration (using cloud)
CHROMADB_HOST=your_chromadb_host_here
CHROMADB_PORT=8000

# GPU Configuration
CUDA_VISIBLE_DEVICES=0
TORCH_CUDA_ARCH_LIST="7.5;8.0;8.6"

# Performance Optimization
OMP_NUM_THREADS=4
TOKENIZERS_PARALLELISM=false
"""
        
        env_file = self.base_dir / ".env"
        with open(env_file, "w") as f:
            f.write(env_template)
        
        self.print_status("Created .env template file - please update with your API keys", "WARNING")
    
    def start_application(self):
        """Start the Lambda GPU application"""
        self.print_status("Starting Lambda GPU application...")
        
        # Check if application is already running
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                self.print_status("✅ Application is already running", "SUCCESS")
                return True
        except:
            pass
        
        # Start application in background
        try:
            if self.venv_dir.exists():
                python_path = self.venv_dir / "bin" / "python"
            else:
                python_path = "python3"
            
            cmd = [
                str(python_path),
                "services/chat_service/lambda_gpu_api.py"
            ]
            
            # Start process in background
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.base_dir
            )
            
            # Wait for application to start
            self.print_status("Waiting for application to start...")
            for i in range(30):  # Wait up to 30 seconds
                try:
                    response = requests.get(f"{self.api_url}/health", timeout=2)
                    if response.status_code == 200:
                        self.print_status("✅ Application started successfully", "SUCCESS")
                        return True
                except:
                    time.sleep(1)
            
            self.print_status("❌ Application failed to start", "ERROR")
            return False
            
        except Exception as e:
            self.print_status(f"❌ Error starting application: {e}", "ERROR")
            return False
    
    def test_api(self):
        """Test API endpoints"""
        self.print_status("Testing API endpoints...")
        
        endpoints = [
            ("/health", "Health Check"),
            ("/gpu-info", "GPU Information"),
            ("/documents", "Document Statistics"),
        ]
        
        for endpoint, description in endpoints:
            try:
                response = requests.get(f"{self.api_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    self.print_status(f"✅ {description}", "SUCCESS")
                else:
                    self.print_status(f"❌ {description} - Status: {response.status_code}", "ERROR")
            except Exception as e:
                self.print_status(f"❌ {description} - Error: {e}", "ERROR")
    
    def test_chat(self):
        """Test chat functionality"""
        self.print_status("Testing chat functionality...")
        
        test_questions = [
            "What programs does Northeastern University offer?",
            "How does the co-op program work?",
            "What are the admission requirements?"
        ]
        
        for question in test_questions:
            try:
                payload = {"question": question}
                response = requests.post(
                    f"{self.api_url}/chat",
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "")
                    confidence = data.get("confidence", 0)
                    documents = data.get("documents_analyzed", 0)
                    
                    self.print_status(f"✅ Question: {question[:50]}...", "SUCCESS")
                    self.print_status(f"   Answer length: {len(answer)} chars", "INFO")
                    self.print_status(f"   Confidence: {confidence:.2f}", "INFO")
                    self.print_status(f"   Documents: {documents}", "INFO")
                else:
                    self.print_status(f"❌ Chat test failed - Status: {response.status_code}", "ERROR")
                    
            except Exception as e:
                self.print_status(f"❌ Chat test error: {e}", "ERROR")
    
    def run_performance_test(self):
        """Run performance benchmarks"""
        self.print_status("Running performance benchmarks...")
        
        try:
            # Test response time
            start_time = time.time()
            payload = {"question": "Tell me about Northeastern University programs"}
            response = requests.post(f"{self.api_url}/chat", json=payload, timeout=60)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.print_status(f"✅ Response time: {response_time:.2f}s", "SUCCESS")
                self.print_status(f"✅ Search time: {data.get('search_time', 0):.2f}s", "SUCCESS")
                self.print_status(f"✅ LLM time: {data.get('llm_time', 0):.2f}s", "SUCCESS")
                self.print_status(f"✅ Documents analyzed: {data.get('documents_analyzed', 0)}", "SUCCESS")
            else:
                self.print_status("❌ Performance test failed", "ERROR")
                
        except Exception as e:
            self.print_status(f"❌ Performance test error: {e}", "ERROR")
    
    def print_summary(self):
        """Print deployment summary"""
        self.print_status("=" * 60)
        self.print_status("🚀 Lambda Labs GPU Deployment Summary", "SUCCESS")
        self.print_status("=" * 60)
        
        # GPU Information
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            self.print_status(f"🖥️  GPU: {gpu_name} ({gpu_memory:.1f} GB)", "INFO")
        else:
            self.print_status("🖥️  GPU: Not available (CPU mode)", "WARNING")
        
        # API Information
        self.print_status(f"🌐 API URL: {self.api_url}", "INFO")
        self.print_status("📊 Health Check: /health", "INFO")
        self.print_status("🔍 GPU Info: /gpu-info", "INFO")
        self.print_status("💬 Chat API: /chat", "INFO")
        
        # Next Steps
        self.print_status("", "INFO")
        self.print_status("📋 Next Steps:", "INFO")
        self.print_status("1. Update .env file with your API keys", "INFO")
        self.print_status("2. Test the chat functionality", "INFO")
        self.print_status("3. Monitor GPU usage with: ./monitor_gpu.sh", "INFO")
        self.print_status("4. Scale as needed for production", "INFO")
        
        self.print_status("", "INFO")
        self.print_status("🎉 Deployment completed successfully!", "SUCCESS")
    
    def run(self):
        """Run the complete quick start process"""
        self.print_status("🚀 Lambda Labs GPU Quick Start", "SUCCESS")
        self.print_status("=" * 50)
        
        # Check GPU
        gpu_available = self.check_gpu()
        
        # Check dependencies
        if not self.check_dependencies():
            self.print_status("❌ Missing dependencies - please install them first", "ERROR")
            return False
        
        # Check environment
        if not self.check_environment():
            self.print_status("❌ Environment not configured - please update .env file", "ERROR")
            return False
        
        # Start application
        if not self.start_application():
            self.print_status("❌ Failed to start application", "ERROR")
            return False
        
        # Test API
        self.test_api()
        
        # Test chat functionality
        self.test_chat()
        
        # Run performance test
        self.run_performance_test()
        
        # Print summary
        self.print_summary()
        
        return True


if __name__ == "__main__":
    quick_start = LambdaQuickStart()
    success = quick_start.run()
    
    if success:
        print("\n🎉 Quick start completed successfully!")
        print("Your Northeastern University Chatbot is ready on Lambda Labs GPU! 🚀")
    else:
        print("\n❌ Quick start failed. Please check the errors above.")
        sys.exit(1)
