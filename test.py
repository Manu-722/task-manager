import sqlite3 # imports python's built-in SQLite database module

class TaskDB:
    def __init__(self, db_name="tasks.db"): # connects to the database 
        self.conn = sqlite3.connect(db_name) # connects to the SQL database and if it doesn't exist it is created
        self.cursor = self.conn.cursor() # creates a cursor to run SQL commands 
        self.create_table() # calls the method to make sure tables exist 

    def create_table(self): # create the tasks table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                description TEXT,
                                due_date TEXT, 
                                priority TEXT CHECK(priority IN ('High', 'Medium', 'Low')),
                                category TEXT,
                                completed INTEGER DEFAULT 0)''')
        self.conn.commit() # saves the table to the database making sure changes are stored
    def close(self): # used for closing the database after usage

        self.conn.close()# closes the connection of the database file
class Task:
    def __init__(self, title, description="", due_date="", priority="Medium", category="General", completed=0):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.category = category
        self.completed = completed
class TaskManager:
    def __init__(self, db_name="tasks.db"):
        self.db = TaskDB(db_name)
    def add_task(self, task):
        with self.db.conn:
            self.db.cursor.execute("INSERT INTO tasks (title, description, due_date, priority, category, completed) VALUES (?, ?, ?, ?, ?, ?)",
                                   (task.title, task.description, task.due_date, task.priority, task.category, task.completed))
    