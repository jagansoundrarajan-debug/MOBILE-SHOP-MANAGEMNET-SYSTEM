# ui/dashboard.py

import tkinter as tk
from tkinter import messagebox

from ui.sales_ui import open_sales_window
from ui.service_ui import open_service_window
from ui.inventory_ui import open_inventory_window
from ui.search_ui import open_search_window
from ui.analytics_ui import open_analytics_window
from ui.user_management_ui import open_usermanagement_window

from modules import reports as reports_module
from modules import backup_restore as backup_module
from modules import usermanagement as user_module


def open_dashboard(username, role, root):

    dashboard = tk.Toplevel(root)

    dashboard.title(
        "JAYAM MOBILES SALEM"
    )

    dashboard.geometry(
        "1200x700"
    )

    dashboard.configure(
        bg="white"
    )

    # ======================
    # HEADER
    # ======================

    header = tk.Frame(
        dashboard,
        bg="#1f4e79",
        height=60
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="MOBILE SHOP MANAGEMENT SYSTEM",
        bg="#1f4e79",
        fg="white",
        font=("Arial", 18, "bold")
    ).pack(
        pady=10
    )

    # ======================
    # SIDEBAR
    # ======================

    sidebar = tk.Frame(
        dashboard,
        bg="#2f2f2f",
        width=220
    )

    sidebar.pack(
        side="left",
        fill="y"
    )

    # ======================
    # MAIN AREA
    # ======================

    main_frame = tk.Frame(
        dashboard,
        bg="white"
    )

    main_frame.pack(
        side="right",
        expand=True,
        fill="both"
    )

    tk.Label(
        main_frame,
        text=f"Welcome {username}",
        font=("Arial", 20, "bold"),
        bg="white"
    ).pack(
        pady=20
    )

    tk.Label(
        main_frame,
        text=f"Role : {role}",
        font=("Arial", 12),
        bg="white"
    ).pack()

    # ======================
    # FUNCTIONS
    # ======================

    def open_sales():
        open_sales_window(dashboard)

    def open_service():
        open_service_window(dashboard)

    def open_inventory():
        open_inventory_window(dashboard)

    def open_search():
        open_search_window(dashboard)

    def open_analytics():
        open_analytics_window(dashboard)

    def open_reports():

        result = reports_module.handle({})

        if result.get("status") == "success":

            messagebox.showinfo(

                "Reports",

                f"Total Sales Records : {result['total_sales']}\n\n"
                f"Total Service Jobs : {result['total_services']}\n\n"
                f"Revenue : ₹{result['total_revenue']}\n\n"
                f"Pending Services : {result['pending_services']}"
            )

        else:

            messagebox.showerror(
                "Error",
                result.get("message")
            )

    def open_backup():

        result = backup_module.handle({

            "action": "backup"

        })

        if result.get("status") == "success":

            messagebox.showinfo(

                "Backup Success",

                result["path"]
            )

        else:

            messagebox.showerror(

                "Error",

                result.get("message")
            )

    def open_users():
        open_usermanagement_window(dashboard)
        result = user_module.handle({})

        if result.get("status") == "success":

            count = len(
                result["users"]
            )

            messagebox.showinfo(

                "Users",

                f"Total Users : {count}"
            )

    def logout():

        dashboard.destroy()

        root.deiconify()

    # ======================
    # BUTTON STYLE
    # ======================

    btn_style = {

        "font": ("Arial", 11),

        "width": 20,

        "bg": "#404040",

        "fg": "white"
    }

    # ======================
    # BUTTONS
    # ======================

    tk.Button(
        sidebar,
        text="Sales",
        command=open_sales,
        **btn_style
    ).pack(pady=10)

    tk.Button(
        sidebar,
        text="Service",
        command=open_service,
        **btn_style
    ).pack(pady=10)

    tk.Button(
        sidebar,
        text="Inventory",
        command=open_inventory,
        **btn_style
    ).pack(pady=10)

    tk.Button(
        sidebar,
        text="Search",
        command=open_search,
        **btn_style
    ).pack(pady=10)

    tk.Button(
        sidebar,
        text="Reports",
        command=open_reports,
        **btn_style
    ).pack(pady=10)

    tk.Button(
        sidebar,
        text="Analytics",
        command=open_analytics,
        **btn_style
    ).pack(pady=10)

    tk.Button(
        sidebar,
        text="Backup",
        command=open_backup,
        **btn_style
    ).pack(pady=10)

    if role == "Admin":

        tk.Button(
            sidebar,
            text="User Management",
            command=open_users,
            **btn_style
        ).pack(pady=10)

    tk.Button(
        sidebar,
        text="Logout",
        bg="red",
        fg="white",
        width=20,
        command=logout
    ).pack(
        side="bottom",
        pady=20
    )

    dashboard.protocol(
        "WM_DELETE_WINDOW",
        logout
    )
