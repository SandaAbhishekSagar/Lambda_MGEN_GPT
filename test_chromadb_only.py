"""
Simple test for ChromaDB Cloud connection only
Tests your existing ChromaDB setup without installing new dependencies
"""

import os
import sys

def test_chromadb_connection():
    """Test ChromaDB Cloud connection using existing setup"""
    print("Testing ChromaDB Cloud Connection...")
    print("=" * 50)
    
    try:
        # Set environment variables
        os.environ['CHROMA_API_KEY'] = 'ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW'
        os.environ['CHROMA_TENANT'] = '28757e4a-f042-4b0c-ad7c-9257cd36b130'
        os.environ['CHROMA_DATABASE'] = 'newtest'
        
        # Try to import from your existing setup
        from chroma_cloud_config import get_chroma_cloud_client, test_cloud_connection
        
        print("OK ChromaDB Cloud configuration found!")
        print(f"API Key: {os.environ['CHROMA_API_KEY'][:8]}...")
        print(f"Tenant: {os.environ['CHROMA_TENANT']}")
        print(f"Database: {os.environ['CHROMA_DATABASE']}")
        
        # Test connection
        if test_cloud_connection():
            print("OK ChromaDB Cloud connection successful!")
            return True
        else:
            print("FAIL ChromaDB Cloud connection failed!")
            return False
        
    except Exception as e:
        print(f"FAIL ChromaDB Cloud test failed: {str(e)}")
        return False

def test_existing_setup():
    """Test your existing chatbot setup"""
    print("\nTesting Existing Chatbot Setup...")
    print("=" * 50)
    
    try:
        # Test if we can import your existing services
        from services.chat_service.enhanced_openai_chatbot import EnhancedOpenAIUniversityRAGChatbot
        
        print("OK Enhanced OpenAI chatbot found!")
        
        # Test if we can create the chatbot
        chatbot = EnhancedOpenAIUniversityRAGChatbot()
        print("OK Chatbot instance created successfully!")
        
        return True
        
    except Exception as e:
        print(f"FAIL Existing setup test failed: {str(e)}")
        return False

def main():
    """Run tests"""
    print("ChromaDB Cloud Test - Northeastern University Chatbot")
    print("=" * 60)
    
    # Test 1: ChromaDB Cloud connection
    chromadb_ok = test_chromadb_connection()
    
    # Test 2: Existing setup
    existing_ok = test_existing_setup()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if chromadb_ok:
        print("PASS ChromaDB Cloud Connection")
    else:
        print("FAIL ChromaDB Cloud Connection")
    
    if existing_ok:
        print("PASS Existing Chatbot Setup")
    else:
        print("FAIL Existing Chatbot Setup")
    
    if chromadb_ok and existing_ok:
        print("\nAll tests passed! Your setup is ready for RunPod deployment!")
        print("\nNext steps:")
        print("1. Set your OpenAI API key:")
        print("   export OPENAI_API_KEY=sk-proj-your-openai-key-here")
        print("2. Deploy to RunPod using GitHub integration")
        print("3. Set environment variables in RunPod console")
    else:
        print("\nSome tests failed. Please check the errors above.")
    
    return chromadb_ok and existing_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
