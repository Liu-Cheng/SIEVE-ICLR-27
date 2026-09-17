"""Regenerate Figure 2 and Figure 3 with a unified ICLR-ready style.

Data sources (authoritative, do not edit by hand):
  - Fig 2: experiments/figure2_significant_sdc_among_sdc/significant_sdc_among_finite_value_sdc.csv
  - Fig 3: experiments/fault_deviation_buckets_telemetry50/aggregate_finite_sdc_global_shares.csv

Usage:
  python scripts/make_fig2_fig3.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ----------------------------------------------------------------------------
# Shared style
# ----------------------------------------------------------------------------
BLUE, GREEN, RED = "#5E81AC", "#A3BE8C", "#BF616A"  # Nord palette
GRID = "#D3D3D3"
LEGEND_KW = dict(facecolor="#F5F5F5", edgecolor="none")

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 9.5,
        "axes.linewidth": 1.0,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": GRID,
        "grid.linewidth": 0.7,
        "axes.axisbelow": True,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    }
)

PCT = FuncFormatter(lambda v, _: f"{v:.0f}%")
OUT_DIR = Path(__file__).resolve().parent.parent / "Figures"

# ----------------------------------------------------------------------------
# Figure 2: Significant SDC share among finite-value SDCs (9 tasks)
# ----------------------------------------------------------------------------
# model, dataset, finite_value_sdc_labeled, significant_sdc
FIG2_ROWS = [
    ("Qwen2.5-VL-7B", "EarthVQA", 12133, 982),
    ("Qwen2.5-VL-7B", "LingoQA", 9388, 933),
    ("Qwen2.5-VL-7B", "VQAv2", 7904, 1033),
    ("InternVL3-8B", "EarthVQA", 13460, 2413),
    ("InternVL3-8B", "LingoQA", 11142, 2573),
    ("InternVL3-8B", "VQAv2", 11004, 2597),
    ("LLaVA-1.5-7B", "EarthVQA", 1205, 711),
    ("LLaVA-1.5-7B", "LingoQA", 1461, 763),
    ("LLaVA-1.5-7B", "VQAv2", 771, 710),
]

MODELS = ["Qwen2.5-VL-7B", "InternVL3-8B", "LLaVA-1.5-7B"]
DATASETS = ["EarthVQA", "LingoQA", "VQAv2"]
DS_COLORS = dict(zip(DATASETS, [BLUE, GREEN, RED]))


def make_figure2():
    shares = {
        (m, d): 100.0 * sig / labeled for m, d, labeled, sig in FIG2_ROWS
    }

    fig, ax = plt.subplots(figsize=(4.6, 3.1))
    bar_w, group_gap = 0.24, 0.06
    xs_base = []
    for gi in range(len(MODELS)):
        left = gi * (3 * bar_w + group_gap * 2)
        xs_base.append(left)

    for di, ds in enumerate(DATASETS):
        xs, ys = [], []
        for gi, m in enumerate(MODELS):
            x0 = gi * (3 * bar_w + group_gap * 2)
            xs.append(x0 + di * bar_w + bar_w / 2)
            ys.append(shares[(m, ds)])
        ax.bar(xs, ys, width=bar_w * 0.92, color=DS_COLORS[ds],
               edgecolor="black", linewidth=0.9, label=ds)
        for x, y in zip(xs, ys):
            ax.annotate(f"{y:.1f}", (x, y), xytext=(0, 2),
                        textcoords="offset points", ha="center", fontsize=9)

    centers = [gi * (3 * bar_w + group_gap * 2) + 1.5 * bar_w
               for gi in range(len(MODELS))]
    ax.set_xticks(centers)
    ax.set_xticklabels(MODELS)
    ax.set_xlim(-0.08, centers[-1] + 1.5 * bar_w + 0.08)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(PCT)
    ax.set_ylabel("Significant SDC share (%)")
    ax.legend(frameon=True, framealpha=1.0, loc="upper left", ncol=1,
              handlelength=1.4, **LEGEND_KW)
    ax.set_axisbelow(True)

    fig.savefig(OUT_DIR / "figure2_significant_SDC_share.png")
    fig.savefig(OUT_DIR / "figure2_significant_SDC_share.pdf")
    plt.close(fig)


# ----------------------------------------------------------------------------
# Figure 3: SDC percentage by fault-induced value deviation (broken axis)
# ----------------------------------------------------------------------------
# bucket, non-significant count, significant count  (denominator = 68468)
FIG3_ROWS = [
    ("[0, 1]", 39248, 941),
    (r"$(1, 10^6]$", 10265, 586),
    (r"$>10^6$", 6240, 11188),
]
TOTAL_FINITE_SDC = 40189 + 10851 + 17428  # 68468


def make_figure3():
    cats = ["Non-significant SDC", "Significant SDC"]
    cat_colors = {cats[0]: BLUE, cats[1]: GREEN}
    vals = {
        b: [100.0 * ns / TOTAL_FINITE_SDC, 100.0 * s / TOTAL_FINITE_SDC]
        for b, ns, s in FIG3_ROWS
    }

    # Single axis; the one oversized bar (57.3%) is sliced on the bar itself
    # (white gap + double slash) instead of using a broken two-panel axis.
    ymax, slice_y0, slice_y1 = 24.0, 21.2, 22.0
    fig, ax = plt.subplots(figsize=(4.6, 3.1))
    bar_w = 0.32
    for ci, cat in enumerate(cats):
        xs = [i + (ci - 0.5) * bar_w for i in range(len(FIG3_ROWS))]
        ys = [vals[b][ci] for b, _, _ in FIG3_ROWS]
        ax.bar(xs, ys, width=bar_w * 0.92, color=cat_colors[cat],
               edgecolor="black", linewidth=0.9, label=cat)
        for x, y in zip(xs, ys):
            if y < slice_y0:  # normal label above the bar
                ax.annotate(f"{y:.1f}", (x, y), xytext=(0, 2),
                            textcoords="offset points", ha="center", fontsize=9)

    # slice the oversized bar: plain white gap, no slash marks
    x_tall = 0 + (0 - 0.5) * bar_w  # bucket 0, category 0 (non-significant)
    half = bar_w * 0.92 / 2
    ax.add_patch(plt.Rectangle((x_tall - half - 0.005, slice_y0),
                               2 * half + 0.01, slice_y1 - slice_y0,
                               color="white", zorder=5))
    # explicit top edge of the clipped bar cap
    ax.plot([x_tall - half, x_tall + half], [ymax, ymax],
            color="black", lw=0.9, zorder=6, solid_capstyle="butt")
    ax.annotate(f"{vals[FIG3_ROWS[0][0]][0]:.1f}", (x_tall, ymax),
                xytext=(0, 2), textcoords="offset points",
                ha="center", fontsize=9, clip_on=False)

    ax.set_ylim(0, ymax)
    ax.set_yticks([0, 5, 10, 15, 20])
    ax.yaxis.set_major_formatter(PCT)
    ax.set_xticks(range(len(FIG3_ROWS)))
    ax.set_xticklabels([b for b, _, _ in FIG3_ROWS])
    ax.set_xlim(-0.6, len(FIG3_ROWS) - 0.4)
    ax.set_xlabel("Fault-induced value deviation")
    ax.set_ylabel("Percentage of SDCs (%)")
    ax.legend(frameon=True, framealpha=1.0, loc="upper right", ncol=1,
              handlelength=1.4, **LEGEND_KW)

    fig.savefig(OUT_DIR / "figure3_distribution_of_SDCs_by_numerical_deviation.png")
    fig.savefig(OUT_DIR / "figure3_distribution_of_SDCs_by_numerical_deviation.pdf")
    plt.close(fig)


def make_figure7():
    # Source: experiments/ablation_36d_k28_fit_only_strict_finite/
    #         component_ablation_paper_table.csv (Full / Finite macro F1, %)
    panels = [
        ("Layer-pair ablation", [
            ("Full 36D", 93.42205336320795, 71.48632125916124),
            ("w/o (6,7)", 92.25546580679183, 68.81785956669063),
            ("w/o (24,25)", 91.26395785216516, 66.78256865625123),
            ("w/o (26,27)", 90.94911025969053, 65.86415605097623),
        ]),
        ("Metric ablation", [
            ("Full 36D", 93.42205336320795, 71.48632125916124),
            ("w/o CosSim", 91.4669956757122, 64.79515612560853),
            ("w/o Mean", 89.68498769368995, 65.29280963195147),
            ("w/o Std", 92.96270395264808, 70.29817006055742),
            ("w/o L2", 92.02063034908761, 68.98759733418098),
        ]),
    ]
    cats = ["Full", "Finite"]
    cat_colors = {cats[0]: BLUE, cats[1]: GREEN}

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.5))
    bar_w = 0.36
    for ax, (title, rows) in zip(axes, panels):
        ax.set_title(title, pad=2)
        for ci, cat in enumerate(cats):
            xs = [i + (ci - 0.5) * bar_w for i in range(len(rows))]
            ys = [r[1 + ci] for r in rows]
            ax.bar(xs, ys, width=bar_w * 0.80, color=cat_colors[cat],
                   edgecolor="black", linewidth=0.9, label=cat)
            for x, y in zip(xs, ys):
                ax.annotate(f"{y:.1f}", (x, y), xytext=(0, 2),
                            textcoords="offset points", ha="center", fontsize=8.5)
        ax.set_xticks(range(len(rows)))
        ax.set_xticklabels([r[0] for r in rows], fontsize=7.5)
        ax.set_xlim(-0.6, len(rows) - 0.4)
        ax.set_ylim(60, 100)
        ax.set_yticks([60, 65, 70, 75, 80, 85, 90, 95, 100])
        ax.set_ylabel("Significant-SDC F1 (%)")

    # compact legend per panel: right side, hanging into the 95-100 band
    for ax in axes:
        ax.legend(frameon=True, framealpha=1.0, loc="upper right",
                  ncol=2, fontsize=8, handlelength=1.0, handletextpad=0.4,
                  borderpad=0.3, columnspacing=0.8,
                  bbox_to_anchor=(1.0, 1.0), **LEGEND_KW)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "figure7_component_ablation.png")
    fig.savefig(OUT_DIR / "figure7_component_ablation.pdf")
    plt.close(fig)


if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    make_figure2()
    make_figure3()
    make_figure7()
    print("done:", OUT_DIR)
