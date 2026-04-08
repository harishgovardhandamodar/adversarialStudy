import argparse
import torch as th
from bank_data_loader import load_bank_data
from bank_gnn_model import train_target_model, evaluate_model
from bank_attacks import run_attack
from bank_visualizer import plot_bank_network, plot_extracted_network


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv",
        type=str,
        default="synthetic_bank_transactions.csv",
        help="Path to CSV data",
    )
    parser.add_argument("--attack_type", type=int, default=0, help="Attack type (0-6)")
    parser.add_argument(
        "--attack_node_ratio",
        type=float,
        default=0.25,
        help="Proportion of nodes for attack",
    )
    parser.add_argument(
        "--sampling_strategy",
        type=str,
        default="random",
        choices=["random", "fraud"],
        help="Sampling strategy",
    )
    args = parser.parse_args()

    args = parser.parse_args()

    print(f"Adapting Project for Bank Transaction Data...")
    print(
        f"CSV: {args.csv}\nAttack Type: {args.attack_type}\nNode Ratio: {args.attack_node_ratio}"
    )

    # 1. Load Data
    G_nx, dgl_g, id_to_acc = load_bank_data(args.csv)
    features = dgl_g.ndata["feat"]
    labels = dgl_g.ndata["label"]

    # 2. Visualize Full Network
    print("Generating full network view...")
    plot_bank_network(G_nx, labels.numpy(), title="Full Bank Network")

    # 3. Run Attack
    surrogate_model, adv_g, adv_feat, fidelity = run_attack(
        args.attack_type, args.csv, args.attack_node_ratio, args.sampling_strategy
    )

    # 4. Visualize Extracted Graph
    print("Generating extracted graph view...")
    plot_extracted_network(adv_g, title=f"Extracted Network Attack {args.attack_type}")

    print(f"\nAttack Result: Fidelity = {fidelity:.4f}")


if __name__ == "__main__":
    main()
