from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "output" / "pygsp_graph_visualization.png"

def visualize_pygsp_graph(G, cities, output_file=OUTPUT_FILE):
    """
    Visualize PyGSP graph as a DIRECTED graph
    """
    try:
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyArrowPatch
        coords = G.coords
        W = G.W.toarray()
        fig, axes = plt.subplots(1, 2, figsize=(20, 10))
        ax = axes[0]
        nonzero = W[W > 0]
        if len(nonzero) > 0:
            w_min, w_max = nonzero.min(), nonzero.max()
        else:
            w_min = w_max = 1
        node_radius = 0.1
        for i in range(G.N):
            for j in range(G.N):
                weight = W[i, j]
                if weight > 0:
                    x1, y1 = coords[i]
                    x2, y2 = coords[j]

                    # Calculate direction vector
                    dx = x2 - x1
                    dy = y2 - y1
                    distance = np.sqrt(dx**2 + dy**2)
                    # Normalize direction
                    dx_norm = dx / distance
                    dy_norm = dy / distance
                    
                    start_x = x1 + node_radius * dx_norm
                    start_y = y1 + node_radius * dy_norm
                    end_x = x2 - node_radius * dx_norm
                    end_y = y2 - node_radius * dy_norm
                    
                    lw = 0.5 + 2.5 * (weight - w_min) / (w_max - w_min + 1e-9)
                    arrow = FancyArrowPatch(
                        (start_x, start_y),
                        (end_x, end_y),
                        arrowstyle='-|>',
                        mutation_scale=20,
                        linewidth=lw,
                        alpha=0.6,
                        color='blue',
                        zorder=1
                    )
                    ax.add_patch(arrow)
        ax.scatter(coords[:, 0], coords[:, 1], s=50, c='silver', 
                   zorder=3, edgecolors='black', linewidths=0.7)
        ax.set_title("Wind Directed Graph", fontsize=14, fontweight='bold')
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.grid(alpha=0.3)
        ax.set_aspect('equal', adjustable='box')
        ax2 = axes[1]

        rows, cols = np.where(W > 0)  
        values = W[rows, cols] 
        sc = ax2.scatter(
            cols,
            rows,
            c=values,
            s=100,            
            cmap='viridis'
        )

        ax2.set_title("Adjacency Matrix")
        ax2.set_xlabel("Target City Index")
        ax2.set_ylabel("Source City Index")

        plt.colorbar(sc, ax=ax2, label="Wind Speed (m/s)")
        ax2.set_xticks(np.arange(0, len(cities), max(1, len(cities)//20)))
        ax2.set_yticks(np.arange(0, len(cities), max(1, len(cities)//20)))
        ax2.grid(alpha=0.3)
        ax2.invert_yaxis() 
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        plt.close()

    except Exception as e:
        print(f"\nvisualization failed: {e}")
