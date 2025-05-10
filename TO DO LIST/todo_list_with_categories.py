import json
import os
from datetime import datetime

class Task:
    def __init__(self, description, category="General", due_date=None, completed=False):
        self.description = description
        self.category = category
        self.due_date = due_date
        self.completed = completed
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "completed": self.completed,
            "created_at": self.created_at
        }

class TodoList:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def add_task(self, description, category, due_date=None):
        task = Task(description, category, due_date)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task '{description}' added in category '{category}'.")

    def delete_task(self, index):
        try:
            task = self.tasks.pop(index)
            self.save_tasks()
            print(f"Task '{task.description}' deleted.")
        except IndexError:
            print("Invalid task number.")

    def update_task(self, index, description=None, category=None, due_date=None, completed=None):
        try:
            task = self.tasks[index]
            if description:
                task.description = description
            if category:
                task.category = category
            if due_date:
                task.due_date = due_date
            if completed is not None:
                task.completed = completed
            self.save_tasks()
            print(f"Task {index + 1} updated.")
        except IndexError:
            print("Invalid task number.")

    def view_tasks(self, category_filter=None):
        if not self.tasks:
            print("No tasks found.")
            return
        filtered_tasks = [task for task in self.tasks if not category_filter or task.category.lower() == category_filter.lower()]
        if not filtered_tasks:
            print(f"No tasks found in category '{category_filter}'.")
            return
        for i, task in enumerate(self.tasks, 1):
            if not category_filter or task.category.lower() == category_filter.lower():
                status = "✔" if task.completed else " "
                due = task.due_date if task.due_date else "No due date"
                print(f"{i}. [{status}] {task.description} (Category: {task.category}, Due: {due}, Created: {task.created_at})")

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                tasks_data = json.load(f)
                self.tasks = [Task(
                    data["description"],
                    data.get("category", "General"),  # Default to "General" if category is missing
                    data.get("due_date"),
                    data.get("completed", False)
                ) for data in tasks_data]
                for task, data in zip(self.tasks, tasks_data):
                    task.created_at = data["created_at"]

def main():
    todo = TodoList()
    while True:
        print("\nTodo List Menu:")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Update Task")
        print("4. View All Tasks")
        print("5. View Tasks by Category")
        print("6. Exit")
        choice = input("Enter choice (1-6): ")

        if choice == "1":
            description = input("Enter task description: ")
            category = input("Enter category (e.g., Work, Personal, School, press Enter for General): ")
            category = category if category else "General"
            due_date = input("Enter due date (YYYY-MM-DD, optional): ")
            due_date = due_date if due_date else None
            todo.add_task(description, category, due_date)

        elif choice == "2":
            todo.view_tasks()
            try:
                index = int(input("Enter task number to delete: ")) - 1
                todo.delete_task(index)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "3":
            todo.view_tasks()
            try:
                index = int(input("Enter task number to update: ")) - 1
                description = input("New description (press Enter to skip): ")
                category = input("New category (press Enter to skip): ")
                due_date = input("New due date (YYYY-MM-DD, press Enter to skip): ")
                completed = input("Mark as completed? (yes/no, press Enter to skip): ").lower()
                completed = True if completed == "yes" else False if completed == "no" else None
                todo.update_task(
                    index,
                    description if description else None,
                    category if category else None,
                    due_date if due_date else None,
                    completed
                )
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            todo.view_tasks()

        elif choice == "5":
            category = input("Enter category to filter (e.g., Work, Personal): ")
            todo.view_tasks(category if category else None)

        elif choice == "6":
            print("Exiting Todo List.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()