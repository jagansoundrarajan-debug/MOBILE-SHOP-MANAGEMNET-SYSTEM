# main.py

import tkinter as tk

from ui.login_ui import open_login_window

root = tk.Tk()

root.withdraw()

open_login_window(root)

root.mainloop()