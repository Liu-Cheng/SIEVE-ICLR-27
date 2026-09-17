"""Regenerate figure6 (layer-pair mean cosine similarity, 3 models).

Data: SIEVE_ICLR-27/experiments/feature_visualization_all_steps_all_pairs/
      figure7_lingoqa_all_pairs_all.csv
Style: shared with make_fig2_fig3.py (Nord palette, serif, y-grid only).
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV_PATH = Path(
    "/home/chaiduo/projects/work/SIEVE_ICLR-27/experiments/"
    "feature_visualization_all_steps_all_pairs/figure7_lingoqa_all_pairs_all.csv"
)
OUT_DIR = Path(__file__).resolve().parent.parent / "Figures"

# Nord palette (consistent with figures 2/3/7)
BLUE, GREEN, RED = "#5E81AC", "#A3BE8C", "#BF616A"
GRID = "#D3D3D3"
LEGEND_KW = dict(facecolor="#F5F5F5", edgecolor="none")

GROUPS = [  # (csv sdc_group, label, color, marker)
    ("non_sdc", "Non-SDC", BLUE, "o"),
    ("non_significant_sdc", "Non-significant SDC", GREEN, "s"),
    ("significant_sdc", "Significant SDC", RED, "^"),
]
MODELS = ["Qwen2.5-VL-7B", "InternVL3-8B", "LLaVA-1.5-7B"]

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 9,
        "axes.titlesize": 9.5,
        "axes.labelsize": 9.5,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "pdf.fonttype": 42,
    }
)


def load() -> dict:
    # data[model][group] -> list of (pair, mean, lo, hi), sorted by pair
    acc = defaultdict(lambda: defaultdict(list))
    with CSV_PATH.open(newline="") as fh:
        for row in csv.DictReader(fh):
            if row["metric"] != "cos_sim":
                continue
            acc[row["model"]][row["sdc_group"]].append(
                (
                    (int(row["src_layer"]), int(row["tgt_layer"])),
                    float(row["mean_value"]),
                    float(row["mean_ci95_low"]),
                    float(row["mean_ci95_high"]),
                )
            )
    for model in acc:
        for group in acc[model]:
            acc[model][group].sort()
    return acc


def main() -> None:
    data = load()
    fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.6))
    for ax, model in zip(axes, MODELS):
        ax.set_title(f"({chr(ord('a') + MODELS.index(model))}) {model}")
        for group, label, color, marker in GROUPS:
            pts = data[model][group]
            xs = list(range(len(pts)))
            means = [p[1] for p in pts]
            lo = [p[2] for p in pts]
            hi = [p[3] for p in pts]
            ax.fill_between(xs, lo, hi, color=color, alpha=0.15, lw=0)
            ax.plot(
                xs, means, label=label, color=color, marker=marker,
                markersize=3.0, markeredgewidth=0.5, linewidth=1.2,
            )
        n = len(data[model]["non_sdc"])
        tick_pos = list(range(0, n, 4))
        if tick_pos[-1] != n - 1:
            tick_pos.append(n - 1)
        pairs = [p[0] for p in data[model]["non_sdc"]]
        ax.set_xticks(tick_pos)
        ax.set_xticklabels([f"({s},{t})" for s, t in (pairs[i] for i in tick_pos)],
                           rotation=90)
        ax.set_xlim(-0.5, n - 0.5)
        ax.set_ylim(0, 1.0)
        ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_xlabel("Layer pair")
        ax.set_axisbelow(True)
    axes[0].set_ylabel("Mean cosine similarity")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3,
               frameon=True, framealpha=1.0, handlelength=1.4,
               columnspacing=1.2, bbox_to_anchor=(0.5, 1.02), **LEGEND_KW)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(OUT_DIR / "figure6_layer_pair_cosine_similarity.png")
    fig.savefig(OUT_DIR / "figure6_layer_pair_cosine_similarity.pdf")
    print("done:", OUT_DIR)


if __name__ == "__main__":
    main()
