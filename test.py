import sqlite3  # Imports Python's built-in SQLite database module

class TaskDB:
    def __init__(self, db_name="tasks.db"):  # Connects to the database
        self.conn = sqlite3.connect(db_name)  # Creates the database file if it doesn't exist
        self.cursor = self.conn.cursor()  # Creates a cursor to run SQL commands
        self.create_table()  # Ensures the tables exist

    def create_table(self):  # Creates the tasks table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                description TEXT,
                                due_date TEXT,
                                priority TEXT CHECK(priority IN ('High', 'Medium', 'Low')),
                                category TEXT,
                                completed INTEGER DEFAULT 0)''')
        self.conn.commit()  # Saves changes to the database

    def close(self):  # Closes the database connection after use
        self.conn.close()

class Task:
    def __init__(self, title, description="", due_date="", priority="Medium", category="General", completed=0):
        self.title = title # task title
        self.description = description # brief description of the task
        self.due_date = due_date # deadline for the task
        self.priority = priority # defaults to medium if not specified
        self.category = category #grouping tasks by category
        self.completed = completed # defaults to not completed

class TaskManager:
    def __init__(self, db_name="tasks.db"):
        self.db = TaskDB(db_name) # creates a database connection instance
# adding a task to the database
    def add_task(self, task):
        with self.db.conn: # ensures safe management of database operations
            self.db.cursor.execute("INSERT INTO tasks (title, description, due_date, priority, category, completed) VALUES (?, ?, ?, ?, ?, ?)",
                                   (task.title, task.description, task.due_date, task.priority, task.category, task.completed))

    def view_tasks(self, sort_by="priority", category=None):
        query = "SELECT * FROM tasks"
        params = [] # Holds query parameters if filtering is needed
        if category: # If a category is specified, filter tasks by that category
            query += " WHERE category = ?"
            params.append(category)
        query += f" ORDER BY {sort_by} DESC" # sorts tasks by priority
        self.db.cursor.execute(query, params)
        tasks = self.db.cursor.fetchall() #retrieves all matching tasks

        print("\nTask List:")
        for task in tasks:
            print(task)

    def mark_complete(self, task_id):
        with self.db.conn:
            self.db.cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))

    def delete_task(self, task_id):
        with self.db.conn:
            self.db.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

def main():
    manager = TaskManager()
    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. View Tasks by Category")
        print("4. Mark Task as Complete")
        print("5. Delete Task")
        print("6. Exit")

        choice = input("Choose an option: ") # Gets user input
        if choice == "1": #Adding tasks
            title = input("Task Title: ")
            description = input("Description (optional): ")
            due_date = input("Due Date (optional): ")

            #  Automatically corrects priority casing
            priority = input("Priority (High, Medium, Low): ").capitalize()
            if priority not in ["High", "Medium", "Low"]:  # Prevents invalid entries
                print("Invalid priority! Defaulting to 'Medium'.")
                priority = "Medium"

            category = input("Category: ") # gets category input
            manager.add_task(Task(title, description, due_date, priority, category))

        elif choice == "2": # view all tasks
            manager.view_tasks()

        elif choice == "3": # view tasks filtered by category
            category = input("Enter category: ")
            manager.view_tasks(category=category)

        elif choice == "4": # mark a task as complete
            task_id = int(input("Enter Task ID to mark as complete: "))
            manager.mark_complete(task_id)

        elif choice == "5": #delete a task
            task_id = int(input("Enter Task ID to delete: "))
            manager.delete_task(task_id)

        elif choice == "6": # exit the program
            break
        else:
            print("Invalid choice, try again!")

if __name__ == "__main__":
    main() # starts the program