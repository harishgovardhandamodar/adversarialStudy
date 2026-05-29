import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
from scipy.ndimage import gaussian_filter1d

DATA_DIR = '.'
FIG_DIR = os.path.join(DATA_DIR, 'report_figures')
os.makedirs(FIG_DIR, exist_ok=True)

imp_df = pd.read_csv(os.path.join(DATA_DIR, 'all_imp.csv'))
sr_df = pd.read_csv(os.path.join(DATA_DIR, 'success_rate.csv'))

ATTACK_MAP = {'deepfool': 'DeepFool', 'carlini_l_2': 'Carlini L2', 'fgsm_l_inf': 'FGSM Linf'}
DATASET_MAP = {'adult': 'Adult', 'german': 'German', 'compas': 'COMPAS', 
               'diabetes': 'Diabetes', 'breast_cancer': 'Breast Cancer'}
C_ATTACK = {'DeepFool': '#4e79a7', 'Carlini L2': '#f28027', 'FGSM Linf': '#59a14f'}
C_MODEL  = {'LR':  '#4e79a7', 'MLP': '#f28027', 'SVC': '#e15759'}

plt.rcParams.update({
    'figure.figsize': (10, 6), 'font.size': 10, 'axes.titlesize': 12,
    'axes.labelsize': 11, 'savefig.dpi': 200, 'savefig.bbox': 'tight',
    'axes.spines.top': False, 'axes.spines.right': False,
})

def get_sub(model=None, dataset=None, attack=None, success=True):
    m = imp_df['attack_success'] == 1 if success else imp_df['attack_success'] == 0
    if model: m = m & (imp_df['model'] == model)
    if dataset: m = m & (imp_df['dataset'] == dataset)
    if attack: m = m & (imp_df['attack'] == attack)
    return imp_df[m]

# === FIG 1: Distribution Comparison ===
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
titles = ['L2 Distance', 'Sensitivity', 'Mahalanobis Distance']
cols = ['eval_L2', 'eval_Sen', 'eval_Mahalanobis']

for i in range(3):
    for att_name, clr in C_ATTACK.items():
        sub = get_sub(attack=att_name)
        if len(sub) == 0: continue
        vals = sub[cols[i]].values
        bins = np.linspace(vals.min() + 1e-6, vals.max(), 80)
        hist, edges = np.histogram(vals, bins=bins)
        kde = gaussian_filter1d(hist.astype(float), sigma=2.0)
        scale = (edges[1] - edges[0]) * np.sum(hist)
        kde /= scale
        axes[i].plot((edges[:-1]+edges[1:])/2, kde, label=att_name, linewidth=2, color=clr)
    
    axes[i].set_xscale('log')
    axes[i].set_yscale('log')
    axes[i].set_title(titles[i], fontweight='bold')
    axes[i].set_xlabel('Value', fontsize=10)
    if i == 0:
        axes[i].set_ylabel('Density', fontsize=10)
    axes[i].grid(True, alpha=0.2)

axes[0].legend(fontsize=9, loc='upper left', frameon=False)
fig.suptitle('Attack Metric Distributions (Successful Attacks Only)', fontsize=13, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, '01_distributions.png'))
plt.close()
print('Saved: 01_distributions.png')

# === FIG 2: Success Rate Heatmap ===
fig, ax = plt.subplots(figsize=(8, 5))
attacks_plot = list(ATTACK_MAP.values())
datasets_plot = list(DATASET_MAP.values())
data = np.zeros((5, 3))

for d_idx, d in enumerate(datasets_plot):
    for a_idx, att in enumerate(ATTACK_MAP.keys()):
        sub = imp_df[(imp_df['attack'] == att) & (imp_df['dataset'] == d)]
        data[d_idx, a_idx] = sub['attack_success'].mean() * 100 if len(sub) > 0 else 0

