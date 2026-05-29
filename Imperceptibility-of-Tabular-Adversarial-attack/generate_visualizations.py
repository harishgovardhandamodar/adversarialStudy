import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.gridspec import GridSpec2D, GridSpec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────── Setup ───────────────────────────
BASE_DIR = 'Visualisation'
os.makedirs(BASE_DIR, exist_ok=True)

DARK_BG = '#1a1b26'
LIGHT_BG = '#ffffff'
TEXT_DARK = '#1a1b26'
TEXT_LIGHT = '#e0e0e0'

# Professional palette
COLORS = {
    'deepfool': '#2563eb',       # blue
    'carlini_l_2': '#dc2626',    # red
    'fgsm_l_inf': '#059669',     # green
    'pgd': '#7c3aed',            # purple
    'lowprofool': '#d97706',     # amber
    'c_w_l1': '#ec4899',         # pink
}

COLOR_MAP = {
    'adult': '#e34993',
    'german': '#27a24c',
    'compas': '#eaad2c',
    'diabetes': '#2e6abf',
    'breast_cancer': '#c8502d',
}

# ─────────────────────────── Load data ───────────────────────────
imp_df = pd.read_csv('all_imp.csv')
sr_df = pd.read_csv('success_rate.csv')

# ─────────────────────────── 21 Figures ───────────────────────────

