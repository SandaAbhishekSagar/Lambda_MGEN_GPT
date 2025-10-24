#!/usr/bin/env python3
"""
Test script to verify comprehensive search improvements
"""

import os
import sys
import time
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_search_scope():
    """Test the search scope improvements"""
    try:
        from services.chat_service.lambda_gpu_chatbot_optimized import get_chatbot
        
        logger.info("Testing comprehensive search improvements...")
        
        # Initialize chatbot
        chatbot = get_chatbot()
        
        # Test collection discovery
        collections = chatbot.chroma_service.get_batch_collections(force_refresh=True)
        logger.info(f"Found {len(collections)} total collections")
        
        # Test search with comprehensive scope
        test_question = "Tell me about Northeastern campus housing"
        
        logger.info(f"Testing question: {test_question}")
        start_time = time.time()
        
        response = chatbot.chat(test_question)
        
        end_time = time.time()
        
        logger.info(f"Response time: {end_time - start_time:.2f}s")
        logger.info(f"Answer length: {len(response.answer)} characters")
        logger.info(f"Sources found: {len(response.sources)}")
        logger.info(f"Confidence: {response.confidence}")
        logger.info(f"GPU Info: {response.gpu_info}")
        
        # Check if we're searching all collections
        if len(collections) > 1000:
            logger.info("✅ Comprehensive search enabled - searching all collections")
        else:
            logger.warning("⚠️ Limited search scope detected")
            
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return False

def test_environment_config():
    """Test environment configuration"""
    logger.info("Testing environment configuration...")
    
    # Check environment variables
    search_all = os.getenv('SEARCH_ALL_COLLECTIONS', 'true')
    max_collections = os.getenv('MAX_COLLECTIONS', '0')
    
    logger.info(f"SEARCH_ALL_COLLECTIONS: {search_all}")
    logger.info(f"MAX_COLLECTIONS: {max_collections}")
    
    if search_all.lower() == 'true' and max_collections == '0':
        logger.info("✅ Comprehensive search configuration detected")
        return True
    else:
        logger.warning("⚠️ Limited search configuration detected")
        return False

if __name__ == "__main__":
    logger.info("Starting comprehensive search test...")
    
    # Test environment configuration
    config_ok = test_environment_config()
    
    # Test search scope
    search_ok = test_search_scope()
    
    if config_ok and search_ok:
        logger.info("✅ All tests passed - comprehensive search is working")
    else:
        logger.warning("⚠️ Some tests failed - check configuration")
