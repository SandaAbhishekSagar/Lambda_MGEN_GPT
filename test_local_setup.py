"""
Local Test Setup for RunPod Deployment
Tests ChromaDB Cloud connection, OpenAI API, and handler functionality
"""

import os
import sys
import time
from typing import Dict, Any

def test_environment_variables():
    """Test if all required environment variables are set"""
    print("🔍 Testing Environment Variables...")
    print("=" * 50)
    
    # Required variables
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API Key',
        'CHROMA_API_KEY': 'ChromaDB API Key',
        'CHROMA_TENANT': 'ChromaDB Tenant',
        'CHROMA_DATABASE': 'ChromaDB Database'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'KEY' in var:
                masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            else:
                masked_value = value
            print(f"✅ {description}: {masked_value}")
        else:
            print(f"❌ {description}: Not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ Missing required variables: {', '.join(missing_vars)}")
        return False
    else:
        print("\n✅ All required environment variables are set!")
        return True

def test_chromadb_connection():
    """Test ChromaDB Cloud connection"""
    print("\n🔍 Testing ChromaDB Cloud Connection...")
    print("=" * 50)
    
    try:
        import chromadb
        from chromadb import CloudClient
        
        # Get environment variables
        api_key = os.getenv('CHROMA_API_KEY')
        tenant = os.getenv('CHROMA_TENANT')
        database = os.getenv('CHROMA_DATABASE')
        
        if not all([api_key, tenant, database]):
            print("❌ ChromaDB environment variables not set")
            return False
        
        # Create ChromaDB Cloud client
        client = CloudClient(
            api_key=api_key,
            tenant=tenant,
            database=database
        )
        
        # Test connection by listing collections
        collections = client.list_collections()
        
        print(f"✅ ChromaDB Cloud connection successful!")
        print(f"📊 Database: {database}")
        print(f"📋 Collections found: {len(collections)}")
        
        # Show collection details
        for collection in collections[:5]:  # Show first 5 collections
            try:
                count = collection.count()
                print(f"  - {collection.name} ({count} documents)")
            except:
                print(f"  - {collection.name} (count unavailable)")
        
        if len(collections) > 5:
            print(f"  ... and {len(collections) - 5} more collections")
        
        return True
        
    except Exception as e:
        print(f"❌ ChromaDB Cloud connection failed: {str(e)}")
        return False

def test_openai_connection():
    """Test OpenAI API connection"""
    print("\n🔍 Testing OpenAI API Connection...")
    print("=" * 50)
    
    try:
        from langchain_openai import ChatOpenAI
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ OpenAI API key not set")
            return False
        
        # Create OpenAI client
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            max_tokens=100,
            openai_api_key=api_key,
            request_timeout=10
        )
        
        # Test with a simple query
        response = llm.invoke("Hello, this is a test. Please respond with 'Test successful'.")
        
        print("✅ OpenAI API connection successful!")
        print(f"📝 Response: {response.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API connection failed: {str(e)}")
        return False

def test_embeddings():
    """Test OpenAI embeddings"""
    print("\n🔍 Testing OpenAI Embeddings...")
    print("=" * 50)
    
    try:
        from langchain_openai import OpenAIEmbeddings
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ OpenAI API key not set")
            return False
        
        # Create embeddings client
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=api_key,
            request_timeout=10
        )
        
        # Test embedding generation
        test_text = "What undergraduate programs does Northeastern offer?"
        embedding = embeddings.embed_query(test_text)
        
        print("✅ OpenAI Embeddings successful!")
        print(f"📊 Embedding dimension: {len(embedding)}")
        print(f"📝 Test text: {test_text}")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI Embeddings failed: {str(e)}")
        return False

def test_handler():
    """Test the RunPod handler"""
    print("\n🔍 Testing RunPod Handler...")
    print("=" * 50)
    
    try:
        # Import the handler
        from runpod_handler import handler
        
        # Test input
        test_input = {
            "input": {
                "question": "What undergraduate programs does Northeastern offer?"
            }
        }
        
        print("📝 Test question: What undergraduate programs does Northeastern offer?")
        print("🔄 Processing...")
        
        # Test the handler
        result = handler(test_input)
        
        if 'error' in result:
            print(f"❌ Handler test failed: {result['error']}")
            return False
        
        print("✅ Handler test successful!")
        print(f"📄 Answer length: {len(result.get('answer', ''))}")
        print(f"🎯 Confidence: {result.get('confidence', 'Unknown')}")
        print(f"📊 Sources: {len(result.get('sources', []))}")
        print(f"⏱️  Timing: {result.get('timing', {})}")
        
        return True
        
    except Exception as e:
        print(f"❌ Handler test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 Local Setup Test - Northeastern University Chatbot")
    print("=" * 60)
    
    # Test results
    tests = []
    
    # Test 1: Environment Variables
    tests.append(("Environment Variables", test_environment_variables()))
    
    # Test 2: ChromaDB Connection
    tests.append(("ChromaDB Cloud Connection", test_chromadb_connection()))
    
    # Test 3: OpenAI API
    tests.append(("OpenAI API Connection", test_openai_connection()))
    
    # Test 4: OpenAI Embeddings
    tests.append(("OpenAI Embeddings", test_embeddings()))
    
    # Test 5: Handler
    tests.append(("RunPod Handler", test_handler()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for RunPod deployment!")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
