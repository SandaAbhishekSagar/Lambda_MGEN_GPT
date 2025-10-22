#!/usr/bin/env python3
"""
Test ChromaDB Cloud Connection
"""

import os
import sys
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_chromadb_connection():
    """Test ChromaDB Cloud connection"""
    try:
        # Set environment variables for ChromaDB Cloud
        os.environ['USE_CLOUD_CHROMA'] = 'true'
        os.environ['CHROMADB_API_KEY'] = 'ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW'
        os.environ['CHROMADB_TENANT'] = '28757e4a-f042-4b0c-ad7c-9257cd36b130'
        os.environ['CHROMADB_DATABASE'] = 'newtest'
        
        # Import ChromaDB
        import chromadb
        from chromadb.config import Settings
        
        logger.info("Testing ChromaDB Cloud connection...")
        
        # Try Method 1: CloudClient
        try:
            from chromadb import CloudClient
            client = CloudClient(
                api_key=os.environ['CHROMADB_API_KEY'],
                tenant=os.environ['CHROMADB_TENANT'],
                database=os.environ['CHROMADB_DATABASE']
            )
            logger.info("✅ Method 1 (CloudClient) - SUCCESS")
            
            # Test getting collections
            collections = client.list_collections()
            logger.info(f"Found {len(collections)} collections")
            
            return True
            
        except Exception as e1:
            logger.warning(f"Method 1 failed: {e1}")
            
            # Try Method 2: HTTP Client
            try:
                client = chromadb.HttpClient(
                    host="api.trychroma.com",
                    port=8000,
                    settings=Settings(
                        chroma_api_impl="chromadb.api.fastapi.FastAPI",
                        chroma_server_host="api.trychroma.com",
                        chroma_server_http_port="8000",
                        chroma_server_headers={"X-Chroma-Token": os.environ['CHROMADB_API_KEY']}
                    )
                )
                logger.info("✅ Method 2 (HttpClient) - SUCCESS")
                
                # Test getting collections
                collections = client.list_collections()
                logger.info(f"Found {len(collections)} collections")
                
                return True
                
            except Exception as e2:
                logger.error(f"Method 2 failed: {e2}")
                return False
                
    except Exception as e:
        logger.error(f"ChromaDB connection test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_chromadb_connection()
    if success:
        print("✅ ChromaDB connection test PASSED")
    else:
        print("❌ ChromaDB connection test FAILED")
        print("The system will use fallback mode with estimated document counts.")
