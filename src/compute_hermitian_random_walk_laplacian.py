def compute_hermitian_random_walk_laplacian(W, q=0.01, verbose=True):
    """
    Compute the Unnormalized Hermitian Random Walk Laplacian for a directed graph.
    Parameters:
    -----------
    W : numpy.ndarray
        Weighted adjacency matrix (N x N) where W[i,j] is the weight from node i to node j
    q : float
        Required parameter for phase matrix 
    verbose : bool
        To print each important results calculations
        
    Returns:
    --------
    dict containing:
        - L_hrw: Unnormalized Hermitian Random Walk Laplacian
        - eigenvalues: Real eigenvalues (sorted ascending)
        - eigenvectors: Corresponding eigenvectors (columns)
        - P: Transition matrix
        - Pi: Stationary distribution (diagonal matrix)
        - P_tilde: Symmetric transition matrix
        - P_tilde_hermitian: Hermitian transition matrix
    """
    import numpy as np
    from scipy import linalg
    N = W.shape[0]
    out_degree = W.sum(axis=1)
    
    # Handle nodes with zero out-degree to avoid division by zero
    out_degree[out_degree == 0] = 1
    # Transition probabilities
    P = W / out_degree[np.newaxis, :]

    # Solve πP = π (or equivalently P^T π = π)
    # This is the left eigenvector of P with eigenvalue 1
    eigenvalues_P, eigenvectors_P = linalg.eig(P.T)
    
    # Find eigenvector corresponding to eigenvalue = 1
    idx = np.argmin(np.abs(eigenvalues_P - 1))
    pi = np.real(eigenvectors_P[:, idx])
    # Normalize so that sum = 1
    pi = pi / pi.sum()
    # Create diagonal matrix Π
    Pi = np.diag(pi)
    
    if verbose:
        print(f"Stationary distribution π: {pi}")
        print(f"Sum of π: {pi.sum():.6f}")

    P_tilde = 0.5 * (Pi @ P + P.T @ Pi)
    Gamma_q = np.ones((N, N), dtype=complex)
    for i in range(N):
        for j in range(N):
            if i != j:
                if W[i, j] > 0 or W[j, i] > 0:
                    theta_q = q * (W[i, j] - W[j, i]) * np.pi
                    Gamma_q[i, j] = np.exp(1j * theta_q)
    
    # Computing Hermitian transition matrix
    # Element-wise (Hadamard) product
    P_tilde_hermitian = Gamma_q * P_tilde
    
    if verbose:
        print(f"Hermitian P̃ computed")
        # Check Hermitian property: P̃ = P̃^H
        is_hermitian = np.allclose(P_tilde_hermitian, P_tilde_hermitian.conj().T)
        print(f"P̃ is Hermitian: {is_hermitian}")
    
    # Computing Laplacian
    L_hrw = Pi - P_tilde_hermitian
    if verbose:
        print(f"L^q_rw shape: {L_hrw.shape}")
    
    # Diagonalizing L^q_rw
    eigenvalues, eigenvectors = linalg.eigh(L_hrw)
    # Eigenvalues should be real and non-negative
    eigenvalues_real = np.real(eigenvalues)
    
    # Sort in ascending order
    sort_idx = np.argsort(eigenvalues_real)
    eigenvalues_sorted = eigenvalues_real[sort_idx]
    eigenvectors_sorted = eigenvectors[:, sort_idx]
    
    results = {
        'L_hrw': L_hrw,
        'eigenvalues': eigenvalues_sorted,
        'eigenvectors': eigenvectors_sorted,
        'P': P,
        'Pi': Pi,
        'stationary_distribution': pi,
        'P_tilde': P_tilde,
        'P_tilde_hermitian': P_tilde_hermitian,
        'Gamma_q': Gamma_q,
        'is_hermitian': is_hermitian,
        'q': q
    }
    return results