im = ax.imshow(data, cmap='YlOrRd', aspect='auto', vmin=0, vmax=100)
ax.set_xticks(range(3))
ax.set_yticks(range(5))
ax.set_xticklabels(attacks_plot)
ax.set_yticklabels(datasets_plot)

for i in range(5):
    for j in range(3):
        val = data[i, j]
        ax.text(j, i, f'{val:.0f}%', ha='center', va='center',
                fontsize=11, fontweight='bold',
                color='white' if val > 60 else 'black')

cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('Success Rate (%)', fontsize=11)
ax.set_title('Attack Effectiveness by Dataset', fontweight='bold', fontsize=13, pad=10)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, '02_sr_heatmap.png'))
plt.close()
print('Saved: 02_sr_heatmap.png')

# === FIG 3: Model robustness + L2 box ===
fig = plt.figure(figsize=(14, 5))
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])

# Left: SR per model
ax1 = fig.add_subplot(gs[0])
models = list(C_MODEL.keys())
for att_name, clr in C_ATTACK.items():
    srs = []
    for m in models:
        sub = get_sub(model=m, attack=att_name)
        srs.append(sub['attack_success'].mean() * 100 if len(sub) > 0 else 0)
    ax1.plot(range(3), srs, 'o-', label=att_name, linewidth=2, markersize=8, color=clr)

ax1.set_xticks(range(3))
ax1.set_xticklabels(models)
ax1.set_ylim(0, 105)
ax1.set_ylabel('Success Rate (%)', fontweight='bold')
ax1.set_title('Model Vulnerability to Each Attack', fontweight='bold', fontsize=12)
ax1.grid(True, alpha=0.2)
ax1.legend(fontsize=9)

# Right: L2 boxplot by attack x model
ax2 = fig.add_subplot(gs[1])
attacks_for_box = ['deepfool', 'carlini_l_2', 'fgsm_l_inf']
labels_for_box = ['DeepFool', 'Carlini L2', 'FGSM Linf']
colors_for_box = [C_ATTACK[ATTACK_MAP[k]] for k in ATTACK_MAP]

data_by_attack = []
for att in attacks_for_box:
    sub = get_sub(attack=att)
    data_by_attack.append(sub['eval_L2'].values)

bp = ax2.boxplot(data_by_attack, tick_labels=labels_for_box, patch_artist=True)
for patch, clr in zip(bp['boxes'], colors_for_box):
    patch.set_facecolor(clr)
    patch.set_alpha(0.6)
ax2.set_yscale('log')
ax2.set_ylabel('L2 Distance', fontweight='bold')
ax2.set_title('L2 Distance Distributions by Attack', fontweight='bold', fontsize=12)
ax2.grid(True, alpha=0.2)

fig.suptitle('Model Robustness & Attack Magnitude', fontsize=13, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, '03_model_vulnerability.png'))
plt.close()
print('Saved: 03_model_vulnerability.png')

# === FIG 4: Per-dataset success rates ===
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(5)
width = 0.25

bars_all = []
for att_idx, att in enumerate(ATTACK_MAP.keys()):
    srs = [get_sub(attack=att, dataset=d)['attack_success'].mean() * 100 
           if len(get_sub(attack=att, dataset=d)) > 0 else 0 for d in ['adult','german','compas','diabetes','breast_cancer']]
    bars = ax.bar(x + (att_idx - 1) * width, srs, width, label=ATTACK_MAP[att],
                  color=C_ATTACK[ATTACK_MAP[att]], alpha=0.85, edgecolor='white', linewidth=0.5)
    bars_all.append(bars)

ax.set_xticks(x)
ax.set_xticklabels([DATASET_MAP[d] for d in ['adult','german','compas','diabetes','breast_cancer']], rotation=30, ha='right')
ax.set_ylabel('Success Rate (%)', fontweight='bold')
ax.set_ylim(0, 110)
ax.set_title('Dataset-Level Attack Success Rates', fontweight='bold', fontsize=12)
ax.grid(True, alpha=0.2, axis='y')
ax.legend(fontsize=9)

