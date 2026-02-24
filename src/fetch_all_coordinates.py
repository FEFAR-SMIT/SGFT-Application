from load_cached_coordinates import load_cached_coordinates
from save_coordinates_cache import save_coordinates_cache
from get_city_coordinates import get_city_coordinates

def fetch_all_coordinates(df, use_cache=True):
    """
    Fetch coordinates for all unique cities in the dataframe
    Returns a dictionary of {city: (lat, lon)}
    """

    # Get unique cities from dataframe
    cities = df['District'].dropna().unique().tolist()

    # Load cache if enabled
    coordinates = load_cached_coordinates() if use_cache else {}

    if(coordinates == {}):
        for idx, city in enumerate(cities, 1):
            rows = df[df['District'] == city]
            if rows.empty:
                print(f"State not found for city: {city}")
                continue
            state = rows['State'].iloc[0]
            coords = get_city_coordinates(city, state)
            if coords:
                coordinates[city] = coords
            save_coordinates_cache(coordinates)

    return coordinates, df