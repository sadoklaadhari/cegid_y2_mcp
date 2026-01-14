#!/usr/bin/env python3
"""
Cache Manager - Redis-based caching for performance
"""

import logging
import json
from typing import Dict, Any, Optional
from datetime import timedelta

logger = logging.getLogger(__name__)


class CacheManager:
    """Manage caching with Redis"""
    
    def __init__(self, config: Dict):
        """Initialize cache manager"""
        self.config = config
        self.enabled = config.get("enabled", False)
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 6379)
        self.db = config.get("db", 0)
        self.default_ttl = config.get("default_ttl", 300)
        
        self.redis_client = None
        
        if self.enabled:
            try:
                import redis
                self.redis_client = redis.Redis(
                    host=self.host,
                    port=self.port,
                    db=self.db,
                    decode_responses=True
                )
                # Test connection
                self.redis_client.ping()
                logger.info(f"Redis connected: {self.host}:{self.port}/{self.db}")
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}. Caching disabled.")
                self.redis_client = None
                self.enabled = False
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.enabled or not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                logger.debug(f"Cache hit: {key}")
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            ttl = ttl or self.default_ttl
            self.redis_client.setex(
                key,
                ttl,
                json.dumps(value)
            )
            logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete from cache"""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            self.redis_client.delete(key)
            logger.debug(f"Cache deleted: {key}")
            return True
        except Exception as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache"""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            self.redis_client.flushdb()
            logger.info("Cache cleared")
            return True
        except Exception as e:
            logger.warning(f"Cache clear error: {e}")
            return False
    
    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate cache by pattern"""
        if not self.enabled or not self.redis_client:
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
                logger.debug(f"Invalidated {len(keys)} cache entries matching {pattern}")
            return len(keys)
        except Exception as e:
            logger.warning(f"Cache invalidate error: {e}")
            return 0
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        if not self.enabled or not self.redis_client:
            return {
                "enabled": False,
                "message": "Cache disabled"
            }
        
        try:
            info = self.redis_client.info()
            return {
                "enabled": True,
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory_human", "N/A"),
                "keys_count": self.redis_client.dbsize(),
                "host": self.host,
                "port": self.port
            }
        except Exception as e:
            logger.warning(f"Error getting cache stats: {e}")
            return {"error": str(e)}


# In-memory fallback cache
class InMemoryCacheManager:
    """Fallback in-memory cache when Redis is not available"""
    
    def __init__(self):
        """Initialize in-memory cache"""
        self.cache: Dict[str, Any] = {}
        self.ttl_map: Dict[str, float] = {}
        logger.info("In-memory cache initialized")
    
    def get(self, key: str) -> Optional[Any]:
        """Get from memory"""
        if key in self.cache:
            return self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set in memory"""
        self.cache[key] = value
        return True
    
    def delete(self, key: str) -> bool:
        """Delete from memory"""
        if key in self.cache:
            del self.cache[key]
        return True
    
    def clear(self) -> bool:
        """Clear memory"""
        self.cache.clear()
        return True
    
    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate by pattern"""
        count = 0
        keys = [k for k in self.cache.keys() if pattern in k]
        for key in keys:
            del self.cache[key]
            count += 1
        return count
    
    def get_stats(self) -> Dict:
        """Get memory stats"""
        return {
            "type": "in-memory",
            "entries": len(self.cache),
            "message": "Using in-memory cache (Redis unavailable)"
        }
