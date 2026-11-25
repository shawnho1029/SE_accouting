"""Input module v2: validated multi-entry expense CLI with summary and sample data."""

import csv
import os
from datetime import datetime

CSV_FILE = "expenses.csv"
FIELDNAMES = ["date", "amount", "category", "notes"]
DEFAULT_CATEGORIES = ["Food", "Transport", "Shopping", "Entertainment", "Utilities", "Other"]

SAMPLE_EXPENSES = [
    {"date": "2026-11-20", "amount": "180.00", "category": "Food", "notes": "Lunch bento and drink"},
    {"date": "2026-11-20", "amount": "55.00", "category": "Transport", "notes": "Bus fare"},
    {"date": "2026-11-21", "amount": "650.00", "category": "Shopping", "notes": "Notebook and pens"},
    {"date": "2026-11-22", "amount": "320.00", "category": "Entertainment", "notes": "Movie ticket"},
    {"date": "2026-11-23", "amount": "240.00", "category": "Food", "notes": "Dinner with friends"},
    {"date": "2026-11-24", "amount": "450.00", "category": "Utilities", "notes": "Phone bill"},
    {"date": "2026-11-25", "amount": "120.00", "category": "Transport", "notes": "Scooter fuel"},
]


def ensure_csv_header(csv_path: str = CSV_FILE) -> None:
    """Create the CSV file with headers if it does not exist or is empty."""
    if not os.path.isfile(csv_path) or os.path.getsize(csv_path) == 0:
        with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def save_expense(date_str: str, amount: float, category: str, notes: str = "", csv_path: str = CSV_FILE) -> None:
    """Append a validated expense record to the CSV file."""
    ensure_csv_header(csv_path)
    with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({
            "date": date_str,
            "amount": f"{amount:.2f}",
            "category": category,
            "notes": notes,
        })


def load_sample_data(csv_path: str = CSV_FILE, overwrite: bool = False) -> int:
    """Load sample expense records into CSV. Returns number of rows written."""
    mode = "w" if overwrite or not os.path.isfile(csv_path) or os.path.getsize(csv_path) == 0 else "a"
    with open(csv_path, mode=mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if mode == "w":
            writer.writeheader()
        writer.writerows(SAMPLE_EXPENSES)
    return len(SAMPLE_EXPENSES)


def read_expenses(csv_path: str = CSV_FILE) -> list[dict[str, str]]:
    """Read all expense rows from the CSV file."""
    if not os.path.isfile(csv_path):
        return []
    with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def prompt_date() -> str:
    """Prompt until a valid YYYY-MM-DD date is entered (blank defaults to today)."""
    today = datetime.now().strftime("%Y-%m-%d")
    while True:
        raw = input(f"Date (YYYY-MM-DD) [default {today}]: ").strip()
        if not raw:
            return today
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD (e.g. 2026-11-25).")


def prompt_amount() -> float:
    """Prompt until a positive numeric amount is entered."""
    while True:
        raw = input("Amount (> 0): ").strip()
        try:
            value = float(raw)
            if value <= 0:
                print("Amount must be greater than 0.")
                continue
            return value
        except ValueError:
            print("Invalid number. Please enter a numeric amount (e.g. 120 or 99.5).")


def prompt_category() -> str:
    """Let user pick a preset category by number or type a custom category."""
    print("Categories:")
    for idx, cat in enumerate(DEFAULT_CATEGORIES, start=1):
        print(f"  {idx}. {cat}")
    while True:
        raw = input("Select category number or type custom name: ").strip()
        if not raw:
            print("Category cannot be empty.")
            continue
        if raw.isdigit():
            choice = int(raw)
            if 1 <= choice <= len(DEFAULT_CATEGORIES):
                return DEFAULT_CATEGORIES[choice - 1]
            print(f"Please choose 1-{len(DEFAULT_CATEGORIES)} or enter a category name.")
            continue
        return raw


def add_expenses_interactive(csv_path: str = CSV_FILE) -> None:
    """Loop to add one or more expenses interactively."""
    while True:
        print("\n--- Add New Expense ---")
        date_str = prompt_date()
        amount = prompt_amount()
        category = prompt_category()
        notes = input("Notes (optional): ").strip()

        save_expense(date_str, amount, category, notes, csv_path=csv_path)
        print(f"[Saved] {date_str} | {category} | ${amount:.2f}" + (f" | {notes}" if notes else ""))

        again = input("Add another expense? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            break


def view_summary(csv_path: str = CSV_FILE) -> None:
    """Print recorded expenses and total spending."""
    rows = read_expenses(csv_path)
    if not rows:
        print("\nNo expenses recorded yet.")
        return

    print("\n=== Recorded Expenses ===")
    total = 0.0
    for i, row in enumerate(rows, start=1):
        amt = float(row["amount"])
        total += amt
        note_part = f" ({row['notes']})" if row.get("notes") else ""
        print(f"{i:2d}. {row['date']} | {row['category']:<14} | ${amt:8.2f}{note_part}")
    print(f"Total ({len(rows)} items): ${total:.2f}")


def main() -> None:
    """Interactive menu for the expense input module."""
    while True:
        print("\n=== Expense Input Module (v2) ===")
        print("1. Add expense(s)")
        print("2. View recorded expenses")
        print("3. Load sample expenses (demo)")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_expenses_interactive()
        elif choice == "2":
            view_summary()
        elif choice == "3":
            count = load_sample_data()
            print(f"Loaded {count} sample expense records into {CSV_FILE}.")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please enter 1-4.")


if __name__ == "__main__":
    main()
