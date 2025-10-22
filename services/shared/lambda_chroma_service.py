"""
Lambda Labs GPU-Optimized ChromaDB Service
Ultra-fast vector database operations for sub-8-second response times
"""

import os
import time
import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import chromadb
from chromadb.config import Settings
from chromadb.api.models.Collection import Collection
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LambdaGPUChromaService:
    """Ultra-optimized ChromaDB service for Lambda Labs GPU deployment"""
    
    def __init__(self):
        self.client = None
        self.collections_cache = []
        self.collections_metadata = {}
        self.last_cache_update = 0
        self.cache_ttl = 300  # 5 minutes
        self.connection_retries = 3
        self.connection_timeout = 10
        
        # Performance optimization settings
        self.max_collections_per_search = 150  # Increased for better coverage
        self.parallel_workers = 8  # Optimized for Lambda Labs
        self.search_timeout = 5  # 5 seconds per collection
        self.batch_size = 32  # GPU-optimized batch size
        
        logger.info("[LAMBDA CHROMA] Service initialized with GPU optimizations")
    
    def get_client(self):
        """Get or create ChromaDB client with connection pooling"""
        if self.client is None:
            try:
                # Check if using ChromaDB Cloud (newtest database)
                use_cloud = os.getenv('USE_CLOUD_CHROMA', 'true').lower() == 'true'
                
                if use_cloud:
                    # Use ChromaDB Cloud with newtest database
                    from chromadb import CloudClient
                    
                    # ChromaDB Cloud configuration for newtest database
                    chroma_api_key = os.getenv('CHROMADB_API_KEY', 'ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW')
                    chroma_tenant = os.getenv('CHROMADB_TENANT', '28757e4a-f042-4b0c-ad7c-9257cd36b130')
                    chroma_database = os.getenv('CHROMADB_DATABASE', 'newtest')
                    
                    self.client = CloudClient(
                        api_key=chroma_api_key,
                        tenant=chroma_tenant,
                        database=chroma_database
                    )
                    
                    logger.info(f"[LAMBDA CHROMA] Connected to ChromaDB Cloud database: {chroma_database}")
                else:
                    # Fallback to local ChromaDB (for development)
                    chroma_host = os.getenv('CHROMADB_HOST', 'localhost')
                    chroma_port = int(os.getenv('CHROMADB_PORT', '8000'))
                    chroma_api_key = os.getenv('CHROMADB_API_KEY')
                    
                    # Connection settings optimized for Lambda Labs
                    settings = Settings(
                        chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
                        chroma_client_auth_credentials=chroma_api_key
                    ) if chroma_api_key else Settings()
                    
                    self.client = chromadb.HttpClient(
                        host=chroma_host,
                        port=chroma_port,
                        settings=settings
                    )
                    
                    logger.info(f"[LAMBDA CHROMA] Connected to local ChromaDB at {chroma_host}:{chroma_port}")
                
                # Test connection
                self.client.heartbeat()
                
                if use_cloud:
                    logger.info(f"[LAMBDA CHROMA] ChromaDB Cloud connection established")
                else:
                    logger.info(f"[LAMBDA CHROMA] Connected to {chroma_host}:{chroma_port}")
                
            except Exception as e:
                logger.error(f"[LAMBDA CHROMA] Connection failed: {e}")
                raise
        
        return self.client
    
    def get_batch_collections(self, force_refresh: bool = False) -> List[str]:
        """Get batch collections with intelligent caching"""
        current_time = time.time()
        
        # Return cached collections if still valid
        if not force_refresh and self.collections_cache and (current_time - self.last_cache_update) < self.cache_ttl:
            logger.info(f"[LAMBDA CHROMA] Using cached collections ({len(self.collections_cache)} collections)")
            return self.collections_cache
        
        try:
            client = self.get_client()
            all_collections = []
            offset = 0
            limit = 1000
            
            logger.info("[LAMBDA CHROMA] Fetching collections from ChromaDB...")
            
            # Fetch all collections with pagination
            while True:
                try:
                    collections_batch = client.list_collections(limit=limit, offset=offset)
                    if not collections_batch or len(collections_batch) == 0:
                        break
                    
                    all_collections.extend(collections_batch)
                    if len(collections_batch) < limit:
                        break
                    offset += limit
                    
                except Exception as e:
                    logger.warning(f"[LAMBDA CHROMA] Error fetching collections batch: {e}")
                    break
            
            # Filter for batch collections with enhanced filtering
            batch_collections = []
            for col in all_collections:
                col_name = col.name.lower()
                if any(keyword in col_name for keyword in ['batch', 'ultra_optimized', 'documents', 'northeastern']):
                    batch_collections.append(col.name)
                    # Store metadata for optimization
                    self.collections_metadata[col.name] = {
                        'name': col.name,
                        'created': getattr(col, 'created', None),
                        'metadata': getattr(col, 'metadata', {})
                    }
            
            # Update cache
            self.collections_cache = batch_collections
            self.last_cache_update = current_time
            
            logger.info(f"[LAMBDA CHROMA] Found {len(batch_collections)} batch collections")
            return batch_collections
            
        except Exception as e:
            logger.error(f"[LAMBDA CHROMA] Error getting collections: {e}")
            return self.collections_cache  # Return cached if available
    
    def search_documents_parallel(self, query_embedding: np.ndarray, n_results: int = 10, 
                                university_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Ultra-fast parallel search across collections with GPU optimization"""
        try:
            start_time = time.time()
            collections = self.get_batch_collections()
            
            if not collections:
                logger.warning("[LAMBDA CHROMA] No collections available for search")
                return []
            
            # Limit collections for performance (optimized for Lambda Labs)
            collections_to_search = collections[:self.max_collections_per_search]
            
            logger.info(f"[LAMBDA CHROMA] Searching {len(collections_to_search)} collections in parallel")
            
            all_documents = []
            search_tasks = []
            
            # Create search tasks
            for collection_name in collections_to_search:
                task = {
                    'collection_name': collection_name,
                    'query_embedding': query_embedding,
                    'n_results': n_results * 2,  # Get more results for better quality
                    'university_id': university_id
                }
                search_tasks.append(task)
            
            # Execute parallel searches
            with ThreadPoolExecutor(max_workers=self.parallel_workers) as executor:
                # Submit all search tasks
                future_to_task = {
                    executor.submit(self._search_single_collection_optimized, task): task
                    for task in search_tasks
                }
                
                # Collect results with timeout
                for future in as_completed(future_to_task, timeout=self.search_timeout * len(search_tasks)):
                    task = future_to_task[future]
                    try:
                        results = future.result(timeout=self.search_timeout)
                        if results:
                            all_documents.extend(results)
                    except Exception as e:
                        logger.warning(f"[LAMBDA CHROMA] Collection {task['collection_name']} search failed: {e}")
                        continue
            
            search_time = time.time() - start_time
            logger.info(f"[LAMBDA CHROMA] Parallel search completed in {search_time:.2f}s, found {len(all_documents)} documents")
            
            # Advanced deduplication with similarity scoring
            unique_documents = self._deduplicate_documents(all_documents)
            
            # Sort by similarity and return top N
            unique_documents.sort(key=lambda x: x['distance'])
            final_results = unique_documents[:n_results]
            
            logger.info(f"[LAMBDA CHROMA] Returning {len(final_results)} unique documents")
            return final_results
            
        except Exception as e:
            logger.error(f"[LAMBDA CHROMA] Error in parallel search: {e}")
            return []
    
    def _search_single_collection_optimized(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Optimized single collection search with error handling"""
        try:
            collection_name = task['collection_name']
            query_embedding = task['query_embedding']
            n_results = task['n_results']
            university_id = task.get('university_id')
            
            client = self.get_client()
            collection = client.get_collection(collection_name)
            
            # Build where filter for university_id if provided
            where_filter = {}
            if university_id:
                where_filter["university_id"] = university_id
            
            # Perform optimized search
            results = collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=n_results,
                where=where_filter if where_filter else None
            )
            
            documents = []
            if results and results.get('documents') and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results.get('metadatas') else {}
                    distance = results['distances'][0][i] if results.get('distances') else 1.0
                    doc_id = results['ids'][0][i] if results.get('ids') else str(i)
                    
                    # Calculate similarity score
                    similarity = 1 - distance
                    
                    documents.append({
                        'id': doc_id,
                        'content': doc,
                        'metadata': metadata,
                        'distance': distance,
                        'similarity': similarity,
                        'collection': collection_name
                    })
            
            return documents
            
        except Exception as e:
            logger.warning(f"[LAMBDA CHROMA] Error searching collection {task.get('collection_name', 'unknown')}: {e}")
            return []
    
    def _deduplicate_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Advanced deduplication with similarity scoring"""
        try:
            seen_ids = {}
            
            for doc in documents:
                doc_id = doc['id']
                similarity = doc.get('similarity', 0)
                
                # Keep document with highest similarity
                if doc_id not in seen_ids or similarity > seen_ids[doc_id].get('similarity', 0):
                    seen_ids[doc_id] = doc
            
            unique_documents = list(seen_ids.values())
            logger.info(f"[LAMBDA CHROMA] Deduplication: {len(documents)} -> {len(unique_documents)} documents")
            
            return unique_documents
            
        except Exception as e:
            logger.error(f"[LAMBDA CHROMA] Error in deduplication: {e}")
            return documents
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics for monitoring"""
        try:
            collections = self.get_batch_collections()
            
            stats = {
                'total_collections': len(collections),
                'collections': collections[:10],  # Show first 10
                'cache_status': {
                    'cached': len(self.collections_cache),
                    'last_update': self.last_cache_update,
                    'cache_age': time.time() - self.last_cache_update
                },
                'performance': {
                    'max_collections_per_search': self.max_collections_per_search,
                    'parallel_workers': self.parallel_workers,
                    'search_timeout': self.search_timeout
                }
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"[LAMBDA CHROMA] Error getting collection stats: {e}")
            return {'error': str(e)}
    
    def optimize_for_lambda_labs(self):
        """Apply Lambda Labs specific optimizations"""
        try:
            # Increase parallel workers for Lambda Labs GPUs
            if os.getenv('LAMBDA_LABS_GPU'):
                self.parallel_workers = 12
                self.max_collections_per_search = 200
                self.batch_size = 64
                logger.info("[LAMBDA CHROMA] Applied Lambda Labs GPU optimizations")
            
            # Optimize for specific GPU types
            gpu_type = os.getenv('GPU_TYPE', '').lower()
            if 'a100' in gpu_type or 'h100' in gpu_type:
                self.parallel_workers = 16
                self.max_collections_per_search = 250
                self.batch_size = 128
                logger.info("[LAMBDA CHROMA] Applied high-end GPU optimizations")
            elif '4090' in gpu_type or '3090' in gpu_type:
                self.parallel_workers = 10
                self.max_collections_per_search = 180
                self.batch_size = 48
                logger.info("[LAMBDA CHROMA] Applied mid-range GPU optimizations")
            
        except Exception as e:
            logger.error(f"[LAMBDA CHROMA] Error applying optimizations: {e}")
    
    def clear_cache(self):
        """Clear all caches for memory management"""
        try:
            self.collections_cache = []
            self.collections_metadata = {}
            self.last_cache_update = 0
            
            logger.info("[LAMBDA CHROMA] Cache cleared successfully")
            return True
            
        except Exception as e:
            logger.error(f"[LAMBDA CHROMA] Error clearing cache: {e}")
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        try:
            # Test connection
            client = self.get_client()
            heartbeat = client.heartbeat()
            
            # Get collection stats
            collections = self.get_batch_collections()
            
            health_status = {
                'status': 'healthy',
                'connection': 'ok',
                'heartbeat': heartbeat,
                'collections': len(collections),
                'cache_status': {
                    'cached_collections': len(self.collections_cache),
                    'cache_age': time.time() - self.last_cache_update
                },
                'performance': {
                    'parallel_workers': self.parallel_workers,
                    'max_collections': self.max_collections_per_search,
                    'search_timeout': self.search_timeout
                }
            }
            
            return health_status
            
        except Exception as e:
            logger.error(f"[LAMBDA CHROMA] Health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'connection': 'failed'
            }

# Global service instance
chroma_service = None

def get_chroma_service() -> LambdaGPUChromaService:
    """Get or create ChromaDB service instance"""
    global chroma_service
    
    if chroma_service is None:
        chroma_service = LambdaGPUChromaService()
        chroma_service.optimize_for_lambda_labs()
    
    return chroma_service

if __name__ == "__main__":
    # Test the service
    logger.info("[LAMBDA CHROMA] Testing ChromaDB service...")
    
    try:
        service = get_chroma_service()
        
        # Test health check
        health = service.health_check()
        print(f"Health status: {health}")
        
        # Test collection retrieval
        collections = service.get_batch_collections()
        print(f"Found {len(collections)} collections")
        
        # Test collection stats
        stats = service.get_collection_stats()
        print(f"Collection stats: {stats}")
        
    except Exception as e:
        logger.error(f"[LAMBDA CHROMA] Test failed: {e}")