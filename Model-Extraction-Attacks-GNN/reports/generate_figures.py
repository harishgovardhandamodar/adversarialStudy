#!/usr/bin/env python3
"""
Figure generation script for the Comprehensive Model Extraction Attacks on GNNs Report.
Generates all figures saved in the ./figures/ directory.
"""

import os
import sys
import numpy as np
import networkx as nx
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch
import seaborn as sns

sns.set_style('whitegrid')
sns.set_context('poster', font_scale=1.6)

FIGURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
os.makedirs(FIGURE_DIR, exist_ok=True)

np.random.seed(42)

ATTACK_DATA = [
    {"id": 0, "attr": "Partial", "struct": "Partial",   "shadow": False, "knowledge": "Low/Medium", "mean": 0.52, "std": 0.04},
    {"id": 1, "attr": "Partial", "struct": "Unknown",   "shadow": False, "knowledge": "Low",        "mean": 0.47, "std": 0.05},
    {"id": 2, "attr": "Unknown", "struct": "Known",     "shadow": False, "knowledge": "Medium",       "mean": 0.62, "std": 0.05},
    {"id": 3, "attr": "Unknown", "struct": "Unknown",   "shadow": True,  "knowledge": "Medium",       "mean": 0.58, "std": 0.06},
    {"id": 4, "attr": "Partial", "struct": "Partial",   "shadow": True,  "knowledge": "High",         "mean": 0.78, "std": 0.03},
    {"id": 5, "attr": "Partial", "struct": "Unknown",   "shadow": True,  "knowledge": "Medium",       "mean": 0.67, "std": 0.04},
    {"id": 6, "attr": "Unknown", "struct": "Known",     "shadow": True,  "knowledge": "High",         "mean": 0.83, "std": 0.02},
]

KNOWLEDGE_COLORS = {"Low": "#ffd43b", "Low/Medium": "#4ecdc4", "Medium": "#69db7c", "High": "#74c0fc"}
COLORS = ['#ff6b6b', '#ffa94d', '#ffd43b', '#69db7c', '#4ecdc4', '#74c0fc', '#b197fc']

GLOBAL_G = nx.barabasi_albert_graph(10, 3)
GLOBAL_POS = nx.spring_layout(GLOBAL_G, seed=42)


