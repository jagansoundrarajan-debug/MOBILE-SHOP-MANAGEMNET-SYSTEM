# ui/inventory_ui.py

import tkinter as tk
from tkinter import ttk, messagebox

from modules import inventory as inventory_module


def open_inventory_window(parent=None):

    win = tk.Toplevel(parent) if parent else tk.Tk()

    win.title("Inventory Management")
    win.geometry("1000x600")

    # =========================
    # ENTRY FRAME
    # =========================

    frame = tk.LabelFrame(
        win,
        text="Add Product",
        padx=10,
        pady=10
    )

    frame.pack(fill="x", padx=10, pady=5)

    tk.Label(frame, text="Product Name").grid(row=0, column=0)

    e_product = tk.Entry(frame, width=30)
    e_product.grid(row=0, column=1)

    tk.Label(frame, text="Brand").grid(row=1, column=0)

    e_brand = tk.Entry(frame, width=30)
    e_brand.grid(row=1, column=1)

    tk.Label(frame, text="Model").grid(row=2, column=0)

    e_model = tk.Entry(frame, width=30)
    e_model.grid(row=2, column=1)

    tk.Label(frame, text="Purchase Price").grid(row=0, column=2)

    e_purchase = tk.Entry(frame, width=30)
    e_purchase.grid(row=0, column=3)

    tk.Label(frame, text="Selling Price").grid(row=1, column=2)

    e_selling = tk.Entry(frame, width=30)
    e_selling.grid(row=1, column=3)

    tk.Label(frame, text="Quantity").grid(row=2, column=2)

    e_quantity = tk.Entry(frame, width=30)
    e_quantity.grid(row=2, column=3)

    # =========================
    # SEARCH FRAME
    # =========================

    search_frame = tk.Frame(win)

    search_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(
        search_frame,
        text="Search"
    ).pack(side="left")

    e_search = tk.Entry(
        search_frame,
        width=40
    )

    e_search.pack(
        side="left",
        padx=5
    )

    # =========================
    # TABLE
    # =========================

    columns = (
        "ID",
        "Product",
        "Brand",
        "Model",
        "Purchase",
        "Selling",
        "Qty"
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

        tree.column(
            col,
            width=120
        )

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # =========================
    # FUNCTIONS
    # =========================

    def load_stock():

        tree.delete(
            *tree.get_children()
        )

        result = inventory_module.handle({
            "action": "list"
        })

        if result.get("status") != "success":
            return

        for item in result["items"]:

            tree.insert(
                "",
                tk.END,
                values=(

                    item["id"],

                    item["product_name"],

                    item["brand"],

                    item["model"],

                    item["purchase_price"],

                    item["selling_price"],

                    item["quantity"]
                )
            )

    def add_stock():

        payload = {

            "action": "add",

            "product_name":
                e_product.get(),

            "brand":
                e_brand.get(),

            "model":
                e_model.get(),

            "purchase_price":
                e_purchase.get(),

            "selling_price":
                e_selling.get(),

            "quantity":
                e_quantity.get()
        }

        result = inventory_module.handle(
            payload
        )

        if result.get("status") == "success":

            messagebox.showinfo(
                "Success",
                "Stock Added"
            )

            load_stock()

        else:

            messagebox.showerror(
                "Error",
                result.get("message")
            )

    def search_stock():

        keyword = e_search.get()

        result = inventory_module.handle({

            "action": "search",

            "keyword": keyword

        })

        tree.delete(
            *tree.get_children()
        )

        if result.get("status") != "success":
            return

        for item in result["items"]:

            tree.insert(
                "",
                tk.END,
                values=(

                    item["id"],

                    item["product_name"],

                    item["brand"],

                    item["model"],

                    item["purchase_price"],

                    item["selling_price"],

                    item["quantity"]
                )
            )

    # =========================
    # BUTTONS
    # =========================

    btn_frame = tk.Frame(win)

    btn_frame.pack(
        fill="x",
        pady=5
    )

    tk.Button(
        btn_frame,
        text="Add Stock",
        bg="green",
        fg="white",
        command=add_stock
    ).pack(side="left", padx=5)

    tk.Button(
        btn_frame,
        text="Search",
        bg="orange",
        command=search_stock
    ).pack(side="left", padx=5)

    tk.Button(
        btn_frame,
        text="Refresh",
        command=load_stock
    ).pack(side="left", padx=5)

    load_stock()

    if not parent:
        win.mainloop()


if __name__ == "__main__":

    open_inventory_window()
