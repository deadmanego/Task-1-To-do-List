import json
import os
import time


class Task:
    def __init__(self, description, priority='low', due_date=None):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False

    def complete(self):
        self.completed = True

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        due_date = self.due_date.strftime('%Y-%m-%d') if self.due_date else "N/A"
        return f"{self.description} ({status}, {self.priority}, due on {due_date})"


class TodoList:
    def __init__(self, filename):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task):
        self.tasks.remove(task)
        self.save_tasks()

    def complete_task(self, task):
        task.complete()
        self.save_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                for task_data in data:
                    task = Task(task_data['description'], task_data['priority'], time.strptime(task_data['due_date'], '%Y-%m-%d'))
                    task.completed = task_data['completed']
                    self.tasks.append(task)

    def save_tasks(self):
        data = []
        for task in self.tasks:
            data.append({
                'description': task.description,
                'priority': task.priority,
                'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
                'completed': task.completed
            })
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def list_tasks(self):
        for task in self.tasks:
            print(task)


def main():
    todo_list = TodoList('todo_list.json')
    while True:
        print("\n1. Add Task")
        print("2. Remove Task")
        print("3. Complete Task")
        print("4. List Tasks")
        print("5. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            description = input("Enter task description: ")
            priority = input("Enter task priority (high/medium/low): ")
            due_date = input("Enter task due date (yyyy-mm-dd): ")
            task = Task(description, priority, time.strptime(due_date, '%Y-%m-%d'))
            todo_list.add_task(task)
        elif choice == 2:
            index = int(input("Enter index of task to remove: "))
            todo_list.remove_task(todo_list.tasks[index - 1])
        elif choice == 3:
            index = int(input("Enter index of task to mark as completed: "))
            todo_list.complete_task(todo_list.tasks[index - 1])
        elif choice == 4:
            todo_list.list_tasks()
        elif choice == 5:
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()