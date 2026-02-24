import json
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_FILE = PROJECT_ROOT / "data" / "coordinates_cache.json"

def save_coordinates_cache(coordinates, cache_file=CACHE_FILE):
    """
    Save coordinates to cache file as json format
    """
    with open(cache_file, 'w') as f:
        json.dump(coordinates, f, indent=2)
    print(f"Saved {len(coordinates)} coordinates to cache: {cache_file}")
