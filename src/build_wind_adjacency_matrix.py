import numpy as np

def build_wind_adjacency_matrix(df, graph, coordinates, angle_segment_size=20):
    """
    Build NxN adjacency matrix using wind speed as edge weight with consideration of wind direction
    For each source city:
    - Find all cities in the wind direction segment
    - Assign wind speed ONLY to the closest city in that segment
    - All other cities in that segment get 0
    """

    cities = list(coordinates.keys())
    city_index = {city: i for i, city in enumerate(cities)}
    n = len(cities)

    adj_matrix = np.zeros((n, n))
    df['District'] = df['District'].astype(str).str.strip()
    wind_lookup = df.set_index('District')[[
        'Speed (in m/s)', 
        'Direction (in ° angle)'
    ]]

    for source_city, edges in graph.items():
        if source_city not in wind_lookup.index:
            continue

        wind_speed = wind_lookup.loc[source_city, 'Speed (in m/s)']
        wind_dir = wind_lookup.loc[source_city, 'Direction (in ° angle)']
        source_idx = city_index[source_city]

        # Convert wind direction into angle segment
        wind_segment = int(wind_dir.iloc[0] // angle_segment_size) if hasattr(wind_dir, 'iloc') else int(wind_dir // angle_segment_size)
        # Find all cities in the wind direction segment
        cities_in_wind_segment = []
        
        for edge in edges:
            edge_segment = edge['segment']
            
            # If city lies in wind direction segment
            if edge_segment == wind_segment:
                target_city = edge['city']
                target_idx = city_index[target_city]
                has_outgoing = np.any(adj_matrix[target_idx, :] > 0)
                if not has_outgoing:
                    cities_in_wind_segment.append({
                        'city': edge['city'],
                        'distance': edge['distance']
                    })
        
        # If there are cities in the wind segment, assign wind speed to the closest one
        if cities_in_wind_segment:
            # Sort by distance to find the closest
            cities_in_wind_segment.sort(key=lambda x: x['distance'])
            
            # Get the closest city
            closest_city = cities_in_wind_segment[0]['city']
            closest_idx = city_index[closest_city]
            
            # Assign wind speed to the closest city only
            wind_speed_value = wind_speed.iloc[0] if hasattr(wind_speed, 'iloc') else wind_speed

            #because in wind data, the direction is about wind coming into the source not going outward from the source
            adj_matrix[closest_idx,source_idx] = wind_speed_value
            
    row_sums = np.count_nonzero(adj_matrix, axis=1)
    
    print(f"Total nodes: {n}")
    print(f"Rows with exactly 1 connection: {np.sum(row_sums == 1)}")
    print(f"Rows with 0 connections: {np.sum(row_sums == 0)}")
    return adj_matrix, cities
