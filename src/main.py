import pandas as pd
from visualize_pygsp_graph import visualize_pygsp_graph
from save_pygsp_graph import save_pygsp_graph
from build_pygsp_graph import build_pygsp_graph
from compute_hermitian_random_walk_laplacian import compute_hermitian_random_walk_laplacian
from build_wind_adjacency_matrix import build_wind_adjacency_matrix
from build_graph import build_graph
from fetch_all_coordinates import fetch_all_coordinates
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def main():
    try:
        DATA_FILE = PROJECT_ROOT / "data" / "wind_data.xlsx"
        df = pd.read_excel(DATA_FILE)
    except FileNotFoundError:
        print("ERROR during reading the Excel file!!")
        return None, None
    
    coordinates, dataf = fetch_all_coordinates(df, use_cache=True)
    graph = build_graph(dataf, coordinates, radius_km=100, angle_segment_size=20)

    # Build Adjancency matrix
    adj_matrix, city_order = build_wind_adjacency_matrix(
        dataf, graph, coordinates, angle_segment_size=20
    )
    print(f"\nMatrix size: {adj_matrix.shape}")

    # # Save adjacency matrix to csv file
    # adj_df = pd.DataFrame(adj_matrix, index=city_order, columns=city_order)
    # adj_df.to_csv('wind_adjacency_matrix.csv')

    # Computing eigen values and eigen vectors using hermitian method for directed graph
    results_from_hermitian_method = compute_hermitian_random_walk_laplacian(adj_matrix, 0.01, True)
    print("\nResult from hermitian method of computing eigen values and eigen vectors:\n")
    print(results_from_hermitian_method)
    print("\n")

    # BUILD PYGSP GRAPH
    pygsp_graph = build_pygsp_graph(adj_matrix, city_order, coordinates)
    if pygsp_graph is not None:
        visualize_pygsp_graph(pygsp_graph, city_order)
        save_pygsp_graph(pygsp_graph, city_order)
    return graph, coordinates

if __name__ == "__main__":
    graph, coordinates = main()
