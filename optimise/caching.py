import logging

logger = logging.getLogger(__name__)

# A simple in-memory cache. In a real app, this could be Redis.
_cache = {}

def get_cached_response(key: str):
    """Checks the cache for a given key (e.g., the user input)."""
    result = _cache.get(key)
    if result:
        logger.debug(f"Cache hit for key: {key}")
        return result
    
    logger.debug(f"Cache miss for key: {key}")
    return None

def set_cached_response(key: str, value: str):
    """Saves a response to the cache."""
    _cache[key] = value
    logger.debug(f"Cache set for key: {key}")
