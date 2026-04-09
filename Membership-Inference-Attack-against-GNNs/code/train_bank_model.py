import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, random_split
import numpy as np
import time
import os
import argparse
import json

# Import custom modules
from attack_models import MLP
from data.dataset import BankTransactionDataset, TrainData, TestData
from nets.bank_transaction_classification.load_net import gnn_model


class DotDict(dict):
    def __init__(self, **kwds):
        self.update(kwds)
        self.__dict__ = self


def gpu_setup(use_gpu, gpu_id):
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    if torch.cuda.is_available() and use_gpu:
        print("cuda available with GPU:", torch.cuda.get_device_name(0))
        device = torch.device("cuda")
    else:
        print("cuda not available")
        device = torch.device("cpu")
    return device


def binary_acc(y_pred, y_test):
    y_pred_tag = torch.round(torch.sigmoid(y_pred))
    correct_results_sum = (y_pred_tag == y_test).sum().float()
    acc = correct_results_sum / y_test.shape[0]
    acc = torch.round(acc * 100)
    return acc


def train_epoch(model, optimizer, device, train_loader, epoch):
    model.train()
    epoch_loss = 0
    epoch_acc = 0

    for batch_idx, (features, labels) in enumerate(train_loader):
        features, labels = features.to(device), labels.to(device)
        optimizer.zero_grad()
        output = model(features)
        loss = F.binary_cross_entropy_with_logits(output, labels.unsqueeze(1).float())
        acc = binary_acc(output, labels)

        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()
        epoch_acc += acc.item()

    return epoch_loss / len(train_loader), epoch_acc / len(train_loader), optimizer


def evaluate_network(model, device, test_loader, epoch):
    model.eval()
    epoch_loss = 0
    epoch_acc = 0

    with torch.no_grad():
        for batch_idx, (features, labels) in enumerate(test_loader):
            features, labels = features.to(device), labels.to(device)
            output = model(features)
            loss = F.binary_cross_entropy_with_logits(
                output, labels.unsqueeze(1).float()
            )
            acc = binary_acc(output, labels)

            epoch_loss += loss.item()
            epoch_acc += acc.item()

    return epoch_loss / len(test_loader), epoch_acc / len(test_loader)


def train_val_pipeline(MODEL_NAME, DATASET_NAME, params, net_params, dirs):
    # Initialize variables
    t_avg_test_acc, t_avg_train_acc, t_avg_convergence_epochs = [], [], []
    s_avg_test_acc, s_avg_train_acc, s_avg_convergence_epochs = [], [], []

    t0 = time.time()
    per_epoch_time = []

    # Load dataset
    dataset = BankTransactionDataset(DATASET_NAME)

    # Get the device
    device = net_params["device"]

    # Create model
    model = gnn_model(MODEL_NAME, net_params)
    model = model.to(device)

    if MODEL_NAME in ["GCN"]:
        # For GCN models, we need to build graph from the data
        # This is a simplified version - in practice, you'd build proper graph structures
        pass

    # Training setup
    optimizer = torch.optim.Adam(
        model.parameters(), lr=params["init_lr"], weight_decay=params["weight_decay"]
    )
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="min",
        factor=params["lr_reduce_factor"],
        patience=params["lr_schedule_patience"],
        verbose=True,
    )

    # Split dataset into train/val/test
    train_size = int(0.7 * len(dataset))
    val_size = int(0.15 * len(dataset))
    test_size = len(dataset) - train_size - val_size
    train_dataset, val_dataset, test_dataset = random_split(
        dataset, [train_size, val_size, test_size]
    )

    # Create data loaders
    train_loader = DataLoader(
        train_dataset, batch_size=params["batch_size"], shuffle=True
    )
    val_loader = DataLoader(val_dataset, batch_size=params["batch_size"], shuffle=False)
    test_loader = DataLoader(
        test_dataset, batch_size=params["batch_size"], shuffle=False
    )

    # Training loop
    for epoch in range(params["epochs"]):
        # Training
        train_loss, train_acc, optimizer = train_epoch(
            model, optimizer, device, train_loader, epoch
        )

        # Validation
        val_loss, val_acc = evaluate_network(model, device, val_loader, epoch)

        print(
            f"Epoch: {epoch + 1:03d}, Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, "
            f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}"
        )

    # Final evaluation
    test_loss, test_acc = evaluate_network(model, device, test_loader, epoch)

    print(f"Final Test Accuracy: {test_acc:.4f}")

    # Save model weights
    torch.save(model.state_dict(), dirs[1] + "/model_weights.pth")

    return model, test_acc


