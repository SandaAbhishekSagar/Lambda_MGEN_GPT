"""
Lambda Labs GPU-Optimized Cache Manager
Ultra-fast caching system for sub-8-second response times
"""

import os
import time
import pickle
import hashlib
import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    data: Any
    timestamp: float
    access_count: int
    size_bytes: int
    ttl: float

class LambdaGPUCacheManager:
    """Ultra-optimized cache manager for Lambda Labs GPU deployment"""
    
    def __init__(self, cache_dir: str = "lambda_gpu_cache"):
        self.cache_dir = cache_dir
        self.memory_cache = {}
        self.disk_cache = {}
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_size': 0
        }
        
        # Performance settings optimized for Lambda Labs
        self.max_memory_cache_size = 1024 * 1024 * 1024  # 1GB memory cache
        self.max_disk_cache_size = 5 * 1024 * 1024 * 1024  # 5GB disk cache
        self.default_ttl = 3600  # 1 hour default TTL
        self.cleanup_interval = 300  # 5 minutes cleanup interval
        
        # Threading for async operations
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.cleanup_thread = None
        self.running = True
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        # Start cleanup thread
        self._start_cleanup_thread()
        
        logger.info("[LAMBDA CACHE] Cache manager initialized with GPU optimizations")
    
    def _start_cleanup_thread(self):
        """Start background cleanup thread"""
        def cleanup_worker():
            while self.running:
                try:
                    self._cleanup_expired_entries()
                    time.sleep(self.cleanup_interval)
                except Exception as e:
                    logger.error(f"[LAMBDA CACHE] Cleanup thread error: {e}")
        
        self.cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        self.cleanup_thread.start()
        logger.info("[LAMBDA CACHE] Cleanup thread started")
    
    def _generate_cache_key(self, key: str, namespace: str = "default") -> str:
        """Generate cache key with namespace"""
        return f"{namespace}:{hashlib.md5(key.encode()).hexdigest()}"
    
    def _get_cache_entry_size(self, data: Any) -> int:
        """Estimate cache entry size in bytes"""
        try:
            if isinstance(data, (str, bytes)):
                return len(data)
            elif isinstance(data, (list, tuple)):
                return sum(self._get_cache_entry_size(item) for item in data)
            elif isinstance(data, dict):
                return sum(self._get_cache_entry_size(k) + self._get_cache_entry_size(v) 
                          for k, v in data.items())
            elif isinstance(data, np.ndarray):
                return data.nbytes
            else:
                return len(pickle.dumps(data))
        except:
            return 1024  # Default estimate
    
    def _cleanup_expired_entries(self):
        """Clean up expired cache entries"""
        try:
            current_time = time.time()
            expired_keys = []
            
            # Check memory cache
            for key, entry in self.memory_cache.items():
                if current_time - entry.timestamp > entry.ttl:
                    expired_keys.append(key)
            
            # Remove expired entries
            for key in expired_keys:
                if key in self.memory_cache:
                    del self.memory_cache[key]
                    self.cache_stats['evictions'] += 1
            
            # Check disk cache
            disk_expired = []
            for key, entry in self.disk_cache.items():
                if current_time - entry.timestamp > entry.ttl:
                    disk_expired.append(key)
            
            for key in disk_expired:
                if key in self.disk_cache:
                    del self.disk_cache[key]
                    self.cache_stats['evictions'] += 1
            
            if expired_keys or disk_expired:
                logger.info(f"[LAMBDA CACHE] Cleaned up {len(expired_keys)} memory and {len(disk_expired)} disk entries")
                
        except Exception as e:
            logger.error(f"[LAMBDA CACHE] Error in cleanup: {e}")
    
    def _evict_lru_entries(self, required_size: int):
        """Evict least recently used entries to make space"""
        try:
            # Sort by access count and timestamp
            sorted_entries = sorted(
                self.memory_cache.items(),
                key=lambda x: (x[1].access_count, x[1].timestamp)
            )
            
            freed_size = 0
            evicted_keys = []
            
            for key, entry in sorted_entries:
                if freed_size >= required_size:
                    break
                
                freed_size += entry.size_bytes
                evicted_keys.append(key)
            
            # Remove evicted entries
            for key in evicted_keys:
                if key in self.memory_cache:
                    del self.memory_cache[key]
                    self.cache_stats['evictions'] += 1
            
            logger.info(f"[LAMBDA CACHE] Evicted {len(evicted_keys)} entries, freed {freed_size} bytes")
            
        except Exception as e:
            logger.error(f"[LAMBDA CACHE] Error in LRU eviction: {e}")
    
    def get(self, key: str, namespace: str = "default") -> Optional[Any]:
        """Get value from cache"""
        try:
            cache_key = self._generate_cache_key(key, namespace)
            current_time = time.time()
            
            # Check memory cache first
            if cache_key in self.memory_cache:
                entry = self.memory_cache[cache_key]
                
                # Check if expired
                if current_time - entry.timestamp > entry.ttl:
                    del self.memory_cache[cache_key]
                    self.cache_stats['misses'] += 1
                    return None
                
                # Update access count and return
                entry.access_count += 1
                self.cache_stats['hits'] += 1
                return entry.data
            
            # Check disk cache
            if cache_key in self.disk_cache:
                entry = self.disk_cache[cache_key]
                
                # Check if expired
                if current_time - entry.timestamp > entry.ttl:
                    del self.disk_cache[cache_key]
                    self.cache_stats['misses'] += 1
                    return None
                
                # Load from disk
                try:
                    disk_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
                    if os.path.exists(disk_file):
                        with open(disk_file, 'rb') as f:
                            data = pickle.load(f)
                        
                        # Move to memory cache if small enough
                        if entry.size_bytes < 1024 * 1024:  # 1MB threshold
                            self.memory_cache[cache_key] = entry
                            if cache_key in self.disk_cache:
                                del self.disk_cache[cache_key]
                        
                        entry.access_count += 1
                        self.cache_stats['hits'] += 1
                        return data
                except Exception as e:
                    logger.warning(f"[LAMBDA CACHE] Error loading from disk: {e}")
                    if cache_key in self.disk_cache:
                        del self.disk_cache[cache_key]
            
            self.cache_stats['misses'] += 1
            return None
            
        except Exception as e:
            logger.error(f"[LAMBDA CACHE] Error getting cache entry: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None, 
            namespace: str = "default", force_memory: bool = False) -> bool:
        """Set value in cache"""
        try:
            cache_key = self._generate_cache_key(key, namespace)
            current_time = time.time()
            ttl = ttl or self.default_ttl
            size_bytes = self._get_cache_entry_size(value)
            
            # Create cache entry
            entry = CacheEntry(
                data=value,
                timestamp=current_time,
                access_count=0,
                size_bytes=size_bytes,
                ttl=ttl
            )
            
            # Decide storage location
            use_memory = force_memory or size_bytes < 1024 * 1024  # 1MB threshold
            
            if use_memory:
                # Check memory cache size
                current_memory_size = sum(entry.size_bytes for entry in self.memory_cache.values())
                
                if current_memory_size + size_bytes > self.max_memory_cache_size:
                    # Evict LRU entries
                    self._evict_lru_entries(size_bytes)
                
                # Store in memory cache
                self.memory_cache[cache_key] = entry
                logger.debug(f"[LAMBDA CACHE] Stored in memory cache: {cache_key}")
                
            else:
                # Store in disk cache
                try:
                    disk_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
                    with open(disk_file, 'wb') as f:
                        pickle.dump(value, f)
                    
                    self.disk_cache[cache_key] = entry
                    logger.debug(f"[LAMBDA CACHE] Stored in disk cache: {cache_key}")
                    
                except Exception as e:
                    logger.error(f"[LAMBDA CACHE] Error storing to disk: {e}")
                    return False
            
            # Update stats
            self.cache_stats['total_size'] += size_bytes
            
            return True
            
        except Exception as e:
            logger.error(f"[LAMBDA CACHE] Error setting cache entry: {e}")
            return False
    
    def delete(self, key: str, namespace: str = "default") -> bool:
        """Delete value from cache"""
        try:
            cache_key = self._generate_cache_key(key, namespace)
            deleted = False
            
            # Remove from memory cache
            if cache_key in self.memory_cache:
                del self.memory_cache[cache_key]
                deleted = True
            
            # Remove from disk cache
            if cache_key in self.disk_cache:
                disk_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
                if os.path.exists(disk_file):
                    os.remove(disk_file)
                del self.disk_cache[cache_key]
                deleted = True
            
            return deleted
            
        except Exception as e:
            logger.error(f"[LAMBDA CACHE] Error deleting cache entry: {e}")
            return False
    
    def clear(self, namespace: Optional[str] = None) -> bool:
        """Clear cache entries"""
        try:
            if namespace:
                # Clear specific namespace
                keys_to_remove = []
                for key in self.memory_cache.keys():
                    if key.startswith(f"{namespace}:"):
                        keys_to_remove.append(key)
                
                for key in keys_to_remove:
                    del self.memory_cache[key]
                
                # Clear disk files
                for key in keys_to_remove:
                    disk_file = os.path.join(self.cache_dir, f"{key}.pkl")
                    if os.path.exists(disk_file):
                        os.remove(disk_file)
                    if key in self.disk_cache:
                        del self.disk_cache[key]
            else:
                # Clear all caches
                self.memory_cache.clear()
                self.disk_cache.clear()
                
                # Remove all disk files
                for filename in os.listdir(self.cache_dir):
                    if filename.endswith('.pkl'):
                        os.remove(os.path.join(self.cache_dir, filename))
            
            logger.info(f"[LAMBDA CACHE] Cache cleared for namespace: {namespace or 'all'}")
            return True
            
        except Exception as e:
            logger.error(f"[LAMBDA CACHE] Error clearing cache: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            current_time = time.time()
            
            # Calculate hit rate
            total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
            hit_rate = (self.cache_stats['hits'] / total_requests * 100) if total_requests > 0 else 0
            
            # Calculate memory usage
            memory_entries = len(self.memory_cache)
            disk_entries = len(self.disk_cache)
            memory_size = sum(entry.size_bytes for entry in self.memory_cache.values())
            
            # Count expired entries
            expired_memory = sum(1 for entry in self.memory_cache.values() 
                               if current_time - entry.timestamp > entry.ttl)
            expired_disk = sum(1 for entry in self.disk_cache.values() 
                             if current_time - entry.timestamp > entry.ttl)
            
            stats = {
                'memory_cache': {
                    'entries': memory_entries,
                    'size_bytes': memory_size,
                    'expired_entries': expired_memory
                },
                'disk_cache': {
                    'entries': disk_entries,
                    'expired_entries': expired_disk
                },
                'performance': {
                    'hits': self.cache_stats['hits'],
                    'misses': self.cache_stats['misses'],
                    'hit_rate': round(hit_rate, 2),
                    'evictions': self.cache_stats['evictions']
                },
                'settings': {
                    'max_memory_size': self.max_memory_cache_size,
                    'max_disk_size': self.max_disk_cache_size,
                    'default_ttl': self.default_ttl,
                    'cleanup_interval': self.cleanup_interval
                }
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"[LAMBDA CACHE] Error getting stats: {e}")
            return {'error': str(e)}
    
    def optimize_for_lambda_labs(self):
        """Apply Lambda Labs specific optimizations"""
        try:
            # Optimize for Lambda Labs GPUs
            if os.getenv('LAMBDA_LABS_GPU'):
                self.max_memory_cache_size = 2 * 1024 * 1024 * 1024  # 2GB for GPU instances
                self.max_disk_cache_size = 10 * 1024 * 1024 * 1024  # 10GB for GPU instances
                self.default_ttl = 7200  # 2 hours for GPU instances
                logger.info("[LAMBDA CACHE] Applied Lambda Labs GPU optimizations")
            
            # Optimize for specific GPU types
            gpu_type = os.getenv('GPU_TYPE', '').lower()
            if 'a100' in gpu_type or 'h100' in gpu_type:
                self.max_memory_cache_size = 4 * 1024 * 1024 * 1024  # 4GB for high-end GPUs
                self.max_disk_cache_size = 20 * 1024 * 1024 * 1024  # 20GB for high-end GPUs
                logger.info("[LAMBDA CACHE] Applied high-end GPU optimizations")
            
        except Exception as e:
            logger.error(f"[LAMBDA CACHE] Error applying optimizations: {e}")
    
    def shutdown(self):
        """Shutdown cache manager"""
        try:
            self.running = False
            
            if self.cleanup_thread:
                self.cleanup_thread.join(timeout=5)
            
            self.executor.shutdown(wait=True)
            
            logger.info("[LAMBDA CACHE] Cache manager shutdown complete")
            
        except Exception as e:
            logger.error(f"[LAMBDA CACHE] Error during shutdown: {e}")

# Global cache manager instance
cache_manager = None

def get_cache_manager() -> LambdaGPUCacheManager:
    """Get or create cache manager instance"""
    global cache_manager
    
    if cache_manager is None:
        cache_manager = LambdaGPUCacheManager()
        cache_manager.optimize_for_lambda_labs()
    
    return cache_manager

if __name__ == "__main__":
    # Test the cache manager
    logger.info("[LAMBDA CACHE] Testing cache manager...")
    
    try:
        cache = get_cache_manager()
        
        # Test basic operations
        cache.set("test_key", "test_value", ttl=60)
        value = cache.get("test_key")
        print(f"Test value: {value}")
        
        # Test stats
        stats = cache.get_stats()
        print(f"Cache stats: {stats}")
        
        # Test cleanup
        cache.clear()
        print("Cache cleared")
        
    except Exception as e:
        logger.error(f"[LAMBDA CACHE] Test failed: {e}")
