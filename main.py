#main.py
import tkinter as tk

from database import initialize_database
from ui.login_ui import open_login_window

# Create database and tables
initialize_database()

# Start application
root = tk.Tk()
root.withdraw()

open_login_window(root)

root.mainloop()