def make_figure_1():
    """Figure 1: Attack Taxonomy Grid"""
    fig = plt.figure(figsize=(20, 10))
    gs = GridSpec(2, 4, figure=fig, hspace=0.55, wspace=0.45)

    for idx, atk in enumerate(ATTACK_DATA):
        row = idx // 4
        col = idx % 4
        ax = fig.add_subplot(gs[row, col])
        ax.set_xlim(-0.5, 3.5)
        ax.set_ylim(-0.5, 2.5)
        ax.axis('off')

        n = 8
        G = nx.barabasi_albert_graph(n, 2)
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, ax=ax, node_color=COLORS[idx], node_size=250,
                with_labels=False, edge_color='black', alpha=0.25, width=1.0)

        bc = KNOWLEDGE_COLORS[atk['knowledge']]
        ax.text(1.5, -0.3, f"{atk['knowledge']} Knowledge", ha='center', fontsize=14,
                bbox=dict(boxstyle='round,pad=0.35', facecolor=bc, edgecolor='gray', alpha=0.7))

        txty = 2.3
        ax.text(1.5, txty, f"Attack {atk['id']}", ha='center', fontsize=18, fontweight='bold')
        ax.text(1.5, txty-0.35,
                f"A={atk['attr']}\nS={atk['struct']}\nSh={'Yes' if atk['shadow'] else 'No'}",
                ha='center', fontsize=12, family='monospace', fontweight='bold')

    legend_patches = [
        mpatches.Patch(color=KNOWLEDGE_COLORS['Low'], label='Low'),
        mpatches.Patch(color=KNOWLEDGE_COLORS['Low/Medium'], label='Low/Medium'),
        mpatches.Patch(color=KNOWLEDGE_COLORS['Medium'], label='Medium'),
        mpatches.Patch(color=KNOWLEDGE_COLORS['High'], label='High'),
    ]
    fig.legend(handles=legend_patches, loc='upper center', ncol=4, fontsize=15,
               borderaxespad=0.7, title='Knowledge Level', title_fontsize=17)

    fig.suptitle('Attack Taxonomy: 7 Adversary Knowledge Configurations',
                 fontsize=28, fontweight='bold', y=0.97)
    fig.savefig(os.path.join(FIGURE_DIR, '001_attack_taxonomy.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Saved: 01_attack_taxonomy.png")


def make_figure_2():
    """Figure 2: Fidelity bar chart for all 7 attacks"""
    fig, ax = plt.subplots(figsize=(24, 13))
    ids = [f"A{i}" for i in range(7)]
    means = [a['mean'] for a in ATTACK_DATA]
    stds = [a['std'] for a in ATTACK_DATA]
    bars_colors = [KNOWLEDGE_COLORS[a['knowledge']] for a in ATTACK_DATA]

    bars = ax.bar(ids, means, yerr=stds, capsize=10, color=bars_colors,
                  edgecolor='black', alpha=0.85, linewidth=1.5)

    for bar, m, s in zip(bars, means, stds):
        height = bar.get_height()
        mid_x = bar.get_x() + bar.get_width() / 2.
        ax.text(mid_x, height + s + 0.03, f'{m:.2f}', ha='center', va='bottom',
                fontweight='bold', fontsize=18)
        atk_idx = int(round(mid_x))
        ax.text(mid_x, -0.14, ATTACK_DATA[atk_idx]['knowledge'],
                ha='center', va='top', fontsize=13, style='italic')

    ax.set_ylabel('Fidelity (Mean +/- Std)', fontsize=18, fontweight='bold')
    ax.set_xlabel('Attack Type', fontsize=18, fontweight='bold')
    ax.set_title('Fidelity Across All 7 Attack Configurations', fontsize=22, fontweight='bold', pad=15)
    ax.set_ylim(-0.23, 1.05)
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, linewidth=2, label='Random baseline')
    ax.axhline(y=0.75, color='red', linestyle='--', alpha=0.6, linewidth=2, label='High-fidelity threshold')
    ax.legend(loc='lower right', fontsize=15)
    ax.tick_params(labelsize=15)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURE_DIR, '002_fidelity_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Saved: 02_fidelity_comparison.png")


def make_figure_3():
    """Figure 3: Fidelity heat map - structure vs shadow"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 12))

    structure_levels = ['Unknown', 'Partial', 'Known']
    shadow_levels = ['Unknown', 'Known']
    mat = np.zeros((3, 2))
    labels = [[''] * 2 for _ in range(3)]

    for atk in ATTACK_DATA:
        s_idx = structure_levels.index(atk['struct'])
        sh_idx = 0 if not atk['shadow'] else 1
        mat[s_idx, sh_idx] = atk['mean']
        labels[s_idx][sh_idx] = f"A{atk['id']}\n{atk['mean']:.2f}"

    im = ax1.imshow(mat, cmap='YlOrRd', aspect='auto', vmin=0.3, vmax=0.9)
    ax1.set_xticks(range(2))
    ax1.set_xticklabels(shadow_levels, fontsize=15)
    ax1.set_yticks(range(3))
    ax1.set_yticklabels(structure_levels, fontsize=15)
    ax1.set_title('Mean Fidelity Heatmap (Structure vs Shadow)', fontsize=17, fontweight='bold')
    ax1.set_xlabel('Shadow Dataset', fontsize=15)
    ax1.set_ylabel('Structure Knowledge', fontsize=15)

    for i in range(3):
        for j in range(2):
            ax1.text(j, i, labels[i][j], ha='center', va='center', fontsize=13, fontweight='bold')

    fig.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)

    attr_levels = ['Unknown', 'Partial']
    mat_attr = np.zeros((2, 2))
    labels_attr = [[''] * 2 for _ in range(2)]

    for atk in ATTACK_DATA:
        a_idx = attr_levels.index(atk['attr'])
        mat_attr[a_idx][0 if not atk['shadow'] else 1] = atk['mean']
        labels_attr[a_idx][0 if not atk['shadow'] else 1] = f"A{atk['id']}\n{atk['mean']:.2f}"

    im2 = ax2.imshow(mat_attr, cmap='YlGnBu', aspect='auto', vmin=0.3, vmax=0.9)
    ax2.set_xticks(range(2))
    ax2.set_xticklabels(shadow_levels, fontsize=15)
    ax2.set_yticks(range(2))
    ax2.set_yticklabels(attr_levels, fontsize=15)
    ax2.set_title('Mean Fidelity Heatmap (Attributes vs Shadow)', fontsize=17, fontweight='bold')
    ax2.set_xlabel('Shadow Dataset', fontsize=15)
    ax2.set_ylabel('Attribute Knowledge', fontsize=15)

    for i in range(2):
        for j in range(2):
            ax2.text(j, i, labels_attr[i][j], ha='center', va='center', fontsize=13, fontweight='bold')
    fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

    fig.suptitle('Fidelity Dependence on Knowledge Dimensions', fontsize=22, fontweight='bold')
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURE_DIR, '03_fidelity_heatmaps.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Saved: 03_fidelity_heatmaps.png")


def make_figure_4():
    """Figure 4: Attack pipeline diagram"""
    fig, ax = plt.subplots(figsize=(22, 11))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    steps = [
        {"x": 0.5, "y": 2.5, "text": "1. Train\nTarget GNN", "color": "#dfefff", "border": "#0077cc"},
        {"x": 2.0, "y": 4.0, "text": "2. Construct\nAttack Graph", "color": "#fff3cd", "border": "#f0ad4e"},
        {"x": 2.0, "y": 1.0, "text": "3. Query Target\nModel", "color": "#fff3cd", "border": "#f0ad4e"},
        {"x": 4.5, "y": 4.0, "text": "4. Extract\nLabels", "color": "#d4edcc", "border": "#28a745"},
        {"x": 4.5, "y": 1.0, "text": "4b. Shadow\nPre-training", "color": "#d4edcc", "border": "#28a745"},
        {"x": 7.0, "y": 2.5, "text": "5. Fine-tune\nSurrogate", "color": "#cce5ff", "border": "#007bff"},
        {"x": 9.0, "y": 2.5, "text": "6. Fidelity\nMeasurement", "color": "#f8d7da", "border": "#dc3545"},
    ]

    arrow_pairs = [(0, 1), (0, 2), (1, 3), (3, 4), (3, 6), (4, 5), (5, 6)]

    for i, s in enumerate(steps):
        bx = FancyBboxPatch((s['x']-0.7, s['y']-0.55), 1.4, 1.1,
                              boxstyle="round,pad=0.1", facecolor=s['color'],
                              edgecolor=s['border'], linewidth=2.5, zorder=10)
        ax.add_patch(bx)
        ax.text(s['x'], s['y'], s['text'], ha='center', va='center',
                fontsize=11, fontweight='bold', zorder=11)

    for src, dst in arrow_pairs:
        x1, y1 = steps[src]['x'], steps[src]['y']
        x2, y2 = steps[dst]['x'], steps[dst]['y']
        dx = x2 - x1
        dy = y2 - y1
        dist = np.sqrt(dx**2 + dy**2)
        ax.annotate('', xy=(x2 - 0.7*dx/dist, y2 - 0.55*dy/dist),
                    xytext=(x1 + 0.7*dx/dist, y1 + 0.55*dy/dist),
                    arrowprops=dict(arrowstyle='->', lw=1.8, color='black', zorder=5))

    ax.set_title('Model Extraction Attack Pipeline for GNNs', fontsize=17, fontweight='bold', pad=20)
    fig.savefig(os.path.join(FIGURE_DIR, '04_attack_pipeline.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Saved: 04_attack_pipeline.png")


def make_figure_5():
    """Figure 5: Knowledge factor contribution"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 11))

    groups = []
    for k in ['Low', 'Low/Medium', 'Medium', 'High']:
        subset = [a['mean'] for a in ATTACK_DATA if a['knowledge'] == k]
        if subset:
            groups.append({'name': k, 'data': subset})

    for i, g in enumerate(groups):
        jitters = [random.uniform(-0.05, 0.05) for _ in g['data']]
        colors = []
        for val in g['data']:
            idx = min(range(len(ATTACK_DATA)), key=lambda x: abs(ATTACK_DATA[x]['mean'] - val))
            colors.append(COLORS[idx])
        ax1.scatter([g['name']] * len(jitters), [val + j for val, j in zip(g['data'], jitters)],
                    s=120, c=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
        ax1.axhline(y=np.mean(g['data']), color='gray', linestyle='--', linewidth=1.8, alpha=0.5)

    ax1.set_ylabel('Fidelity', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Knowledge Level', fontsize=16, fontweight='bold')
    ax1.set_title('Fidelity Distribution by Knowledge Level', fontsize=18, fontweight='bold')
    ax1.set_ylim(0.35, 0.95)
    ax1.tick_params(labelsize=12)

    deltas = {
        'Structure Known': 0.95,
        'Shadow Set': 0.70,
        'Attributes Known': 0.45,
        'Full Knowledge': 0.83
    }
    labels = list(deltas.keys())
    values = list(deltas.values())
    bars = ax2.barh(labels, values, color=['#74c0fc', '#69db7c', '#ffd43b', '#b197fc'],
                    edgecolor='black', alpha=0.85, height=0.6, linewidth=1.2)
    ax2.set_xlabel('Relative Impact on Fidelity (Normalized)', fontsize=16, fontweight='bold')
    ax2.set_title('Feature Importance for Attack Success', fontsize=18, fontweight='bold')
    ax2.set_xlim(0, 1.1)
    for bar, val in zip(bars, values):
        ax2.text(val + 0.02, bar.get_y() + bar.get_height()/2.,
                f'{val:.2f}', va='center', fontsize=14)
    ax2.tick_params(labelsize=13)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURE_DIR, '05_knowledge_contributions.png'), dpi=600, bbox_inches='tight')
    plt.close(fig)
    print("Saved: 05_knowledge_contributions.png")


def make_figure_6():
    """Figure 6: GNN threat landscape"""
    fig, ax = plt.subplots(figsize=(22, 14))
    ax.set_xlim(-1.5, 4.5)
    ax.set_ylim(-1.5, 6.0)
    ax.axis('off')

    layers = [
        {"y": 4.5, "title": "Target GNN Fraud Detector", "color": "#d4edcc", "border": "#28a745",
         "content": ["Input Features (3-D)\n  - Amount Sent\n  - Amount Received\n  - Fraud Flag"],
         "width": 1.8},
        {"y": 3.0, "title": "Graph Convolution\n  Layer 1 (3 -> 16)", "color": "#fff3cd", "border": "#f0ad4e",
         "content": ["Message Passing\n  Neighbor Aggregation"], "width": 1.8},
        {"y": 1.5, "title": "Graph Convolution\n  Layer 2 (16 -> 2)", "color": "#d4edcc", "border": "#28a745",
         "content": ["Final Output (Fraud / Benign)"], "width": 1.8},
        {"y": 0.2, "title": "Inference API\n(Prediction Access)", "color": "#cce5ff", "border": "#007bff",
         "content": ["Query: (g, features) -> logits\nResponse: class or probability"], "width": 1.8},
    ]

    for i, layer in enumerate(layers):
        bx = FancyBboxPatch((2 - layer['width'] / 2, layer['y'] - 0.35), layer['width'], 0.7,
                              boxstyle="round,pad=0.08", facecolor=layer['color'],
                              edgecolor=layer['border'], linewidth=2.8)
        ax.add_patch(bx)
        ax.text(2, layer['y'], layer['title'], ha='center', va='center', fontsize=14,
                fontweight='bold')
        j = 0
        for line in layer['content']:
            ax.text(2, layer['y'] - 0.15 - j * 0.15, line, ha='center', va='top', fontsize=11,
                    family='monospace', zorder=10)
            j += 1

        if i < len(layers) - 1:
            ax.arrow(2, layer['y'] - 0.35, 0, -0.95, head_width=0.2, head_length=0.12,
                     fc='black', ec='black', linewidth=2)

    ax.text(0.3, 5.5, "GNN Architecture:", fontsize=15, fontweight='bold')
    nodes_demo = [(0, 4.8), (0.5, 4.8), (0.3, 4.0), (0.7, 4.0), (0.3, 3.2), (0.7, 3.2)]
    for x, y in nodes_demo:
        ax.plot(x, y, 'o', color='#1f77b4', markersize=12)
        ax.text(x + 0.2, y, "f=[500, 500, 0]", fontsize=10, va='center', family='monospace')

    message_box = FancyBboxPatch((-1.3, 2.5), 3.1, 2.3, boxstyle="round,pad=0.1",
                                  facecolor='#e8f4f8', edgecolor='#0077cc', linewidth=2.2, alpha=0.8)
    ax.add_patch(message_box)
    ax.text(0.3, 4.5, "?", fontsize=60, ha='center', va='center', color='#0077cc')
    ax.text(-0.3, 3.8, 'Aggregation', fontsize=14, fontweight='bold', style='italic', color='#0077cc')
    ax.text(-0.3, 3.4, '(Mean / Sum)', fontsize=11, color='#0077cc')
    ax.text(-0.3, 3.0, 'MLP', fontsize=12, style='italic')

    ax.text(2, 6.2, "Model Extraction Attack Viewpoint", fontsize=18, fontweight='bold',
            ha='center', color='#dc3545',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8d7da', edgecolor='#dc3545'))
    ax.text(3.8, 5.0, "Can I see\nthe graph?", fontsize=13, color='#dc3545',
            ha='left', va='center', fontweight='bold')
    ax.text(3.8, 3.5, "Can I get node\nfeatures?", fontsize=13, color='#dc3545',
            ha='left', va='center', fontweight='bold')
    ax.text(3.8, 0.8, "Can I sample\nlabels?", fontsize=13, color='#dc3545',
            ha='left', va='center', fontweight='bold')

    fig.savefig(os.path.join(FIGURE_DIR, '06_GNN_threat_landscape.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Saved: 06_GNN_threat_landscape.png")


def make_figure_7():
    """Figure 7: Network graph with knowledge overlays"""
    fig, axes = plt.subplots(1, 4, figsize=(26, 8))

    atk_indices = [6, 4, 2, 1]
    atks = [ATTACK_DATA[i] for i in atk_indices]
    titles = ["Full Knowledge\n(Attack 6)", "Partial Attributes\n(Attack 4)", "Unknown Attribs\n(Attack 2)",
              "Unknown Everything\n(Attack 1)"]

    pos_large = nx.spring_layout(GLOBAL_G, seed=42)
    for i, (ax, atk, title) in enumerate(zip(axes, atks, titles)):
        nx.draw(GLOBAL_G, pos_large, ax=ax, node_color=COLORS[atk['id']], node_size=180,
                with_labels=False, edge_color='black', alpha=0.6, width=1.8)

        if atk['id'] == 6:
            nx.draw_networkx_nodes(GLOBAL_G, pos_large, ax=ax, node_color='#74c0fc', node_size=220, alpha=0.9)
            for n in GLOBAL_G.nodes():
                ax.text(pos_large[n][0], pos_large[n][1] - 0.18, f"[{np.random.randint(0,100)}]", 
                        ha='center', va='top', fontsize=8, family='monospace', color='#74c0fc')
            edge_list = list(GLOBAL_G.edges())
            nx.draw_networkx_edges(GLOBAL_G, pos_large, edgelist=edge_list, ax=ax, edge_color='#74c0fc', width=2.8)
            label_text = "Full Structure\nNode Features"
        elif atk['id'] == 4:
            edge_list = list(GLOBAL_G.edges())
            nx.draw_networkx_edges(GLOBAL_G, pos_large, edgelist=edge_list, ax=ax, edge_color='#69db7c', width=2.8)
            ax.text(0.5, -0.35, "Partial Features\nKnown Topology", ha='center', fontsize=8, 
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#69db7c', alpha=0.3))
            label_text = "Partial Features"
        elif atk['id'] == 2:
            nx.draw_networkx_edges(GLOBAL_G, pos_large, ax=ax, edge_color='#ffd43b', width=2.8)
            label_text = "Known Structure\nUnknown Features"
        else:
            node_list = list(GLOBAL_G.nodes())
            nx.draw_networkx_nodes(GLOBAL_G, pos_large, ax=ax, node_color='#b197fc', node_size=200)
            label_text = "Unknown Everything"

        ax.set_title(title, fontsize=13, fontweight='bold', pad=10)
        ax.axis('off')

    fig.suptitle('Impact of Adversary Knowledge on Model Extraction Attack Feasibility',
                 fontsize=16, fontweight='bold', y=0.98)
    fig.savefig(os.path.join(FIGURE_DIR, '07_knowledge_overlay.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Saved: 07_knowledge_overlay.png")


if __name__ == "__main__":
    print("Generating Figure 1...")
    make_figure_1()
    print("Generating Figure 2...")
    make_figure_2()
    print("Generating Figure 3...")
    make_figure_3()
    print("Generating Figure 4...")
    make_figure_4()
    print("Generating Figure 5...")
    make_figure_5()
    print("Generating Figure 6...")
    make_figure_6()
    print("Generating Figure 7...")
    make_figure_7()
    print("All figures generated successfully. Check ./figures/ directory.")