# Add median line
for bar_group in range(5):
    medians = [bars_all[i][bar_group].get_height() for i in range(3)]
    med_val = np.median(medians)
    ax.plot(x[bar_group] - width, med_val, 's', color='red', markersize=6)
ax.plot([], [], 's', color='red', markersize=6, label='Median SR')
ax.legend(fontsize=9)

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, '04_dataset_sr.png'))
plt.close()
print('Saved: 04_dataset_sr.png')

# === FIG 5: The Imperceptibility Paradox (LR/adult) ===
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

title_text = 'The Imperceptibility Paradox'
subtitle_text = 'Large imperceptible perturbations can yield higher success than tiny ones'
ax.text(0.5, 0.95, title_text, fontsize=16, fontweight='bold', ha='center', va='top',
        transform=ax.transAxes, color='#1a1a1a')
ax.text(0.5, 0.90, subtitle_text, fontsize=11, ha='center', va='top', transform=ax.transAxes,
        style='italic', color='#666')

# LR/adult comparison
lr_adult_deepfool = get_sub(model='LR', dataset='adult', attack='deepfool')
lr_adult_carlini = get_sub(model='LR', dataset='adult', attack='carlini_l_2')
lr_adult_fgsm = get_sub(model='LR', dataset='adult', attack='fgsm_l_inf')

def make_comparison(y, sub_df, label_name, clr):
    sr = sub_df['attack_success'].mean() * 100
    med_l2 = np.median(sub_df['eval_L2'])
    min_l2 = sub_df['eval_L2'].min()
    mean_mahal = sub_df['eval_Mahalanobis'].mean()
    
    # Draw horizontal bar
    ax.barh(y, sr/100.0, height=0.06, left=0.05, color=clr, alpha=0.5)
    
    ax.text(0.04, y + 0.03, f'{label_name}:', fontsize=10, fontweight='bold',
            ha='right', va='center', transform=ax.transAxes, color=clr)
    ax.text(0.07, y + 0.03, f'SR={sr:.1f}%', fontsize=9, ha='left', va='center',
            transform=ax.transAxes, color=clr, fontweight='bold')
    ax.text(0.35, y + 0.03, f'MedL2={med_l2:.4f}', fontsize=9, ha='left', va='center',
            transform=ax.transAxes, color=clr, fontweight='bold')
    ax.text(0.57, y + 0.03, f'MeanMahal={mean_mahal:.2f}', fontsize=9, ha='left', va='center',
            transform=ax.transAxes, color=clr, fontweight='bold')

y_pos = 0.72
make_comparison(y_pos, lr_adult_deepfool, 'DeepFool', C_ATTACK['DeepFool'])
y_pos -= 0.09
make_comparison(y_pos, lr_adult_carlini, 'Carlini L2', C_ATTACK['Carlini L2'])
y_pos -= 0.09
make_comparison(y_pos, lr_adult_fgsm, 'FGSM Linf', C_ATTACK['FGSM Linf'])

# Add note
note = 'Carlini L2 achieves high success with much smaller median perturbation'
ax.text(0.5, 0.35, note, fontsize=10, ha='center', va='top', transform=ax.transAxes,
        color='#333', fontweight='bold', style='italic')

# Add arrows
from matplotlib.patches import FancyArrowPatch
arrow1 = FancyArrowPatch((0.35, 0.68), (0.35, 0.60),
                        transform=ax.transAxes, arrowstyle='->', mutation_scale=12,
                        linewidth=1.5, color='#999')
ax.add_patch(arrow1)

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, '05_imperceptibility_paradox.png'))
plt.close()
print('Saved: 05_imperceptibility_paradox.png')

