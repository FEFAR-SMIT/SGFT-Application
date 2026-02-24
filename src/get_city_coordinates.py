try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError
    import time
except ImportError:
    print("WARNING: geopy not installed")
geolocator = Nominatim(user_agent="city_graph_builder_v1")

def get_city_coordinates(city_name, state_name, max_retries=2):
    """
    Get coordinates for a city using geopy
    Returns (latitude, longitude) or None if not found
    """
    # Try different query formats for better results
    queries = [
        f"{city_name}, {state_name}, India",
        f"{city_name} District, {state_name}, India",
        f"{city_name}, India"
    ]
    
    for query in queries:
        for attempt in range(max_retries):
            try:
                # Add delay to avoid rate limiting
                time.sleep(1.1)
                location = geolocator.geocode(query, timeout=10)
                if location:
                    print(f"  ✓ Found: {city_name} → ({location.latitude:.4f}, {location.longitude:.4f})")
                    return (location.latitude, location.longitude)
                
            except GeocoderTimedOut:
                if attempt < max_retries - 1:
                    print(f"Timeout for {city_name}, retrying...")
                    time.sleep(1.5)
                else:
                    print(f"  ✗ Timeout: {city_name} (after {max_retries} attempts)")
            except GeocoderServiceError as e:
                print(f" ✗ Service error for {city_name}: {e}")
                break
            except Exception as e:
                print(f"  ✗ Error for {city_name}: {e}")
                break
    
    print(f"  ✗ {city_name}: Not found")
    return None
