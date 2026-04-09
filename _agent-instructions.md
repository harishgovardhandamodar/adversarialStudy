    *   The `DatasetGenerator` is meant to be a utility. I should create a file named `data_generator.py`.
    *   The current project has:
        *   `bank_data_loader.py` (converts CSV to GNN graphs)
        *   `bank_gnn_model.py` (GCN model)
        *   `bank_attacks.py` (Attack logic)
        *   `bank_visualizer.py` (Visualization)
        *   `main_bank.py` (Entry point)
    *   The `DatasetGenerator` creates `target_accounts.csv`, `target_transactions.csv`, `shadow_accounts.csv`, and `shadow_transactions.csv`.
    *   The `bank_data_loader.py` currently expects a single `synthetic_bank_transactions.csv`. I need to update it to handle the new split (accounts vs transactions) and distinguish between target and shadow loaders.
    *   The `bank_attacks.py` currently trains a target model and then does the attack. It needs to be updated to:
        1.  Load target data to train the target model.
        2.  Load shadow data to create the adversary's surrogate dataset.
    *   The `main_bank.py` needs to trigger the data generation before running attacks.
    *   Step 1: Write `data_generator.py`.
    *   Step 2: Modify `bank_data_loader.py` to accept `accounts_csv` and `transactions_csv`.
    *   Step 3: Modify `bank_attacks.py` to load both target and shadow graphs.
    *   Step 4: Modify `main_bank.py` to:
        *   Import and run `data_generator.py`.
        *   Pass the target and shadow file paths to `run_attack`.
    *   *Wait*, `bank_data_loader.py` handles features calculation. I should ensure it's consistent.
    *   In `bank_attacks.py`, the `run_attack` function should now take `target_csvs` and `shadow_csvs`.
    *   The `run_attack` function can use the shadow graph to simulate the attacker's knowledge.
    *   Write `data_generator.py`.
    *   Update `bank_data_loader.py` signature: `load_bank_data(accounts_csv, transactions_csv)`.
    *   Update `bank_attacks.py`:
        *   Change `run_attack` params to accept target and shadow file paths.
        *   Train target model on target data.
        *   Create adv_g/adv_feat from shadow data.
    *   Update `main_bank.py`.




    Looking at attacks/attack_0.py:
- It has load_data(dataset_name) and attack0(dataset_name, attack_node_arg, cuda).
- It currently supports 'cora', 'citeseer', 'pubmed'.
- I should add support for 'synthetic_bank' or similar, utilizing utils.data_generator.DatasetGenerator.
Looking at attacks/attack_1.py:
- It expects specific text files for selected indices, query labels, and graph structure.
- This seems to be a different type of attack that relies on pre-generated data.
- However, the user says "update the attack files accordingly to use the datasets appropriately".
The DatasetGenerator generates accounts and transactions.
bank_data_loader.py converts these into DGL graphs.
The goal is to integrate the DatasetGenerator into the attack pipeline.
Wait, the user mentioned "save this generator to folder", which I did. "and update the attack files accordingly to use the datasets appropriately".
In attack_0.py, the target model is trained and then an attack is performed.
I should modify attack_0.py and other attack files to allow synthetic bank data to be used.
Let's start by seeing how I can integrate DatasetGenerator and load_bank_data into attack_0.py.
Currently attack_0.py does:
1. Load citation data.
2. Train a target GCN.
3. Generate synthetic nodes based on the target graph.
4. Train an extracted model.
For synthetic bank data:
1. Use DatasetGenerator to create target and shadow datasets.
2. Use load_bank_data to get DGL graphs.
3. Train target GCN.
4. Perform attack.
Wait, the DatasetGenerator already creates "Target Dataset" and "Shadow Dataset" and saves them to CSVs.
attack_0.py probably needs to be updated to handle these CSVs if dataset_name == 'bank'.
Let's check other attack files to see if they have a similar structure.
I'll read attack_2.py and attack_3.py quickly.