"""
Setup script for local testing
Installs dependencies and sets up environment variables
"""

import os
import sys
import subprocess

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    print("=" * 50)
    
    try:
        # Install from requirements_runpod.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_runpod.txt"])
        print("OK Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAIL Failed to install dependencies: {e}")
        return False

def set_environment_variables():
    """Set environment variables for testing"""
    print("\nSetting environment variables...")
    print("=" * 50)
    
    # Your actual ChromaDB Cloud credentials
    env_vars = {
        'CHROMA_API_KEY': 'ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW',
        'CHROMA_TENANT': '28757e4a-f042-4b0c-ad7c-9257cd36b130',
        'CHROMA_DATABASE': 'newtest',
        'CHROMA_HOST': 'localhost',
        'CHROMA_PORT': '8000'
    }
    
    for var, value in env_vars.items():
        os.environ[var] = value
        print(f"OK {var} = {value}")
    
    print("\nNOTE: You need to set OPENAI_API_KEY manually:")
    print("export OPENAI_API_KEY=sk-proj-your-openai-key-here")
    print("Or set it in your environment before running tests")
    
    return True

def test_chromadb_connection():
    """Test ChromaDB Cloud connection"""
    print("\nTesting ChromaDB Cloud Connection...")
    print("=" * 50)
    
    try:
        import chromadb
        from chromadb import CloudClient
        
        # Get environment variables
        api_key = os.getenv('CHROMA_API_KEY')
        tenant = os.getenv('CHROMA_TENANT')
        database = os.getenv('CHROMA_DATABASE')
        
        if not all([api_key, tenant, database]):
            print("FAIL ChromaDB environment variables not set")
            return False
        
        # Create ChromaDB Cloud client
        client = CloudClient(
            api_key=api_key,
            tenant=tenant,
            database=database
        )
        
        # Test connection by listing collections
        collections = client.list_collections()
        
        print(f"OK ChromaDB Cloud connection successful!")
        print(f"Database: {database}")
        print(f"Collections found: {len(collections)}")
        
        # Show collection details
        for collection in collections[:3]:  # Show first 3 collections
            try:
                count = collection.count()
                print(f"  - {collection.name} ({count} documents)")
            except:
                print(f"  - {collection.name} (count unavailable)")
        
        if len(collections) > 3:
            print(f"  ... and {len(collections) - 3} more collections")
        
        return True
        
    except Exception as e:
        print(f"FAIL ChromaDB Cloud connection failed: {str(e)}")
        return False

def main():
    """Run setup and test"""
    print("Local Setup for RunPod Deployment")
    print("=" * 60)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("FAIL Setup failed at dependency installation")
        return False
    
    # Step 2: Set environment variables
    if not set_environment_variables():
        print("FAIL Setup failed at environment variables")
        return False
    
    # Step 3: Test ChromaDB connection
    if not test_chromadb_connection():
        print("FAIL Setup failed at ChromaDB connection")
        return False
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)
    print("OK Dependencies installed")
    print("OK Environment variables set")
    print("OK ChromaDB Cloud connection working")
    print("\nNext steps:")
    print("1. Set your OpenAI API key:")
    print("   export OPENAI_API_KEY=sk-proj-your-openai-key-here")
    print("2. Run the test:")
    print("   python test_setup_simple.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
