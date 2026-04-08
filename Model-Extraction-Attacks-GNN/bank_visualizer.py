import networkx as nx
import matplotlib.pyplot as plt
import torch as th
import dgl


def plot_bank_network(G, labels, title="Bank Network", sample_size=100):
    """
    Plots a sample of the bank network highlighting fraud and benign nodes.
    """
    plt.figure(figsize=(12, 8))

    # Sample nodes for visualization since the full graph is too large
    nodes = list(G.nodes())
    sampled_nodes = nodes[:sample_size]
    subgraph = G.subgraph(sampled_nodes)

    # Node colors: Fraud (Red), Benign (Green)
    node_colors = []
    for node in sampled_nodes:
        color = "red" if labels[node] == 1 else "green"
        node_colors.append(color)

    pos = nx.spring_layout(subgraph, seed=42)
    nx.draw(
        subgraph,
        pos,
        node_color=node_colors,
        node_size=50,
        with_labels=False,
        edge_color="gray",
        alpha=0.6,
        arrows=True,
    )

    plt.title(title)
    plt.legend(
        handles=[
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor="red",
                markersize=10,
                label="Fraud",
            ),
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor="green",
                markersize=10,
                label="Benign",
            ),
        ]
    )
    plt.show()
    plt.savefig(f"{title.replace(' ', '_').lower()}.png")


def plot_extracted_network(surrogate_g, title="Extracted Network"):
    """
    Plots the structure of the surrogate graph used in the attack.
    """
    # Convert DGL to NetworkX
    G_nx = dgl.to_networkx(surrogate_g)

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G_nx, seed=42)
    nx.draw(
        G_nx,
        pos,
        node_color="blue",
        node_size=30,
        with_labels=False,
        edge_color="gray",
        alpha=0.6,
    )
    plt.title(title)
    plt.savefig(f"{title.replace(' ', '_').lower()}.png")
    plt.show()
