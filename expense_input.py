"""Input module v1: basic CLI expense entry saved to expenses.csv."""

import csv
import os

CSV_FILE = "expenses.csv"
FIELDNAMES = ["date", "amount", "category", "notes"]


def save_expense(date_str: str, amount: float, category: str, notes: str = "", csv_path: str = CSV_FILE) -> None:
    """Append a single expense record to the CSV file, creating headers if needed."""
    file_exists = os.path.isfile(csv_path) and os.path.getsize(csv_path) > 0
    with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "date": date_str,
            "amount": f"{amount:.2f}",
            "category": category,
            "notes": notes,
        })


def main() -> None:
    """Prompt the user to enter one expense record and save it."""
    print("=== Expense Entry (v1) ===")
    date_str = input("Date (YYYY-MM-DD): ").strip()
    amount = float(input("Amount: ").strip())
    category = input("Category (e.g., Food, Transport, Shopping): ").strip()
    notes = input("Notes (optional): ").strip()

    save_expense(date_str, amount, category, notes)
    print(f"Saved expense: {date_str} | {category} | {amount:.2f}")


if __name__ == "__main__":
    main()