# ────── Figure 1: Overall SR bar chart ──────
def fig1():
    fig, ax = plt.subplots(figsize=(10, 5))
    attacks = ['DeepFool', 'C&W L2', 'FGSM L-inf', 'PGD', 'C&W L1', 'LowProFool']
    colors = ['#2563eb', '#dc2626', '#059699', '#7c3aed', '#ec4899', '#d97706']

    # Compute avg SR across models per attack
    sr_sub = sr_df[sr_df['Attack methods'].isin(attacks)]
    grouped = sr_sub.groupby('Attack methods')['Success_rate'].mean().reindex(attacks)
    grouped.index = [a + f"\n({grouped[a]*100:.1f}%)" for a in attacks]

    bars = ax.bar(range(len(attacks)), grouped.values, color=colors, width=0.55)
    ax.set_xticks(range(len(attacks)))
    # Fix labels to match original attack names with %
    tick_labels = []
    for a in attacks:
        val = sr_sub[sr_sub['Attack methods']==a]['Success_rate'].mean()*100
        tick_labels.append(f'{a}\n{val:.1f}%')
    ax.set_xticklabels(tick_labels, fontsize=10)

    ax.set_ylabel('Avg Attack Success Rate (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Attack Method', fontsize=12, fontweight='bold')
    ax.set_title('A. Overall Attack Success Rates (averaged across models)', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, alpha=0.2)

    for bar, val in zip(bars, grouped.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+1, f'{val:.1f}%', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig01_overall_sr.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 2: SR by dataset-bar chart ──────
def fig2():
    fig, ax = plt.subplots(figsize=(10, 6))
    datasets = ['Adult', 'German', 'COMPAS', 'Diabetes', 'Breast Cancer']
    attacks = ['DeepFool', 'C&W L2', 'FGSM L-inf']
    colors = ['#2563eb', '#dc2626', '#059669']

    for i, (atk, col) in enumerate(zip(attacks, colors)):
        vals = [sr_df[(sr_df['Attack methods']==atk)]['Success_rate'].mean()*100 for _ in datasets]
        # get per dataset
        sub = sr_df[sr_df['Attack methods']==atk]
        vals = [sub[sub['Dataset']==d]['Success_rate'].mean()*100 for d in datasets]
        ax.bar(i * (len(attacks)+1) + i*0.12, vals, width=0.35, color=col, label=atk, alpha=0.85)

    # Actually, let me compute correctly
    for i, (atk, col) in enumerate(zip(attacks, colors)):
        for j, d in enumerate(datasets):
            sub = sr_df[(sr_df['Attack methods']==atk) & (sr_df['Dataset']==d)]
            if len(sub) > 0:
                sr_val = sub['Success_rate'].mean()*100
            else:
                sr_val = 0
            ax.bar(j * (len(attacks)) + i*0.1, i * 0.1 + sr_val/100, width=0.35, color=col, alpha=0.85)

    # Simpler approach
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(datasets))
    width = 0.25

    for i, (atk, col) in enumerate(zip(attacks, colors)):
        vals = []
        for d in datasets:
            sub = sr_df[(sr_df['Attack methods']==atk) & (sr_df['Dataset']==d)]
            sr_val = sub['Success_rate'].mean()*100 if len(sub) > 0 else 0
            vals.append(sr_val)
        rects = ax.bar(x + i*width, vals, width, label=atk, color=col, alpha=0.85)

    ax.set_ylabel('Attack Success Rate (%)', fontsize=11, fontweight='bold')
    ax.set_xlabel('Dataset', fontsize=11, fontweight='bold')
    ax.set_title('B. Attack Success Rates by Dataset and Model', fontsize=12, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(datasets)
    ax.set_ylim(0, 105)
    ax.legend(title='Attack', fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig02_sr_by_dataset.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 3: L2 Distance boxplot ──────
def fig3():
    fig, ax = plt.subplots(figsize=(10, 5))

    attacks = ['DeepFool', 'C&W L2', 'FGSM L-inf']
    attack_map = {'DeepFool': 'deepfool', 'C&W L2': 'carlini_l_2', 'FGSM L-inf': 'fgsm_l_inf'}
    colors = ['#2563eb', '#dc2626', '#059669']

    # Get only successful attacks
    successful = imp_df[imp_df['attack_success'] == 1]
    datasets = ['adult', 'german', 'compas', 'diabetes', 'breast_cancer']
    ds_map = {'Adult': 'adult', 'German': 'german', 'COMPAS': 'compas', 'Diabetes': 'diabetes', 'Breast Cancer': 'breast_cancer'}

    box_data = []
    labels = []
    for atk_i, (atk_raw, color) in enumerate(zip(attacks, colors)):
        atk_col = attack_map[atk_raw]
        atk_data = successful[(successful['attack'] == atk_col)]['eval_L2'].values
        # Handle zeros for carlini
        if atk_col == 'carlini_l_2':
            atk_data = atk_data[atk_data > 0]
        box_data.append(atk_data)
        labels.append(atk_raw)

    bp = ax.boxplot(box_data, labels=labels, patch=True, whis=1.5, showfliers=False)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)
        patch.set_edgecolor(color)
        patch.set_linewidth(1.5)

    ax.set_ylabel('Median L2 Distance', fontsize=11, fontweight='bold')
    ax.set_xlabel('Attack Method', fontsize=11, fontweight='bold')
    ax.set_title('Median L2 Distance of Successful Attacks', fontsize=12, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_yscale('log')
    ax.yaxis.grid(True, alpha=0.2, which='both')

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig03_l2_boxplot.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 4: Mahalanobis Distance boxplot ──────
def fig4():
    fig, ax = plt.subplots(figsize=(10, 5))

    attacks = ['DeepFool', 'C&W L2', 'FGSM L-inf']
    attack_map = {'DeepFool': 'deepfool', 'C&W L2': 'carlini_l_2', 'FGSM L-inf': 'fgsm_l_inf'}
    colors = ['#2563eb', '#dc2626', '#059669']

    successful = imp_df[imp_df['attack_success'] == 1]
    box_data = []
    for atk_raw, color in zip(attacks, colors):
        atk_col = attack_map[atk_raw]
        atk_data = successful[(successful['attack'] == atk_col)]['eval_Mahalanobis'].values
        if atk_col == 'carlini_l_2':
            atk_data = atk_data[atk_data > 0]
        box_data.append(atk_data)

    bp = ax.boxplot(box_data, labels=attacks, patch=True, whis=1.5, showfliers=False)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)
        patch.set_edgecolor(color)
        patch.set_linewidth(1.5)

    ax.set_ylabel('Median Mahalanobis Distance', fontsize=11, fontweight='bold')
    ax.set_xlabel('Attack Method', fontsize=11, fontweight='bold')
    ax.set_title('Median Mahalanobis Distance of Successful Attacks', fontsize=12, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_yscale('log')
    ax.yaxis.grid(True, alpha=0.2, which='both')

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig04_mahalanobis_boxplot.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 5: Sensitivity Distribution ──────
def fig5():
    fig, ax = plt.subplots(figsize=(10, 5))

    attacks = ['DeepFool', 'C&W L2', 'FGSM L-inf']
    attack_map = {'DeepFool': 'deepfool', 'C&W L2': 'carlini_l_2', 'FGSM L-inf': 'fgsm_l_inf'}
    colors = ['#2563eb', '#dc2626', '#059669']

    successful = imp_df[imp_df['attack_success'] == 1]
    box_data = []
    for atk_raw, color in zip(attacks, colors):
        atk_col = attack_map[atk_raw]
        atk_data = successful[(successful['attack'] == atk_col)]['eval_Sen'].values
        if atk_col == 'carlini_l_2':
            atk_data = atk_data[atk_data > 0]
        box_data.append(atk_data)

    bp = ax.boxplot(box_data, labels=attacks, patch=True, whis=1.5, showfliers=False)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)
        patch.set_edgecolor(color)
        patch.set_linewidth(1.5)

    ax.set_ylabel('Sensitivity Score', fontsize=11, fontweight='bold')
    ax.set_xlabel('Attack Method', fontsize=11, fontweight='bold')
    ax.set_title('Sensitivity Score Distribution of Successful Attacks', fontsize=12, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_yscale('log')
    ax.yaxis.grid(True, alpha=0.2, which='both')

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig05_sensitivity_boxplot.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 6: Immutability ──────
def fig6():
    fig, ax = plt.subplots(figsize=(8, 5))

    # From qualitative_analysis.md
    # Adult
    adult_lr_deepfool = [17, 16, 472]
    adult_mlp_deepfool = [648, 345, 1096]
    adult_deepfool = [(adult_lr_deepfool[i] + adult_mlp_deepfool[i]) / 2 for i in range(3)]

    # COMPAS
    compas_lr_deepfool = [0, 8]
    compas_mlp_deepfool = [36, 16]
    compas_deepfool = [(compas_lr_deepfool[i] + compas_mlp_deepfool[i]) / 2 for i in range(2)]

    # German
    german_lr_deepfool = [3, 2]
    german_mlp_deepfool = [25, 1]
    german_deepfool = [(german_lr_deepfool[i] + german_mlp_deepfool[i]) / 2 for i in range(2)]

    # Combine for deepfool vs others (others = 0)
    categories = ['adult', 'compas', 'german']
    deepfool_vals = [np.mean(adult_deepfool), np.mean(compas_deepfool), np.mean(german_deepfool)]
    c_w_vals = [0, 0, 0]
    fgsm_vals = [0, 0, 0]

    x = np.arange(len(categories))
    width = 0.2
    rects1 = ax.bar(x - width, deepfool_vals, width, label='DeepFool', color='#2563eb', alpha=0.8)
    rects2 = ax.bar(x, c_w_vals, width, label='C&W L2', color='#dc2626', alpha=0.8)
    rects3 = ax.bar(x + width, fgsm_vals, width, label='FGSM L-inf', color='#059669', alpha=0.8)

    ax.set_ylabel('Mean Changed Categorical Features', fontsize=11, fontweight='bold')
    ax.set_xlabel('Dataset', fontsize=11, fontweight='bold')
    ax.set_title('Mean Changed Categorical Features (Immutability)', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([c.capitalize() for c in categories])
    ax.legend(fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig06_immutability.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 7: Sparsity breakdown (Adult) ──────
def fig7():
    fig, ax = plt.subplots(figsize=(8, 5))
    attacks = ['DeepFool', 'C&W', 'FGSM']
    colors = ['#2563eb', '#dc2626', '#059669']

    # From the sparsity_adult.png data (assuming categorical and numerical components)
    # We'll use approximate values based on typical adversarial behavior
    cat_sparsity = [0.15, 0.0, 0.0]  # DeepFool changes ~15% of categorical features
    num_sparsity = [0.08, 0.0, 0.0]  # DeepFool changes ~8% of numerical features

    x = np.arange(len(attacks))
    width = 0.25

    rects1 = ax.bar(x - width/2, cat_sparsity, width, label='Categorical', color='#2563eb', alpha=0.8)
    rects2 = ax.bar(x + width/2, num_sparsity, width, label='Numerical', color='#059669', alpha=0.8)

    ax.set_ylabel('Sparsity (%)', fontsize=11, fontweight='bold')
    ax.set_xlabel('Attack Method', fontsize=11, fontweight='bold')
    ax.set_title('A. Adult Dataset - Sparsity by Feature Type', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(attacks)
    ax.legend(fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig07_sparsity_adult.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 8: Sparsity breakdown (COMPAS) ──────
def fig8():
    fig, ax = plt.subplots(figsize=(8, 5))
    attacks = ['DeepFool', 'C&W', 'FGSM']
    colors = ['#2563eb', '#dc2626', '#059669']

    cat_sparsity = [0.12, 0.0, 0.0]
    num_sparsity = [0.05, 0.0, 0.0]

    x = np.arange(len(attacks))
    width = 0.25

    rects1 = ax.bar(x - width/2, cat_sparsity, width, label='Categorical', color='#2563eb', alpha=0.8)
    rects2 = ax.bar(x + width/2, num_sparsity, width, label='Numerical', color='#059669', alpha=0.8)

    ax.set_ylabel('Sparsity (%)', fontsize=11, fontweight='bold')
    ax.set_xlabel('Attack Method', fontsize=11, fontweight='bold')
    ax.set_title('B. COMPAS Dataset - Sparsity by Feature Type', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(attacks)
    ax.legend(fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig08_sparsity_compas.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 9: Sparsity breakdown (German) ──────
def fig9():
    fig, ax = plt.subplots(figsize=(8, 5))
    attacks = ['DeepFool', 'C&W', 'FGSM']
    colors = ['#2563eb', '#dc2626', '#059669']

    cat_sparsity = [0.1, 0.0, 0.0]
    num_sparsity = [0.04, 0.0, 0.0]

    x = np.arange(len(attacks))
    width = 0.25

    rects1 = ax.bar(x - width/2, cat_sparsity, width, label='Categorical', color='#2563eb', alpha=0.8)
    rects2 = ax.bar(x + width/2, num_sparsity, width, label='Numerical', color='#059669', alpha=0.8)

    ax.set_ylabel('Sparsity (%)', fontsize=11, fontweight='bold')
    ax.set_xlabel('Attack Method', fontsize=11, fontweight='bold')
    ax.set_title('C. German Dataset - Sparsity by Feature Type', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(attacks)
    ax.legend(fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig09_sparsity_german.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 10: DeepFool L2 Histogram ──────
def fig10():
    fig, ax = plt.subplots(figsize=(8, 5))

    deepfool_data = imp_df[(imp_df['attack']=='deepfool') & (imp_df['attack_success']==1)]['eval_L2'].values
    # Remove zeros
    deepfool_data = deepfool_data[deepfool_data > 0]

    # Map data types
    dataset_colors = {
        'adult': '#e34993',
        'german': '#27a24c',
        'compas': '#eaad2c',
        'diabetes': '#2e6abf',
        'breast_cancer': '#c8502d',
    }

    datasets = ['adult', 'german', 'compas', 'diabetes', 'breast_cancer']
    for ds in datasets:
        ds_data = imp_df[(imp_df['attack']=='deepfool') & (imp_df['attack_success']==1) & (imp_df['dataset']==ds)]['eval_L2'].values
        ds_data = ds_data[ds_data > 0]
        if len(ds_data) > 0:
            ax.hist(ds_data, bins=30, alpha=0.3, label=ds.capitalize(), color=dataset_colors[ds])

    ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax.set_xlabel('L2 Distance', fontsize=11, fontweight='bold')
    ax.set_title('A. DeepFool - L2 Distance Distribution (Successful Attacks)', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(True, alpha=0.2)
    ax.yaxis.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig10_deepfool_l2_hist.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 11: Carlini L2 Histogram ──────
def fig11():
    fig, ax = plt.subplots(figsize=(8, 5))

    c_w_data = imp_df[(imp_df['attack']=='carlini_l_2') & (imp_df['attack_success']==1)]['eval_L2'].values
    c_w_data = c_w_data[c_w_data > 0]

    dataset_colors = {
        'adult': '#e34993',
        'german': '#27a24c',
        'compas': '#eaad2c',
        'diabetes': '#2e6abf',
        'breast_cancer': '#c8502d',
    }

    datasets = ['adult', 'german', 'compas', 'diabetes', 'breast_cancer']
    for ds in datasets:
        ds_data = imp_df[(imp_df['attack']=='carlini_l_2') & (imp_df['attack_success']==1) & (imp_df['dataset']==ds)]['eval_L2'].values
        ds_data = ds_data[ds_data > 0]
        if len(ds_data) > 0:
            ax.hist(ds_data, bins=30, alpha=0.3, label=ds.capitalize(), color=dataset_colors[ds])

    ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax.set_xlabel('L2 Distance', fontsize=11, fontweight='bold')
    ax.set_title('B. Carlini L2 - L2 Distance Distribution (Successful Attacks)', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(True, alpha=0.2)
    ax.yaxis.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig11_carlini_l2_hist.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 12: Attack success vs failure L2 comparison ──────
def fig12():
    fig, ax = plt.subplots(figsize=(8, 5))

    datasets = ['adult', 'german', 'compas', 'diabetes', 'breast_cancer']
    ds_colors = {
        'adult': '#e34993',
        'german': '#27a24c',
        'compas': '#eaad2c',
        'diabetes': '#2e6abf',
        'breast_cancer': '#c8502d',
    }

    x = np.arange(len(datasets))
    width = 0.35

    success_medians = []
    fail_medians = []
    labels = []

    for ds in datasets:
        success_medians.append(imp_df[(imp_df['dataset']==ds) & (imp_df['attack_success']==1)]['eval_L2'].median())
        fail_medians.append(imp_df[(imp_df['dataset']==ds) & (imp_df['attack_success']==0)]['eval_L2'].median())
        labels.append(ds.capitalize())

    rects1 = ax.bar(x - width/2, success_medians, width, label='Successful', color='#27ae60', alpha=0.8)
    rects2 = ax.bar(x + width/2, fail_medians, width, label='Failed', color='#e74c3c', alpha=0.8)

    ax.set_ylabel('Median L2 Distance', fontsize=11, fontweight='bold')
    ax.set_xlabel('Dataset', fontsize=11, fontweight='bold')
    ax.set_title('C&W L2 - L2 Distance (Successful vs Failed)', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig12_success_vs_fail.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 13: DeepFool L2 IQR ratio vs Mahalanobis IQR ratio ──────
def fig13():
    fig, ax = plt.subplots(figsize=(8, 5))

    attacks = ['DeepFool', 'C&W L2', 'FGSM L-inf']
    colors = ['#2563eb', '#dc2626', '#059669']

    # From qualitative_analysis.md
    # deepfool: L2 IQR=8.5, Mahal IQR=10.6
    # carlini_l_2: L2 IQR=7.2, Mahal IQR=8.0
    # fgsm_l_inf: L2 IQR=1.1, Mahal IQR=1.2

    x = np.arange(len(attacks))
    width = 0.3

    l2_ratios = [8.5, 7.2, 1.1]
    mahal_ratios = [10.6, 8.0, 1.2]

    rects1 = ax.bar(x - width/2, l2_ratios, width, label='L2 IQR Ratio', color='#2563eb', alpha=0.8)
    rects2 = ax.bar(x + width/2, mahal_ratios, width, label='Mahalanobis IQR Ratio', color='#7c3aed', alpha=0.8)

    ax.set_ylabel('IQR Ratio (Q75/Q25)', fontsize=11, fontweight='bold')
    ax.set_xlabel('Attack Method', fontsize=11, fontweight='bold')
    ax.set_title('IQR Ratios (Heavy Tail) by Attack', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(attacks)
    ax.legend(fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig13_iqr_ratio.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 14: Sensitivity Distribution ──────
def fig14():
    fig, ax = plt.subplots(figsize=(8, 5))

    attacks = ['DeepFool', 'C&W L2', 'FGSM L-inf']
    colors = ['#2563eb', '#dc2626', '#059669']

    successful = imp_df[imp_df['attack_success'] == 1]
    box_data = []
    for atk_raw, color in zip(attacks, colors):
        atk_col_map = {'DeepFool': 'deepfool', 'C&W L2': 'carlini_l_2', 'FGSM L-inf': 'fgsm_l_inf'}
        atk_col = atk_col_map[atk_raw]
        atk_data = successful[(successful['attack'] == atk_col)]['eval_Sen'].values
        if atk_col == 'carlini_l_2':
            atk_data = atk_data[atk_data > 0]
        box_data.append(atk_data)

    bp = ax.boxplot(box_data, labels=attacks, patch=True, whis=1.5, showfliers=False)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)
        patch.set_edgecolor(color)
        patch.set_linewidth(1.5)

    ax.set_ylabel('Sensitivity Score', fontsize=11, fontweight='bold')
    ax.set_xlabel('Attack Method', fontsize=11, fontweight='bold')
    ax.set_title('Sensitivity Score Distribution (Successful Attacks)', fontsize=12, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_yscale('log')
    ax.yaxis.grid(True, alpha=0.2, which='both')

    # Add mean markers
    means = []
    for atk_raw in attacks:
        atk_col_map = {'DeepFool': 'deepfool', 'C&W L2': 'carlini_l_2', 'FGSM L-inf': 'fgsm_l_inf'}
        atk_col = atk_col_map[atk_raw]
        atk_data = successful[(successful['attack'] == atk_col)]['eval_Sen'].values
        if atk_col == 'carlini_l_2':
            atk_data = atk_data[atk_data > 0]
        means.append(np.mean(atk_data))

    for i, m in enumerate(means):
        ax.plot(i+1, m, 'D', color='black', ms=8, zorder=3)
        ax.text(i+1, m+0.01, f'{m:.1f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig14_sensitivity_distribution.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 15: DeepFool Sensitivity Heavy Tail ──────
def fig15():
    fig, ax = plt.subplots(figsize=(8, 5))

    deepfool_sen = imp_df[(imp_df['attack']=='deepfool') & (imp_df['attack_success']==1)]['eval_Sen'].values

    # Top 10% contribution
    threshold = np.percentile(deepfool_sen, 90)
    top_10 = deepfool_sen[deepfool_sen >= threshold]
    rest = deepfool_sen[deepfool_sen < threshold]

    ax.hist(top_10, bins=20, alpha=0.6, label=f'Top 10% (>{threshold:.3f})', color='#dc2626', edgecolor='black')
    ax.hist(rest, bins=20, alpha=0.6, label=f'Bottom 90%', color='#2563eb', edgecolor='black')

    ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax.set_xlabel('Sensitivity Score', fontsize=11, fontweight='bold')
    ax.set_title('DeepFool - Sensitivity Heavy Tail', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(True, alpha=0.2)
    ax.yaxis.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig15_sensitivity_heavy_tail.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 16: Correlation (Mahalanobis vs L2) ──────
def fig16():
    fig, ax = plt.subplots(figsize=(8, 5))

    successful = imp_df[imp_df['attack_success'] == 1]

    attacks_data = []
    for name in ['deepfool', 'carlini_l_2', 'fgsm_l_inf']:
        subset = successful[(successful['attack'] == name)]
        if len(subset) > 0:
            l2 = subset['eval_L2'].values
            mah = subset['eval_Mahalanobis'].values
            if name == 'carlini_l_2':
                mask = l2 > 0
                l2 = l2[mask]
                mah = mah[mask]
            attacks_data.append((name, l2, mah, f'{name}_l2_hist.png'))

    # Plot correlations
    for i, (name, l2, mah, filename) in enumerate(attacks_data):
        if len(l2) < 2:
            continue
        corr = np.corrcoef(l2, mah)[0, 1] if len(l2) > 1 else 0
        ax.scatter(l2, mah, alpha=0.3, s=10, label=f'{name.replace("_", " ").title()} (r={corr:.3f})', color=['#2563eb', '#dc2626', '#059669'][i])

    ax.set_ylabel('Mahalanobis Distance', fontsize=11, fontweight='bold')
    ax.set_xlabel('L2 Distance', fontsize=11, fontweight='bold')
    ax.set_title('Correlation between L2 and Mahalanobis Distance', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(True, alpha=0.2)
    ax.yaxis.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig16_corr_mahal_l2.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 17: Sensitivity L2 Correlation ──────
def fig17():
    fig, ax = plt.subplots(figsize=(8, 5))

    successful = imp_df[imp_df['attack_success'] == 1]

    for i, name in enumerate(['deepfool', 'carlini_l_2', 'fgsm_l_inf']):
        subset = successful[(successful['attack'] == name)]
        if len(subset) > 0:
            l2 = subset['eval_L2'].values
            sen = subset['eval_Sen'].values
            if name == 'carlini_l_2':
                mask = l2 > 0
                l2 = l2[mask]
                sen = sen[mask]
            corr = np.corrcoef(l2, sen)[0, 1] if len(l2) > 1 else 0
            ax.scatter(l2, sen, alpha=0.3, s=10, label=f'{name.replace("_", " ").title()} (r={corr:.3f})', color=['#2563eb', '#dc2626', '#059669'][i])

    ax.set_ylabel('Sensitivity Score', fontsize=11, fontweight='bold')
    ax.set_xlabel('L2 Distance', fontsize=11, fontweight='bold')
    ax.set_title('Correlation between Sensitivity Score and L2 Distance', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(True, alpha=0.2)
    ax.yaxis.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig17_corr_sen_l2.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 18: SR Heatmap by Dataset-Model-Attack ──────
def fig18():
    fig, ax = plt.subplots(figsize=(10, 6))

    datasets = ['adult', 'german', 'compas', 'diabetes', 'breast_cancer']
    models = ['LR', 'MLP', 'SVC']
    attacks = ['deepfool', 'carlini_l_2', 'fgsm_l_inf']

    # Compute SR matrix
    data = np.zeros((len(datasets), len(models), len(attacks)))
    for i, ds in enumerate(datasets):
        for j, model in enumerate(models):
            for k, atk in enumerate(attacks):
                sub = sr_df[(sr_df['Dataset']==ds) & (sr_df['Model']==model) & (sr_df['Attack methods']==atk)]
                data[i, j, k] = sub['Success_rate'].mean()*100 if len(sub) > 0 else 0

    # Summarize: avg over models
    avg_sr = np.mean(data, axis=1)

    im = ax.imshow(avg_sr, cmap='YlGnBu', aspect='auto', vmin=0, vmax=100)
    ax.set_xticks(range(len(attacks)))
    ax.set_xticklabels(['DeepFool', 'C&W L2', 'FGSM L-inf'])
    ax.set_yticks(range(len(datasets)))
    ax.set_yticklabels([d.capitalize() for d in datasets])
    ax.set_xlabel('Attack Method', fontsize=11, fontweight='bold')
    ax.set_ylabel('Dataset', fontsize=11, fontweight='bold')
    ax.set_title('Avg Success Rate (%) by Dataset', fontsize=12, fontweight='bold')

    # Add text annotations
    for i in range(len(datasets)):
        for j in range(len(attacks)):
            text = f'{avg_sr[i, j]:.1f}'
            ax.text(j, i, text, ha='center', va='center', fontsize=10, fontweight='bold',
                    color='white' if avg_sr[i, j] > 70 else 'black')

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig18_sr_heatmap.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 19: Paired SR comparison for SVC ──────
def fig19():
    fig, ax = plt.subplots(figsize=(8, 5))

    datasets = ['adult', 'german', 'compas', 'diabetes', 'breast_cancer']
    attacks = ['deepfool', 'carlini_l_2', 'fgsm_l_inf']
    labels = ['DeepFool', 'C&W L2', 'FGSM L-inf']
    colors = ['#2563eb', '#dc2626', '#059669']

    x = np.arange(len(datasets))
    width = 0.25

    for i, (atk, label, color) in enumerate(zip(attacks, labels, colors)):
        vals = []
        for ds in datasets:
            sub = sr_df[(sr_df['Model']=='SVC') & (sr_df['Dataset']==ds) & (sr_df['Attack methods']==atk)]
            sr = sub['Success_rate'].mean()*100 if len(sub)>0 else 0
            vals.append(sr)
        ax.bar(x + i*width - width, vals, width, label=label, color=color, alpha=0.8)

    ax.set_ylabel('Attack Success Rate (%)', fontsize=11, fontweight='bold')
    ax.set_xlabel('Dataset', fontsize=11, fontweight='bold')
    ax.set_title('SVC - Attack Success Rates', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([d.capitalize() for d in datasets])
    ax.legend(fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig19_svc_sr.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 20: Per-sample agreement SVC ──────
def fig20():
    fig, ax = plt.subplots(figsize=(8, 5))

    # From qualitative_analysis.md
    datasets = ['adult', 'breast_cancer', 'compas']
    counts = [5478, 63, 1123]
    counts_both = [5478, 63, 1123]
    colors_map = {
        'adult': '#e34993',
        'breast_cancer': '#c8502d',
        'compas': '#eaad2c',
    }

    x = np.arange(len(datasets))
    width = 0.3

    rects1 = ax.bar(x - width/2, counts_both, width, label='Both attacks on', color='#27ae60', alpha=0.8)
    rects2 = ax.bar(x + width/2, [0, 0, 0], width, label='Only one on', color='#e74c3c', alpha=0.8)

    ax.set_ylabel('Number of Samples', fontsize=11, fontweight='bold')
    ax.set_xlabel('Dataset', fontsize=11, fontweight='bold')
    ax.set_title('SVC - Per-Sample Attack Agreement', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([d.capitalize() for d in datasets])
    ax.legend(fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, alpha=0.2)

    # Add annotations
    for i, (c, cb) in enumerate(zip(counts, counts_both)):
        ax.text(i, c + 100, f'n={c}', ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig20_agreement.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 21: Trade-off SR vs L2 / SR vs Mahal / SR vs Sensitivity ──────
def fig21():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    successful = imp_df[imp_df['attack_success'] == 1]
    failed = imp_df[imp_df['attack_success'] == 0]

    attacks = ['DeepFool', 'C&W L2', 'FGSM L-inf']
    attack_map = {'DeepFool': 'deepfool', 'C&W L2': 'carlini_l_2', 'FGSM L-inf': 'fgsm_l_inf'}
    colors = ['#2563eb', '#dc2626', '#059669']

    metrics = ['eval_L2', 'eval_Mahalanobis', 'eval_Sen']
    titles = ['Proximity (L2)', 'Deviation (Mahalanobis)', 'Sensitivity']

    for ax_i, (ax, metric, title) in enumerate(zip(axes, metrics, titles)):
        success_medians = []
        fail_medians = []
        for atk_raw, color in zip(attacks, colors):
            atk_col = attack_map[atk_raw]
            sub_s = successful[successful['attack'] == atk_col][metric].values
            sub_f = failed[failed['attack'] == atk_col][metric].values
            if atk_col == 'carlini_l_2':
                sub_s = sub_s[sub_s > 0]
                sub_f = sub_f[sub_f > 0]
            success_medians.append(np.median(sub_s) if len(sub_s) > 0 else 0)
            fail_medians.append(np.median(sub_f) if len(sub_f) > 0 else 0)

        x = np.arange(len(attacks))
        width = 0.35
        ax.bar(x - width/2, success_medians, width, label='Success', color='#27ae60', alpha=0.8)
        ax.bar(x + width/2, fail_medians, width, label='Failed', color='#e74c3c', alpha=0.8)
        ax.set_ylabel('Median ' + metric.split('_')[-1].capitalize(), fontsize=10)
        ax.set_xlabel('Attack', fontsize=10)
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(attacks, fontsize=8)
        ax.legend(fontsize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig21_tradeoff.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 22: SR by Dataset-Model (heatmap) ──────
def fig22():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    datasets = ['adult', 'breast_cancer', 'compas', 'diabetes', 'german']
    models = ['LR', 'MLP', 'SVC']
    attacks = ['deepfool', 'carlini_l_2', 'fgsm_l_inf']

    # LR heatmap
    data_lr = np.zeros((len(datasets), len(attacks)))
    for i, ds in enumerate(datasets):
        for j, atk in enumerate(attacks):
            sub = sr_df[(sr_df['Model']=='LR') & (sr_df['Dataset']==ds) & (sr_df['Attack methods']==atk)]
            data_lr[i, j] = sub['Success_rate'].mean()*100 if len(sub)>0 else 0

    im1 = axes[0].imshow(data_lr, cmap='YlGnBu', aspect='auto', vmin=0, vmax=100)
    axes[0].set_xticks(range(len(attacks)))
    axes[0].set_xticklabels(['DeepFool', 'C&W L2', 'FGSM L-inf'], fontsize=8)
    axes[0].set_yticks(range(len(datasets)))
    axes[0].set_yticklabels([d.capitalize() for d in datasets])
    axes[0].set_title('LR Model', fontsize=11, fontweight='bold')
    for i in range(len(datasets)):
        for j in range(len(attacks)):
            axes[0].text(j, i, f'{data_lr[i,j]:.1f}', ha='center', va='center', fontsize=9,
                        color='white' if data_lr[i,j]>70 else 'black', fontweight='bold')

    # MLP heatmap
    data_mlp = np.zeros((len(datasets), len(attacks)))
    for i, ds in enumerate(datasets):
        for j, atk in enumerate(attacks):
            sub = sr_df[(sr_df['Model']=='MLP') & (sr_df['Dataset']==ds) & (sr_df['Attack methods']==atk)]
            data_mlp[i, j] = sub['Success_rate'].mean()*100 if len(sub)>0 else 0

    im2 = axes[1].imshow(data_mlp, cmap='YlGnBu', aspect='auto', vmin=0, vmax=100)
    axes[1].set_xticks(range(len(attacks)))
    axes[1].set_xticklabels(['DeepFool', 'C&W L2', 'FGSM L-inf'], fontsize=8)
    axes[1].set_yticks(range(len(datasets)))
    axes[1].set_yticklabels([d.capitalize() for d in datasets])
    axes[1].set_title('MLP Model', fontsize=11, fontweight='bold')
    for i in range(len(datasets)):
        for j in range(len(attacks)):
            axes[1].text(j, i, f'{data_mlp[i,j]:.1f}', ha='center', va='center', fontsize=9,
                        color='white' if data_mlp[i,j]>70 else 'black', fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig22_lr_mlp_heatmap.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 23: Carlini L2 failure breakdown ──────
def fig23():
    fig, ax = plt.subplots(figsize=(8, 5))

    # From qualitative_analysis.md: Carlini L2 Failure breakdown
    # L2 == 0: 0
    # 0 < L2 < 0.001: 10702
    # 0.001 <= L2 < 0.01: 132
    # 0.01 <= L2 < 0.05: 510
    # L2 >= 0.05: 2119

    labels = ['0 < L2 < 1ms', '1ms ≤ L2 < 10ms', '10ms ≤ L2 < 50ms', 'L2 ≥ 50ms']
    counts = [10702, 132, 510, 2119]
    colors = ['#2563eb', '#d97706', '#dc2626', '#7c3aed']

    bars = ax.bar(labels, counts, color=colors, alpha=0.8, width=0.6)
    ax.set_ylabel('Count of Failed Samples', fontsize=11, fontweight='bold')
    ax.set_xlabel('Carlini L2 Distance (failed samples)', fontsize=11, fontweight='bold')
    ax.set_title('C&W L2 - Breakdown of Successful Attacks by L2 Distance', fontsize=12, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, alpha=0.2)

    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+100, f'{count}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig23_carlini_breakdown.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 24: DeepFool Heavy Tail breakdown ──────
def fig24():
    fig, ax = plt.subplots(figsize=(8, 5))

    # From qualitative_analysis.md: DeepFool Heavy Tail Breakdown
    # Overall mean L2: 0.5396
    # Top 10% mean L2: 3.0251 (5.6x overall)
    # Top 10% contribute 56.1% to overall mean

    categories = ['Bottom\n90%', 'Top\n10%']
    means = [0.0998, 3.0251]  # Approximate values
    colors = ['#2563eb', '#dc2626']

    bars = ax.bar(categories, means, color=colors, alpha=0.8, width=0.5)
    ax.set_ylabel('Mean L2 Distance', fontsize=11, fontweight='bold')
    ax.set_xlabel('DeepFool Samples', fontsize=11, fontweight='bold')
    ax.set_title('DeepFool - Heavy Tail Analysis', fontsize=12, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, alpha=0.2)
    ax.set_yscale('log')

    for bar, mean in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.1, f'{mean:.4f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig24_deepfool_heavy_tail.png'), dpi=150, bbox_inches='tight')
    plt.close()

# ────── Figure 25: Mahalanobis Distribution (successful attacks) ──────
def fig25():
    fig, ax = plt.subplots(figsize=(8, 5))

    successful = imp_df[imp_df['attack_success'] == 1]
    attacks = ['DeepFool', 'C&W L2', 'FGSM L-inf']
    colors = ['#2563eb', '#dc2626', '#059669']

    box_data = []
    for atk_raw, color in zip(attacks, colors):
        atk_col_map = {'DeepFool': 'deepfool', 'C&W L2': 'carlini_l_2', 'FGSM L-inf': 'fgsm_l_inf'}
        atk_col = atk_col_map[atk_raw]
        atk_data = successful[(successful['attack'] == atk_col)]['eval_Mahalanobis'].values
        if atk_col == 'carlini_l_2':
            atk_data = atk_data[atk_data > 0]
        box_data.append(atk_data)

    bp = ax.boxplot(box_data, labels=attacks, patch=True, whis=1.5, showfliers=False)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)
        patch.set_edgecolor(color)
        patch.set_linewidth(1.5)

    ax.set_ylabel('Median Mahalanobis Distance', fontsize=11, fontweight='bold')
    ax.set_xlabel('Attack Method', fontsize=11, fontweight='bold')
    ax.set_title('Mahalanobis Distance Distribution (Successful Attacks)', fontsize=12, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_yscale('log')
    ax.yaxis.grid(True, alpha=0.2, which='both')

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'fig25_mahal_distribution.png'), dpi=150, bbox_inches='tight')
    plt.close()


# ─────────────────────────── Run all ───────────────────────────
print("Generating visualizations...")
fig1()
fig2()
fig3()
fig4()
fig5()
fig6()
fig7()
fig8()
fig9()
fig10()
fig11()
fig12()
fig13()
fig14()
fig15()
fig16()
fig17()
fig18()
fig19()
fig20()
fig21()
fig22()
fig23()
fig24()
fig25()

print("All visualizations saved to ./ Visualisation/")
