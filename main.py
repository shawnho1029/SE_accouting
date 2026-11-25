"""Unified CLI entry point integrating expense input and pie chart visualization."""

from expense_input import CSV_FILE, add_expenses_interactive, load_sample_data, view_summary
from visualize import CHART_FILE, generate_pie_chart


def main() -> None:
    """Run the integrated Expense Tracker menu."""
    while True:
        print("\n====================================")
        print("       Expense Tracker CLI")
        print("====================================")
        print("1. Add expense(s)")
        print("2. View recorded expenses")
        print("3. Generate & show category pie chart")
        print("4. Load sample expenses (for quick demo)")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            add_expenses_interactive(CSV_FILE)
        elif choice == "2":
            view_summary(CSV_FILE)
        elif choice == "3":
            generate_pie_chart(csv_path=CSV_FILE, output_path=CHART_FILE, show=True)
        elif choice == "4":
            count = load_sample_data(CSV_FILE)
            print(f"Loaded {count} sample expenses into {CSV_FILE}.")
        elif choice == "5":
            print("Exiting Expense Tracker. Bye!")
            break
        else:
            print("Invalid selection. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
