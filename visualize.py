"""Visualization module v1: read expenses.csv and show a basic category pie chart."""

import csv
from collections import defaultdict
import matplotlib.pyplot as plt

CSV_FILE = "expenses.csv"


def load_category_totals(csv_path: str = CSV_FILE) -> dict[str, float]:
    """Sum expense amounts grouped by category."""
    totals: dict[str, float] = defaultdict(float)
    with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row["category"].strip() or "Other"
            totals[category] += float(row["amount"])
    return dict(totals)


def main() -> None:
    """Generate and display a basic pie chart by category."""
    totals = load_category_totals()
    labels = list(totals.keys())
    values = list(totals.values())

    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Expenses by Category")
    plt.axis("equal")
    plt.show()


if __name__ == "__main__":
    main()
