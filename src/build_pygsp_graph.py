import numpy as np

def build_pygsp_graph(adj_matrix, cities, coordinates):
    """
    Build a PyGSP graph from the wind-weighted adjacency matrix
    Parameters:
        adj_matrix: NxN numpy array with wind speeds as edge weights
        cities: list of city names
        coordinates: dict of {city: (lat, lon)}
    Returns:
        G: PyGSP Graph object
    """
    try:
        from pygsp import graphs
        import scipy.sparse as sp
        # Convert adjacency matrix to sparse format
        W = sp.csr_matrix(adj_matrix)
        # Create coordinates array for visualization (Nx2 array of [lon, lat])
        coords_array = np.array([
            [coordinates[city][1], coordinates[city][0]]  # [longitude, latitude]
            for city in cities
        ])

        G = graphs.Graph(W, coords=coords_array)
        G.city_names = cities
    
        print(f"Number of nodes: {G.N}")
        print(f"Number of edges: {G.Ne}")
        print(f"Is directed: {G.is_directed()}")

        # Compute graph Laplacian
        G.compute_laplacian(lap_type='combinatorial')
        print(f"Laplacian computed (type: combinatorial)")
        print("adj matrix:\n", adj_matrix,"\n")
        signal = np.array(adj_matrix.sum(axis=1)).flatten()

        # Perform SVD on the Laplacian matrix
        # Get the Laplacian matrix
        L = G.L.toarray() if hasattr(G.L, 'toarray') else G.L

        # Compute SVD: L = UΣV^T
        U_svd, sigma, Vt = np.linalg.svd(L, full_matrices=True)

        print(f"  U shape (left singular vectors): {U_svd.shape}")
        print(f"  Σ shape (singular values): {sigma.shape}")
        print(f"  V^T shape (right singular vectors): {Vt.shape}")

        V = Vt.T  # Transpose to get V from V^T
        Sigma_matrix = np.diag(sigma)  # Convert to diagonal matrix

        signal_reshaped = signal.reshape(-1, 1)
        print("signal shape: ", signal.shape)
        
        # z1 = (U^T + V^T)x/2
        # z2 = (U^T - V^T)x/2

        z1 = ((U_svd.T + V.T) @ signal_reshaped) / 2
        z2 = ((U_svd.T - V.T) @ signal_reshaped) / 2
        # Combine z1 and z2
        gft_signal = np.vstack([z1, z2])  # Shape: (2N, 1)

        # This is the inverse transformation
        def igft_svd(z1, z2, U_svd, V):
            """
            Inverse GFT using SVD decomposition
            """
            # Apply the inverse formula
            result = 0.5 * (U_svd @ (z1 + z2) + V @ (z1 - z2))
            return result
        
        # Reconstruct signal using IGFT
        reconstructed_signal_svd = igft_svd(z1, z2, U_svd, V)
        print(f"Reconstruction error: {np.linalg.norm(signal_reshaped - reconstructed_signal_svd)}")
        return G        
    except ImportError:
        print("\nERROR: PyGSP not installed!")
        return None
