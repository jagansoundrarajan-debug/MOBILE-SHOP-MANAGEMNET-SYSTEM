
# ui/login_ui.py

import tkinter as tk
from tkinter import messagebox

from modules import login as login_module
from ui.dashboard_ui import open_dashboard


def open_login_window(root=None):

    if root:
        win = tk.Toplevel(root)
    else:
        win = tk.Tk()

    win.title("JAYAM MOBILES SALEM")
    win.geometry("450x350")
    win.resizable(False, False)

    tk.Label(
        win,
        text="MOBILE SHOP MANAGEMENT SYSTEM",
        font=("Arial", 14, "bold"),
        fg="blue"
    ).pack(pady=20)

    tk.Label(
        win,
        text="Username"
    ).pack()

    username_entry = tk.Entry(
        win,
        width=35
    )

    username_entry.pack(pady=5)

    tk.Label(
        win,
        text="Password"
    ).pack()

    password_entry = tk.Entry(
        win,
        width=35,
        show="*"
    )

    password_entry.pack(pady=5)

    def do_login():

        username = username_entry.get().strip()

        password = password_entry.get().strip()

        if not username:

            messagebox.showwarning(
                "Warning",
                "Enter Username"
            )

            return

        if not password:

            messagebox.showwarning(
                "Warning",
                "Enter Password"
            )

            return

        result = login_module.handle({

            "action": "authenticate",

            "username": username,

            "password": password

        })

        if result.get("status") == "success":

            messagebox.showinfo(
                "Success",
                f"Welcome {result['username']}"
            )

            win.withdraw()

            open_dashboard(
                result["username"],
                result["role"],
                root if root else win
            )

        else:

            messagebox.showerror(
                "Login Failed",
                result.get("message")
            )

    tk.Button(
        win,
        text="LOGIN",
        bg="green",
        fg="white",
        width=20,
        command=do_login
    ).pack(pady=20)

    def on_close():

        win.destroy()

    win.protocol(
        "WM_DELETE_WINDOW",
        on_close
    )

    return win


if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    open_login_window(root)

    root.mainloop()
