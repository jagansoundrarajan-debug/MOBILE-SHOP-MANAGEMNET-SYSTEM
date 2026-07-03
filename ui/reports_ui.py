# ui/reports_ui.py

import tkinter as tk
from tkinter import ttk, messagebox

from modules import reports as reports_module


def open_reports_window(parent=None):

    win = tk.Toplevel(parent) if parent else tk.Tk()

    win.title("Reports Dashboard")
    win.geometry("1000x650")

    # ==========================
    # TITLE
    # ==========================

    tk.Label(
        win,
        text="REPORTS DASHBOARD",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    # ==========================
    # SUMMARY
    # ==========================

    summary = tk.Frame(win)
    summary.pack(fill="x", padx=10)

    lbl_sales = tk.Label(summary, font=("Arial", 11, "bold"))
    lbl_sales.grid(row=0, column=0, padx=20)

    lbl_services = tk.Label(summary, font=("Arial", 11, "bold"))
    lbl_services.grid(row=0, column=1, padx=20)

    lbl_revenue = tk.Label(summary, font=("Arial", 11, "bold"))
    lbl_revenue.grid(row=0, column=2, padx=20)

    lbl_pending = tk.Label(summary, font=("Arial", 11, "bold"))
    lbl_pending.grid(row=0, column=3, padx=20)

    # ==========================
    # NOTEBOOK
    # ==========================

    notebook = ttk.Notebook(win)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    sales_tab = tk.Frame(notebook)
    service_tab = tk.Frame(notebook)

    notebook.add(sales_tab, text="Recent Sales")
    notebook.add(service_tab, text="Recent Services")

    # ==========================
    # SALES TABLE
    # ==========================

    sales_columns = (
        "Invoice",
        "Customer",
        "Product",
        "Amount",
        "Date"
    )

    sales_tree = ttk.Treeview(
        sales_tab,
        columns=sales_columns,
        show="headings"
    )

    for col in sales_columns:

        sales_tree.heading(col, text=col)
        sales_tree.column(col, width=180)

    sales_tree.pack(fill="both", expand=True)

    # ==========================
    # SERVICE TABLE
    # ==========================

    service_columns = (
        "Job No",
        "Customer",
        "Complaint",
        "Status",
        "Receive Date"
    )

    service_tree = ttk.Treeview(
        service_tab,
        columns=service_columns,
        show="headings"
    )

    for col in service_columns:

        service_tree.heading(col, text=col)
        service_tree.column(col, width=180)

    service_tree.pack(fill="both", expand=True)

    # ==========================
    # LOAD REPORTS
    # ==========================

    def load_reports():

        result = reports_module.handle({})

        if result.get("status") != "success":

            messagebox.showerror(
                "Error",
                result.get("message")
            )
            return

        lbl_sales.config(
            text=f"Sales : {result['total_sales']}"
        )

        lbl_services.config(
            text=f"Services : {result['total_services']}"
        )

        lbl_revenue.config(
            text=f"Revenue : ₹ {result['total_revenue']:.2f}"
        )

        lbl_pending.config(
            text=f"Pending : {result['pending_services']}"
        )

        sales_tree.delete(
            *sales_tree.get_children()
        )

        for row in result["recent_sales"]:

            sales_tree.insert(
                "",
                tk.END,
                values=(

                    row["invoice_no"],

                    row["customer_name"],

                    row["product_name"],

                    row["grand_total"],

                    row["sale_date"]
                )
            )

        service_tree.delete(
            *service_tree.get_children()
        )

        for row in result["recent_services"]:

            service_tree.insert(
                "",
                tk.END,
                values=(

                    row["job_no"],

                    row["customer_name"],

                    row["complaint"],

                    row["status"],

                    row["receive_date"]
                )
            )

    # ==========================
    # BUTTONS
    # ==========================

    btn = tk.Frame(win)

    btn.pack(pady=10)

    tk.Button(
        btn,
        text="Refresh",
        bg="green",
        fg="white",
        width=15,
        command=load_reports
    ).pack(side="left", padx=5)

    tk.Button(
        btn,
        text="Close",
        bg="red",
        fg="white",
        width=15,
        command=win.destroy
    ).pack(side="left", padx=5)

    load_reports()

    if not parent:
        win.mainloop()


if __name__ == "__main__":

    open_reports_window()
