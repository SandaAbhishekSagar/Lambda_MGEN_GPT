"""
GitHub Actions Test Script
Tests the setup for RunPod deployment
"""

import sys
import os

def test_environment():
    """Test environment variables"""
    print("Testing Environment Variables...")
    print("=" * 50)
    
    # Check if environment variables are set
    env_vars = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', 'Not set'),
        'CHROMA_API_KEY': os.getenv('CHROMA_API_KEY', 'Not set'),
        'CHROMA_TENANT': os.getenv('CHROMA_TENANT', 'Not set'),
        'CHROMA_DATABASE': os.getenv('CHROMA_DATABASE', 'Not set')
    }
    
    all_set = True
    for var, value in env_vars.items():
        if value == 'Not set':
            print(f"WARNING {var}: Not set")
            all_set = False
        else:
            # Mask sensitive values
            if 'KEY' in var:
                masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            else:
                masked_value = value
            print(f"OK {var}: {masked_value}")
    
    return all_set

def test_imports():
    """Test if all required modules can be imported"""
    print("\nTesting Module Imports...")
    print("=" * 50)
    
    modules_to_test = [
        ('runpod', 'RunPod SDK'),
        ('chromadb', 'ChromaDB'),
        ('torch', 'PyTorch'),
        ('langchain_openai', 'LangChain OpenAI'),
        ('langchain', 'LangChain'),
        ('numpy', 'NumPy'),
        ('requests', 'Requests'),
        ('pydantic', 'Pydantic')
    ]
    
    failed_imports = []
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"OK {description}")
        except ImportError as e:
            print(f"FAIL {description}: {e}")
            failed_imports.append(module_name)
    
    if failed_imports:
        print(f"\nFailed imports: {', '.join(failed_imports)}")
        return False
    else:
        print("\nAll imports successful!")
        return True

def test_chromadb_config():
    """Test ChromaDB configuration"""
    print("\nTesting ChromaDB Configuration...")
    print("=" * 50)
    
    try:
        from chroma_cloud_config import get_chroma_cloud_client
        
        print("OK ChromaDB Cloud configuration found!")
        
        # Test if we can create a client (without actually connecting)
        api_key = os.getenv('CHROMA_API_KEY')
        tenant = os.getenv('CHROMA_TENANT')
        database = os.getenv('CHROMA_DATABASE')
        
        if all([api_key, tenant, database]):
            print("OK ChromaDB credentials are set")
            return True
        else:
            print("FAIL ChromaDB credentials not complete")
            return False
            
    except Exception as e:
        print(f"FAIL ChromaDB configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("GitHub Actions Test - RunPod Deployment")
    print("=" * 60)
    
    # Test environment variables
    env_ok = test_environment()
    
    # Test imports
    imports_ok = test_imports()
    
    # Test ChromaDB configuration
    chromadb_ok = test_chromadb_config()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if env_ok:
        print("PASS Environment Variables")
    else:
        print("FAIL Environment Variables")
    
    if imports_ok:
        print("PASS Module Imports")
    else:
        print("FAIL Module Imports")
    
    if chromadb_ok:
        print("PASS ChromaDB Configuration")
    else:
        print("FAIL ChromaDB Configuration")
    
    all_passed = env_ok and imports_ok and chromadb_ok
    
    if all_passed:
        print("\nAll tests passed! Ready for RunPod deployment!")
        print("\nNext steps:")
        print("1. Push to GitHub")
        print("2. Deploy via RunPod console")
        print("3. Set OpenAI API key in RunPod")
        print("4. Test the deployment")
    else:
        print("\nSome tests failed. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
