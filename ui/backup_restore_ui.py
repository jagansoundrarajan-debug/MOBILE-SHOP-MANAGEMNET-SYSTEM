# ui/backup_restore_ui.py

import os
import tkinter as tk
from tkinter import messagebox

from modules import backup_restore as backup_module


def open_backup_restore_window(parent=None):

    win = tk.Toplevel(parent) if parent else tk.Tk()

    win.title("Backup & Restore")
    win.geometry("700x500")

    tk.Label(
        win,
        text="Database Backup & Restore",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    backup_list = tk.Listbox(
        win,
        width=80,
        height=15
    )

    backup_list.pack(
        padx=10,
        pady=10,
        fill="both",
        expand=True
    )

    def load_backups():

        backup_list.delete(
            0,
            tk.END
        )

        result = backup_module.handle({
            "action": "list"
        })

        if result.get("status") != "success":
            return

        for item in result["backups"]:

            backup_list.insert(
                tk.END,
                item
            )

    def create_backup():

        result = backup_module.handle({
            "action": "backup"
        })

        if result.get("status") == "success":

            messagebox.showinfo(
                "Success",
                result["path"]
            )

            load_backups()

        else:

            messagebox.showerror(
                "Error",
                result.get("message")
            )

    def restore_backup():

        selected = backup_list.curselection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Select Backup File"
            )

            return

        filename = backup_list.get(
            selected[0]
        )

        path = os.path.join(
            backup_module.BACKUP_DIR,
            filename
        )

        result = backup_module.handle({

            "action": "restore",

            "path": path
        })

        if result.get("status") == "success":

            messagebox.showinfo(
                "Success",
                "Database Restored"
            )

        else:

            messagebox.showerror(
                "Error",
                result.get("message")
            )

    btn_frame = tk.Frame(win)

    btn_frame.pack(
        pady=10
    )

    tk.Button(
        btn_frame,
        text="Create Backup",
        bg="green",
        fg="white",
        command=create_backup
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        btn_frame,
        text="Restore Selected",
        bg="orange",
        command=restore_backup
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        btn_frame,
        text="Refresh",
        command=load_backups
    ).pack(
        side="left",
        padx=5
    )

    load_backups()

    if not parent:
        win.mainloop()


if __name__ == "__main__":

    open_backup_restore_window()
