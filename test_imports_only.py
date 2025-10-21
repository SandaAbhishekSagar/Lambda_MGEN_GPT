"""
Simple import test for GitHub Actions
Tests if all required modules can be imported
"""

import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing Module Imports...")
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

def test_environment():
    """Test environment variables"""
    print("\nTesting Environment Variables...")
    print("=" * 50)
    
    import os
    
    # Check if environment variables are set
    env_vars = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', 'Not set'),
        'CHROMA_API_KEY': os.getenv('CHROMA_API_KEY', 'Not set'),
        'CHROMA_TENANT': os.getenv('CHROMA_TENANT', 'Not set'),
        'CHROMA_DATABASE': os.getenv('CHROMA_DATABASE', 'Not set')
    }
    
    for var, value in env_vars.items():
        if value == 'Not set':
            print(f"WARNING {var}: Not set")
        else:
            # Mask sensitive values
            if 'KEY' in var:
                masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            else:
                masked_value = value
            print(f"OK {var}: {masked_value}")
    
    return True

def main():
    """Run all tests"""
    print("GitHub Actions Import Test")
    print("=" * 60)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test environment
    env_ok = test_environment()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if imports_ok:
        print("PASS Module Imports")
    else:
        print("FAIL Module Imports")
    
    if env_ok:
        print("PASS Environment Variables")
    else:
        print("FAIL Environment Variables")
    
    if imports_ok and env_ok:
        print("\nAll tests passed! Ready for deployment!")
        return True
    else:
        print("\nSome tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
