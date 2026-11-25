"""Visualization module v2: polished category pie chart with error handling and PNG export."""

import argparse
import csv
import os
from collections import defaultdict
import matplotlib.pyplot as plt

CSV_FILE = "expenses.csv"
CHART_FILE = "sample_pie_chart.png"

# Configure fallback fonts so both English and CJK labels render cleanly
plt.rcParams["font.sans-serif"] = [
    "Microsoft JhengHei",
    "PingFang TC",
    "Noto Sans CJK TC",
    "SimHei",
    "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False

COLOR_PALETTE = [
    "#4E79A7",
    "#F28E2B",
    "#E15759",
    "#76B7B2",
    "#59A14F",
    "#EDC948",
    "#B07AA1",
    "#FF9DA7",
    "#9C755F",
    "#BAB0AC",
]


def load_category_totals(csv_path: str = CSV_FILE) -> dict[str, float]:
    """Load expenses.csv and sum positive amounts by category."""
    if not os.path.isfile(csv_path):
        return {}

    totals: dict[str, float] = defaultdict(float)
    with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                amount = float(row.get("amount", 0))
            except (TypeError, ValueError):
                continue
            if amount <= 0:
                continue
            category = (row.get("category") or "Other").strip() or "Other"
            totals[category] += amount

    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def generate_pie_chart(
    csv_path: str = CSV_FILE,
    output_path: str = CHART_FILE,
    show: bool = True,
) -> bool:
    """Create a category pie chart, save as PNG, and optionally display it."""
    totals = load_category_totals(csv_path)
    if not totals:
        print(f"No valid expense data found in '{csv_path}'. Please add expenses first.")
        return False

    categories = list(totals.keys())
    amounts = list(totals.values())
    grand_total = sum(amounts)
    colors = [COLOR_PALETTE[i % len(COLOR_PALETTE)] for i in range(len(categories))]

    fig, ax = plt.subplots(figsize=(8.5, 6))
    wedges, _, autotexts = ax.pie(
        amounts,
        labels=categories,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        pctdistance=0.75,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")
        autotext.set_fontsize(9)

    legend_labels = [
        f"{cat}: ${amt:,.2f} ({amt / grand_total * 100:.1f}%)"
        for cat, amt in zip(categories, amounts)
    ]
    ax.legend(
        wedges,
        legend_labels,
        title="Category Breakdown",
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
        frameon=False,
    )

    ax.set_title(f"Expenses by Category (Total: ${grand_total:,.2f})", fontsize=14, fontweight="bold", pad=16)
    ax.axis("equal")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Pie chart saved to '{output_path}'.")

    if show:
        plt.show()
    else:
        plt.close(fig)
    return True


def main() -> None:
    """Parse CLI flags and run pie chart generation."""
    parser = argparse.ArgumentParser(description="Generate a category-based expense pie chart.")
    parser.add_argument("--csv", default=CSV_FILE, help="Path to expenses CSV file.")
    parser.add_argument("--output", default=CHART_FILE, help="Output PNG path.")
    parser.add_argument("--no-show", action="store_true", help="Save PNG without opening chart window.")
    args = parser.parse_args()

    generate_pie_chart(csv_path=args.csv, output_path=args.output, show=not args.no_show)


if __name__ == "__main__":
    main()
