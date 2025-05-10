import json
import os
from datetime import datetime

class Expense:
    def __init__(self, amount, category, description="", date=None):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = []
        self.load_expenses()

    def add_expense(self, amount, category, description, date=None):
        expense = Expense(amount, category, description, date)
        self.expenses.append(expense)
        self.save_expenses()
        print(f"Expense of Ksh{amount:.2f} added to category '{category}'.")

    def delete_expense(self, index):
        try:
            expense = self.expenses.pop(index)
            self.save_expenses()
            print(f"Expense of Ksh{expense.amount:.2f} ({expense.description}) deleted.")
        except IndexError:
            print("Invalid expense number.")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses found.")
            return
        for i, expense in enumerate(self.expenses, 1):
            print(f"{i}. Ksh{expense.amount:.2f} - {expense.category} - {expense.description} (Date: {expense.date})")

    def summarize_by_category(self):
        if not self.expenses:
            print("No expenses to summarize.")
            return
        summary = {}
        for expense in self.expenses:
            summary[expense.category] = summary.get(expense.category, 0) + expense.amount
        print("\nExpense Summary by Category:")
        for category, total in summary.items():
            print(f"{category}: Ksh{total:.2f}")

    def summarize_by_month(self):
        if not self.expenses:
            print("No expenses to summarize.")
            return
        summary = {}
        for expense in self.expenses:
            month = expense.date[:7]  # Extract YYYY-MM
            summary[month] = summary.get(month, 0) + expense.amount
        print("\nExpense Summary by Month:")
        for month, total in sorted(summary.items()):
            print(f"{month}: Ksh{total:.2f}")

    def save_expenses(self):
        with open(self.filename, 'w') as f:
            json.dump([expense.to_dict() for expense in self.expenses], f, indent=4)

    def load_expenses(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                expenses_data = json.load(f)
                self.expenses = [Expense(
                    data["amount"],
                    data["category"],
                    data.get("description", ""),
                    data["date"]
                ) for data in expenses_data]

def main():
    tracker = ExpenseTracker()
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. Delete Expense")
        print("3. View All Expenses")
        print("4. Summarize by Category")
        print("5. Summarize by Month")
        print("6. Exit")
        choice = input("Enter choice (1-6): ")

        if choice == "1":
            try:
                amount = float(input("Enter amount: "))
                if amount < 0:
                    print("Amount cannot be negative.")
                    continue
                category = input("Enter category (e.g., Food, Transport, Bills): ")
                description = input("Enter description (optional): ")
                date = input("Enter date (YYYY-MM-DD, press Enter for today): ")
                date = date if date else None
                tracker.add_expense(amount, category, description, date)
            except ValueError:
                print("Please enter a valid number for amount.")

        elif choice == "2":
            tracker.view_expenses()
            try:
                index = int(input("Enter expense number to delete: ")) - 1
                tracker.delete_expense(index)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "3":
            tracker.view_expenses()

        elif choice == "4":
            tracker.summarize_by_category()

        elif choice == "5":
            tracker.summarize_by_month()

        elif choice == "6":
            print("Exiting Expense Tracker.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()