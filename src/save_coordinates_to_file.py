import pandas as pd
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
city_coordinates = PROJECT_ROOT / 'data' / 'city_coordinates.csv'

def save_coordinates_to_file(coordinates, filename=city_coordinates):
    """
    Save fetched coordinates to a CSV file
    """
    coords_df = pd.DataFrame([
        {'City': city, 'Latitude': lat, 'Longitude': lon}
        for city, (lat, lon) in coordinates.items()
    ])
    coords_df.to_csv(filename, index=False)
    print(f"Coordinates saved to '{filename}'")
