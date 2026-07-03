# ui/search_ui.py

import tkinter as tk
from tkinter import ttk, messagebox

from modules import search as search_module


def open_search_window(parent=None):

    win = tk.Toplevel(parent) if parent else tk.Tk()

    win.title("Customer Search")
    win.geometry("1000x650")

    # ==========================
    # SEARCH FRAME
    # ==========================

    search_frame = tk.LabelFrame(
        win,
        text="Search",
        padx=10,
        pady=10
    )

    search_frame.pack(
        fill="x",
        padx=10,
        pady=5
    )

    tk.Label(
        search_frame,
        text="Keyword"
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    e_search = tk.Entry(
        search_frame,
        width=40
    )

    e_search.grid(
        row=0,
        column=1,
        padx=5
    )

    scope_var = tk.StringVar(
        value="both"
    )

    tk.Radiobutton(
        search_frame,
        text="Sales",
        variable=scope_var,
        value="sales"
    ).grid(row=0, column=2)

    tk.Radiobutton(
        search_frame,
        text="Service",
        variable=scope_var,
        value="service"
    ).grid(row=0, column=3)

    tk.Radiobutton(
        search_frame,
        text="Both",
        variable=scope_var,
        value="both"
    ).grid(row=0, column=4)

    # ==========================
    # SUGGESTIONS
    # ==========================

    suggestion_box = tk.Listbox(
        win,
        height=5
    )

    suggestion_box.pack(
        fill="x",
        padx=10
    )

    def show_suggestions(event):

        keyword = e_search.get().strip()

        suggestion_box.delete(
            0,
            tk.END
        )

        if len(keyword) < 3:
            return

        try:

            result = search_module.handle({

                "keyword": keyword,

                "scope": "both"

            })

            names = set()

            if result.get("sales"):

                for row in result["sales"]:

                    if row.get(
                        "customer_name"
                    ):

                        names.add(
                            row["customer_name"]
                        )

            if result.get("services"):

                for row in result["services"]:

                    if row.get(
                        "customer_name"
                    ):

                        names.add(
                            row["customer_name"]
                        )

            for item in sorted(names):

                suggestion_box.insert(
                    tk.END,
                    item
                )

        except Exception:
            pass

    e_search.bind(
        "<KeyRelease>",
        show_suggestions
    )

    def select_suggestion(event):

        selected = suggestion_box.curselection()

        if not selected:
            return

        value = suggestion_box.get(
            selected[0]
        )

        e_search.delete(
            0,
            tk.END
        )

        e_search.insert(
            0,
            value
        )

    suggestion_box.bind(
        "<<ListboxSelect>>",
        select_suggestion
    )

    # ==========================
    # RESULT TABLE
    # ==========================

    columns = (
        "Type",
        "ID",
        "Customer",
        "Mobile",
        "Model",
        "IMEI",
        "Status"
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
            width=130
        )

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # ==========================
    # SEARCH FUNCTION
    # ==========================

    def do_search():

        keyword = e_search.get().strip()

        if not keyword:

            messagebox.showwarning(
                "Warning",
                "Enter Search Keyword"
            )

            return

        tree.delete(
            *tree.get_children()
        )

        result = search_module.handle({

            "keyword": keyword,

            "scope": scope_var.get()

        })

        if result.get("status") != "success":

            messagebox.showerror(
                "Error",
                result.get("message")
            )

            return

        # SALES

        if result.get("scope") == "sales":

            for row in result["results"]:

                tree.insert(
                    "",
                    tk.END,
                    values=(

                        "SALE",

                        row.get("invoice_no"),

                        row.get("customer_name"),

                        row.get("mobile_number"),

                        row.get("model"),

                        row.get("imei"),

                        "Completed"
                    )
                )

        # SERVICE

        elif result.get("scope") == "service":

            for row in result["results"]:

                tree.insert(
                    "",
                    tk.END,
                    values=(

                        "SERVICE",

                        row.get("job_no"),

                        row.get("customer_name"),

                        row.get("mobile_number"),

                        row.get("model"),

                        row.get("imei"),

                        row.get("status")
                    )
                )

        # BOTH

        else:

            for row in result.get(
                "sales",
                []
            ):

                tree.insert(
                    "",
                    tk.END,
                    values=(

                        "SALE",

                        row.get("invoice_no"),

                        row.get("customer_name"),

                        row.get("mobile_number"),

                        row.get("model"),

                        row.get("imei"),

                        "Completed"
                    )
                )

            for row in result.get(
                "services",
                []
            ):

                tree.insert(
                    "",
                    tk.END,
                    values=(

                        "SERVICE",

                        row.get("job_no"),

                        row.get("customer_name"),

                        row.get("mobile_number"),

                        row.get("model"),

                        row.get("imei"),

                        row.get("status")
                    )
                )

    # ==========================
    # BUTTONS
    # ==========================

    btn_frame = tk.Frame(win)

    btn_frame.pack(
        fill="x",
        pady=5
    )

    tk.Button(
        btn_frame,
        text="Search",
        bg="green",
        fg="white",
        command=do_search
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        btn_frame,
        text="Clear",
        command=lambda: (
            e_search.delete(
                0,
                tk.END
            ),
            tree.delete(
                *tree.get_children()
            )
        )
    ).pack(
        side="left",
        padx=5
    )

    if not parent:
        win.mainloop()


if __name__ == "__main__":

    open_search_window()