# ui/user_management_ui.py

import tkinter as tk
from tkinter import ttk, messagebox

from modules import usermanagement as user_module


def open_usermanagement_window(parent=None):

    win = tk.Toplevel(parent) if parent else tk.Tk()

    win.title("User Management")
    win.geometry("700x500")

    # =====================
    # ADD USER
    # =====================

    frame = tk.LabelFrame(
        win,
        text="Add User"
    )

    frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    tk.Label(
        frame,
        text="Username"
    ).grid(row=0, column=0)

    e_username = tk.Entry(
        frame,
        width=30
    )

    e_username.grid(
        row=0,
        column=1
    )

    tk.Label(
        frame,
        text="Password"
    ).grid(row=1, column=0)

    e_password = tk.Entry(
        frame,
        width=30,
        show="*"
    )

    e_password.grid(
        row=1,
        column=1
    )

    tk.Label(
        frame,
        text="Role"
    ).grid(row=2, column=0)

    role_var = tk.StringVar(
        value="User"
    )

    tk.OptionMenu(
        frame,
        role_var,
        "Admin",
        "User"
    ).grid(
        row=2,
        column=1
    )

    # =====================
    # TABLE
    # =====================

    columns = (
        "ID",
        "Username",
        "Role"
    )

    tree = ttk.Treeview(
        win,
        columns=columns,
        show="headings"
    )

    for col in columns:

        tree.heading(
            col,
            text=col
        )

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # =====================
    # FUNCTIONS
    # =====================

    def load_users():

        tree.delete(
            *tree.get_children()
        )

        result = user_module.handle({})

        if result.get("status") != "success":
            return

        for user in result["users"]:

            tree.insert(
                "",
                tk.END,
                values=(

                    user["id"],

                    user["username"],

                    user["role"]
                )
            )

    def add_user():

        result = user_module.handle({

            "action": "create",

            "username":
                e_username.get(),

            "password":
                e_password.get(),

            "role":
                role_var.get()
        })

        if result.get("status") == "success":

            messagebox.showinfo(
                "Success",
                "User Created"
            )

            load_users()

        else:

            messagebox.showerror(
                "Error",
                result.get("message")
            )

    def delete_user():

        selected = tree.selection()

        if not selected:

            return

        values = tree.item(
            selected[0]
        )["values"]

        user_id = values[0]

        result = user_module.handle({

            "action": "delete",

            "user_id":
                user_id
        })

        if result.get("status") == "success":

            load_users()

    # =====================
    # BUTTONS
    # =====================

    btn_frame = tk.Frame(win)

    btn_frame.pack(
        pady=10
    )

    tk.Button(
        btn_frame,
        text="Add User",
        bg="green",
        fg="white",
        command=add_user
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        btn_frame,
        text="Delete User",
        bg="red",
        fg="white",
        command=delete_user
    ).pack(
        side="left",
        padx=5
    )

    load_users()

    if not parent:
        win.mainloop()
