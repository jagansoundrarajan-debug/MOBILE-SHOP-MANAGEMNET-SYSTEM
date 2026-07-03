# ui/analytics_ui.py

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

from modules import analytics as analytics_module


def open_analytics_window(parent=None):

    win = tk.Toplevel(parent) if parent else tk.Tk()

    win.title("Analytics Dashboard")
    win.geometry("1000x650")

    # ==========================
    # HEADER
    # ==========================

    tk.Label(
        win,
        text="ANALYTICS DASHBOARD",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    # ==========================
    # SUMMARY FRAME
    # ==========================

    summary_frame = tk.LabelFrame(
        win,
        text="Summary",
        padx=10,
        pady=10
    )

    summary_frame.pack(
        fill="x",
        padx=10,
        pady=5
    )

    revenue_var = tk.StringVar()
    sales_var = tk.StringVar()

    tk.Label(
        summary_frame,
        text="Total Revenue",
        font=("Arial", 12, "bold")
    ).grid(row=0, column=0, padx=20)

    tk.Label(
        summary_frame,
        textvariable=revenue_var,
        font=("Arial", 12)
    ).grid(row=0, column=1)

    tk.Label(
        summary_frame,
        text="Total Sales",
        font=("Arial", 12, "bold")
    ).grid(row=0, column=2, padx=20)

    tk.Label(
        summary_frame,
        textvariable=sales_var,
        font=("Arial", 12)
    ).grid(row=0, column=3)

    # ==========================
    # TOP PRODUCTS
    # ==========================

    product_frame = tk.LabelFrame(
        win,
        text="Top Selling Products"
    )

    product_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=5
    )

    product_tree = ttk.Treeview(
        product_frame,
        columns=("Product", "Qty"),
        show="headings",
        height=6
    )

    product_tree.heading(
        "Product",
        text="Product"
    )

    product_tree.heading(
        "Qty",
        text="Quantity Sold"
    )

    product_tree.pack(
        fill="both",
        expand=True
    )

    # ==========================
    # TOP BRANDS
    # ==========================

    brand_frame = tk.LabelFrame(
        win,
        text="Top Brands"
    )

    brand_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=5
    )

    brand_tree = ttk.Treeview(
        brand_frame,
        columns=("Brand", "Count"),
        show="headings",
        height=6
    )

    brand_tree.heading(
        "Brand",
        text="Brand"
    )

    brand_tree.heading(
        "Count",
        text="Sales Count"
    )

    brand_tree.pack(
        fill="both",
        expand=True
    )

    # ==========================
    # SERVICE STATUS
    # ==========================

    service_frame = tk.LabelFrame(
        win,
        text="Service Status"
    )

    service_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=5
    )

    service_tree = ttk.Treeview(
        service_frame,
        columns=("Status", "Count"),
        show="headings",
        height=4
    )

    service_tree.heading(
        "Status",
        text="Status"
    )

    service_tree.heading(
        "Count",
        text="Count"
    )

    service_tree.pack(
        fill="both",
        expand=True
    )

    # ==========================
    # LOAD DATA
    # ==========================

    def load_data():

        result = analytics_module.handle({})

        if result.get("status") != "success":

            messagebox.showerror(
                "Error",
                result.get("message")
            )

            return

        summary = result["sales_summary"]

        revenue_var.set(
            f"₹ {summary['revenue']:.2f}"
        )

        sales_var.set(
            str(summary["total_sales"])
        )

        product_tree.delete(
            *product_tree.get_children()
        )

        for row in result["top_products"]:

            product_tree.insert(
                "",
                tk.END,
                values=(

                    row["product_name"],

                    row["total_qty"]
                )
            )

        brand_tree.delete(
            *brand_tree.get_children()
        )

        for row in result["top_brands"]:

            brand_tree.insert(
                "",
                tk.END,
                values=(

                    row["brand"],

                    row["total"]
                )
            )

        service_tree.delete(
            *service_tree.get_children()
        )

        for row in result["service_status"]:

            service_tree.insert(
                "",
                tk.END,
                values=(

                    row["status"],

                    row["total"]
                )
            )

    # ==========================
    # CHARTS
    # ==========================

    def show_product_chart():

        result = analytics_module.handle({})

        products = result["top_products"]

        if not products:
            return

        labels = [
            row["product_name"]
            for row in products
        ]

        values = [
            row["total_qty"]
            for row in products
        ]

        plt.figure(figsize=(8, 5))

        plt.bar(
            labels,
            values
        )

        plt.title(
            "Top Selling Products"
        )

        plt.xlabel(
            "Product"
        )

        plt.ylabel(
            "Quantity"
        )

        plt.show()

    tk.Button(
        win,
        text="Show Product Chart",
        bg="green",
        fg="white",
        command=show_product_chart
    ).pack(
        pady=10
    )

    load_data()

    if not parent:
        win.mainloop()


if __name__ == "__main__":

    open_analytics_window()