# === FIG 6: SVC Carlini resistance ===
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: L2 histogram for SVC+Carlini (failed)
sub_carlini_svc = get_sub(model='SVC', attack='carlini_l_2')
fail = sub_carlini_svc[sub_carlini_svc['attack_success'] == 0]
axes[0].hist(fail['eval_L2'].values, bins=100, color=C_ATTACK['Carlini L2'], alpha=0.8,
             edgecolor='white', linewidth=0.3)
axes[0].set_xscale('log')
axes[0].set_yscale('log')
axes[0].set_xlabel('L2 Distance', fontweight='bold')
axes[0].set_ylabel('Count (log scale)', fontweight='bold')
axes[0].set_xticks([1e-4, 1e-3, 1e-2, 1e-1, 1])
axes[0].set_title('Failed Carlini Attacks (SVC)\nL2 Distribution', fontweight='bold', fontsize=11)
axes[0].grid(True, alpha=0.2)

# Right: Success rate by L2 bins
l2_bins = [0, 0.001, 0.01, 0.1, 1.0]
axis_x = []
axis_y = []
for i in range(len(l2_bins)-1):
    mask = (sub_carlini_svc['eval_L2'] >= l2_bins[i]) & (sub_carlini_svc['eval_L2'] < l2_bins[i+1])
    sub_bin = sub_carlini_svc[mask]
    if len(sub_bin) > 0:
        axis_x.append((l2_bins[i] + l2_bins[i+1])/2)
        axis_y.append(sub_bin['attack_success'].mean() * 100)

axes[1].plot(axis_x, axis_y, 'o-', color=C_ATTACK['Carlini L2'], linewidth=2, markersize=8)
axes[1].set_xscale('log')
axes[1].set_yscale('log')
axes[1].set_xlabel('L2 Distance (bins)', fontweight='bold')
axes[1].set_ylabel('Success Rate (%)', fontweight='bold')
axes[1].set_title('Carlini Success Rate vs. L2 (SVC)', fontweight='bold', fontsize=11)
axes[1].grid(True, alpha=0.3)
axes[1].set_ylim(5, 110)

fig.suptitle('SVC Resistance to Carlini Adversarial Attack', fontsize=13, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, '06_svc_carlini_resistance.png'))
plt.close()
print('Saved: 06_svc_carlini_resistance.png')

# === FIG 7: Model x Attack SR ===
fig, ax = plt.subplots(figsize=(10, 7))
global_sr = []
for m in ['LR', 'MLP', 'SVC']:
    for att in ATTACK_MAP.keys():
        sub = get_sub(model=m, attack=att)
        global_sr.append([m, ATTACK_MAP[att], sub['attack_success'].mean() * 100 if len(sub) > 0 else 0])

sr_pd = pd.DataFrame(global_sr, columns=['Model', 'Attack', 'SR'])
for m in ['LR', 'MLP', 'SVC']:
    mask = sr_pd['Model'] == m
    ax.scatter(sr_pd.loc[mask, 'Attack'], sr_pd.loc[mask, 'SR'],
              c=C_MODEL[m], s=200, alpha=0.7, edgecolors='white', linewidth=1.5)
    ax.plot(sr_pd.loc[mask, 'Attack'], sr_pd.loc[mask, 'SR'], 'o-', color=C_MODEL[m], linewidth=2)
    for _, row in sr_pd[mask].iterrows():
        ax.text(row['Attack'], row['SR']+3, f'{row["SR"]:.0f}%', ha='center', va='bottom',
                fontsize=9, fontweight='bold', color=C_MODEL[m])

ax.set_ylim(0, 105)
ax.set_ylabel('Success Rate (%)', fontweight='bold')
ax.set_title('Global Model Vulnerability by Attack Method', fontweight='bold', fontsize=13)
ax.grid(True, alpha=0.2)
ax.legend(['LR', 'MLP', 'SVC'], title='Model', fontsize=10)

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, '07_global_model_vulnerability.png'))
plt.close()
print('Saved: 07_global_model_vulnerability.png')

print('All figures saved successfully!')