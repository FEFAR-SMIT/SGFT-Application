from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYGSP_OUTPUT_GRAPH_PKL = PROJECT_ROOT / 'output' / 'pygsp_graph.pkl'

def save_pygsp_graph(G, cities, filename=PYGSP_OUTPUT_GRAPH_PKL):
    """
    Save PyGSP graph to file using pickle
    Parameters:
        G: PyGSP Graph object
        cities: list of city names
        filename: output filename
    """
    try:
        import pickle
        graph_data = {
            'graph': G,
            'cities': cities,
            'adjacency_matrix': G.W.toarray()
        }
        with open(filename, 'wb') as f:
            pickle.dump(graph_data, f)
    except Exception as e:
        print(f"\n✗ Error saving graph: {e}")
