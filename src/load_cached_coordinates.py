import json, os
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_FILE = PROJECT_ROOT / "data" / "coordinates_cache.json"

def load_cached_coordinates(cache_file=CACHE_FILE):
    """
    Load previously fetched coordinates from cache file
    """
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
        print(f"Loaded coordinates from cache successfully")
        return cache
    return {}