def main():
    """
    USER CONTROLS
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        help="Please give a config.json file with training/model/data/param details",
    )
    parser.add_argument("--gpu_id", help="Please give a value for gpu id")
    parser.add_argument("--model", help="Please give a value for model name")
    parser.add_argument("--dataset", help="Please give a value for dataset name")
    parser.add_argument("--out_dir", help="Please give a value for out_dir")
    parser.add_argument("--seed", help="Please give a value for seed")
    parser.add_argument("--epochs", help="Please give a value for epochs")
    parser.add_argument("--batch_size", help="Please give a value for batch_size")
    parser.add_argument("--init_lr", help="Please give a value for init_lr")
    parser.add_argument(
        "--lr_reduce_factor", help="Please give a value for lr_reduce_factor"
    )
    parser.add_argument(
        "--lr_schedule_patience", help="Please give a value for lr_schedule_patience"
    )
    parser.add_argument("--min_lr", help="Please give a value for min_lr")
    parser.add_argument("--weight_decay", help="Please give a value for weight_decay")
    parser.add_argument(
        "--print_epoch_interval", help="Please give a value for print_epoch_interval"
    )
    parser.add_argument("--hidden_dim", help="Please give a value for hidden_dim")
    parser.add_argument("--out_dim", help="Please give a value for out_dim")
    parser.add_argument("--n_layers", help="Please give a value for n_layers")
    parser.add_argument("--dropout", help="Please give a value for dropout")
    parser.add_argument("--max_time", help="Please give a value for max_time")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    # device
    if args.gpu_id is not None:
        config["gpu"]["id"] = int(args.gpu_id)
        config["gpu"]["use"] = True
    device = gpu_setup(config["gpu"]["use"], config["gpu"]["id"])

    # model, dataset, out_dir
    if args.model is not None:
        MODEL_NAME = args.model
    else:
        MODEL_NAME = config["model"]
    if args.dataset is not None:
        DATASET_NAME = args.dataset
    else:
        DATASET_NAME = config["dataset"]
    if args.out_dir is not None:
        out_dir = args.out_dir
    else:
        out_dir = config["out_dir"]

    # parameters
    params = config["params"]
    if args.seed is not None:
        params["seed"] = int(args.seed)
    if args.epochs is not None:
        params["epochs"] = int(args.epochs)
    if args.batch_size is not None:
        params["batch_size"] = int(args.batch_size)
    if args.init_lr is not None:
        params["init_lr"] = float(args.init_lr)
    if args.lr_reduce_factor is not None:
        params["lr_reduce_factor"] = float(args.lr_reduce_factor)
    if args.lr_schedule_patience is not None:
        params["lr_schedule_patience"] = int(args.lr_schedule_patience)
    if args.min_lr is not None:
        params["min_lr"] = float(args.min_lr)
    if args.weight_decay is not None:
        params["weight_decay"] = float(args.weight_decay)
    if args.print_epoch_interval is not None:
        params["print_epoch_interval"] = int(args.print_epoch_interval)
    if args.max_time is not None:
        params["max_time"] = float(args.max_time)

    # network parameters
    net_params = config["net_params"]
    net_params["device"] = device
    net_params["gpu_id"] = config["gpu"]["id"]

    if args.hidden_dim is not None:
        net_params["hidden_dim"] = int(args.hidden_dim)
    if args.out_dim is not None:
        net_params["out_dim"] = int(args.out_dim)
    if args.n_layers is not None:
        net_params["n_layers"] = int(args.n_layers)
    if args.dropout is not None:
        net_params["dropout"] = float(args.dropout)

    # Set up dataset parameters
    net_params["in_dim"] = (
        5  # Features: amount, fraud, category_encoding, merchant_encoding, location_encoding
    )
    num_classes = 2  # Normal vs Fraud
    net_params["n_classes"] = num_classes
    net_params["batch_size"] = params["batch_size"]

    # Create output directories
    root_log_dir = (
        out_dir
        + "logs/"
        + MODEL_NAME
        + "_"
        + DATASET_NAME
        + "_GPU"
        + str(config["gpu"]["id"])
        + "_"
        + time.strftime("%Hh%Mm%Ss_on_%b_%d_%Y")
    )
    root_ckpt_dir = (
        out_dir
        + "checkpoints/"
        + MODEL_NAME
        + "_"
        + DATASET_NAME
        + "_GPU"
        + str(config["gpu"]["id"])
        + "_"
        + time.strftime("%Hh%Mm%Ss_on_%b_%d_%Y")
    )
    write_file_name = (
        out_dir
        + "results/result_"
        + MODEL_NAME
        + "_"
        + DATASET_NAME
        + "_GPU"
        + str(config["gpu"]["id"])
        + "_"
        + time.strftime("%Hh%Mm%Ss_on_%b_%d_%Y")
    )
    write_config_file = (
        out_dir
        + "configs/config_"
        + MODEL_NAME
        + "_"
        + DATASET_NAME
        + "_GPU"
        + str(config["gpu"]["id"])
        + "_"
        + time.strftime("%Hh%Mm%Ss_on_%b_%d_%Y")
    )
    dirs = root_log_dir, root_ckpt_dir, write_file_name, write_config_file

    if not os.path.exists(out_dir + "results"):
        os.makedirs(out_dir + "results")

    if not os.path.exists(out_dir + "configs"):
        os.makedirs(out_dir + "configs")

    # Train the model
    model, test_acc = train_val_pipeline(
        MODEL_NAME, DATASET_NAME, params, net_params, dirs
    )

    # Save final model
    final_model_path = (
        out_dir
        + "models/"
        + MODEL_NAME
        + "_"
        + DATASET_NAME
        + "_GPU"
        + str(config["gpu"]["id"])
        + "_"
        + time.strftime("%Hh%Mm%Ss_on_%b_%d_%Y")
    )

    if not os.path.exists(out_dir + "models"):
        os.makedirs(out_dir + "models")

    torch.save(model.state_dict(), final_model_path + "/final_model.pth")


if __name__ == "__main__":
    main()
