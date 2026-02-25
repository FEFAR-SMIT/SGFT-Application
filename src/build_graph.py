from collections import defaultdict
from get_angle_segment import get_angle_segment
from calculate_bearing import calculate_bearing
from haversine_distance import haversine_distance

def build_graph(df, coordinates, radius_km=200, angle_segment_size=5):
    """
    Build a graph where:
    - Nodes are cities
    - Edges connect cities within the range between radius_km and 400 km
    - At most one city per angle_segment_size degree segment
    Parameters:
        df: DataFrame with city data
        coordinates: dict of {city: (lat, lon)}
        radius_km: minimum distance for edges
        angle_segment_size: size of angle segments in degrees
    Returns:
        graph: dict of {city: [list of edge dicts]}
    """

    graph = defaultdict(list)
    cities = [city for city in df['District'].unique() if city in coordinates]
    print("Building Graph: \n")
    for idx, city1 in enumerate(cities, 1):
        lat1, lon1 = coordinates[city1]
        # Store candidates for each angle segment
        angle_segments = defaultdict(list)
        for city2 in cities:
            if city1 == city2:
                continue
            lat2, lon2 = coordinates[city2]
            distance = haversine_distance(lat1, lon1, lat2, lon2)
            if (distance > radius_km) and (distance <= 400):
                # Calculate bearing/angle
                bearing = calculate_bearing(lat1, lon1, lat2, lon2)
                segment = get_angle_segment(bearing, angle_segment_size)
                angle_segments[segment].append((city2, distance, bearing))
        
        # Select closest city from each angle segment
        for segment, candidates in angle_segments.items():
            # Sort by distance and take the closest
            candidates.sort(key=lambda x: x[1])
            closest_city, distance, bearing = candidates[0]
            graph[city1].append({
                'city': closest_city,
                'distance': distance,
                'bearing': bearing,
                'segment': segment
            })
    print("Graph generated successfully\n")
    return graph


