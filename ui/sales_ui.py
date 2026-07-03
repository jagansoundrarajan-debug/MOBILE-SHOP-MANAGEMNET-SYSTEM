# ==========================================
# ui/sales_ui.py
# PART 1
# ==========================================

import tkinter as tk
from tkinter import messagebox

from modules import sales as sales_module


def open_sales_window(parent=None):

    # ======================================
    # MAIN WINDOW
    # ======================================

    if parent:
        win = tk.Toplevel(parent)
    else:
        win = tk.Tk()

    win.title("JAYAM MOBILES - Sales Billing")
    win.geometry("900x850")
    win.resizable(False, False)

    # ======================================
    # TITLE
    # ======================================

    title = tk.Label(
        win,
        text="JAYAM MOBILES SALES BILLING",
        font=("Arial", 18, "bold"),
        fg="blue"
    )

    title.pack(pady=10)

    # ======================================
    # CUSTOMER DETAILS
    # ======================================

    customer_frame = tk.LabelFrame(
        win,
        text="Customer Details",
        padx=10,
        pady=10,
        font=("Arial", 11, "bold")
    )

    customer_frame.pack(
        fill="x",
        padx=10,
        pady=5
    )

    # Customer Name

    tk.Label(
        customer_frame,
        text="Customer Name"
    ).grid(
        row=0,
        column=0,
        sticky="w",
        pady=5
    )

    e_customer = tk.Entry(
        customer_frame,
        width=40
    )

    e_customer.grid(
        row=0,
        column=1,
        padx=10
    )

    # Mobile Number

    tk.Label(
        customer_frame,
        text="Mobile Number"
    ).grid(
        row=1,
        column=0,
        sticky="w",
        pady=5
    )

    e_mobile = tk.Entry(
        customer_frame,
        width=40
    )

    e_mobile.grid(
        row=1,
        column=1,
        padx=10
    )

    # Email Address

    tk.Label(
        customer_frame,
        text="Email Address"
    ).grid(
        row=2,
        column=0,
        sticky="w",
        pady=5
    )

    e_email = tk.Entry(
        customer_frame,
        width=40
    )

    e_email.grid(
        row=2,
        column=1,
        padx=10
    )

    # Address

    tk.Label(
        customer_frame,
        text="Address"
    ).grid(
        row=3,
        column=0,
        sticky="w",
        pady=5
    )

    e_address = tk.Entry(
        customer_frame,
        width=40
    )

    e_address.grid(
        row=3,
        column=1,
        padx=10
    )

    # ======================================
    # PRODUCT DETAILS
    # ======================================

    product_frame = tk.LabelFrame(
        win,
        text="Product Details",
        padx=10,
        pady=10,
        font=("Arial", 11, "bold")
    )

    product_frame.pack(
        fill="x",
        padx=10,
        pady=5
    )
    # ======================================
    # PRODUCT NAME
    # ======================================

    tk.Label(
        product_frame,
        text="Product Name"
    ).grid(row=0, column=0, sticky="w", pady=5)

    e_product = tk.Entry(
        product_frame,
        width=40
    )

    e_product.grid(row=0, column=1, padx=10)

    # ======================================
    # BRAND
    # ======================================

    tk.Label(
        product_frame,
        text="Brand"
    ).grid(row=1, column=0, sticky="w", pady=5)

    e_brand = tk.Entry(
        product_frame,
        width=40
    )

    e_brand.grid(row=1, column=1, padx=10)

    # ======================================
    # MODEL
    # ======================================

    tk.Label(
        product_frame,
        text="Model"
    ).grid(row=2, column=0, sticky="w", pady=5)

    e_model = tk.Entry(
        product_frame,
        width=40
    )

    e_model.grid(row=2, column=1, padx=10)

    # ======================================
    # IMEI
    # ======================================

    tk.Label(
        product_frame,
        text="IMEI Number"
    ).grid(row=3, column=0, sticky="w", pady=5)

    e_imei = tk.Entry(
        product_frame,
        width=40
    )

    e_imei.grid(row=3, column=1, padx=10)

    # ======================================
    # QUANTITY
    # ======================================

    tk.Label(
        product_frame,
        text="Quantity"
    ).grid(row=4, column=0, sticky="w", pady=5)

    e_qty = tk.Entry(
        product_frame,
        width=40
    )

    e_qty.insert(0, "1")

    e_qty.grid(row=4, column=1, padx=10)

    # ======================================
    # RATE
    # ======================================

    tk.Label(
        product_frame,
        text="Rate (₹)"
    ).grid(row=5, column=0, sticky="w", pady=5)

    e_rate = tk.Entry(
        product_frame,
        width=40
    )

    e_rate.grid(row=5, column=1, padx=10)

    # ======================================
    # GST
    # ======================================

    tk.Label(
        product_frame,
        text="GST (%)"
    ).grid(row=6, column=0, sticky="w", pady=5)

    e_gst = tk.Entry(
        product_frame,
        width=40
    )

    e_gst.insert(0, "18")

    e_gst.grid(row=6, column=1, padx=10)

    # ======================================
    # WARRANTY
    # ======================================

    tk.Label(
        product_frame,
        text="Warranty"
    ).grid(row=7, column=0, sticky="w", pady=5)

    warranty_var = tk.StringVar(value="1 Year")

    tk.OptionMenu(
        product_frame,
        warranty_var,
        "No Warranty",
        "3 Months",
        "6 Months",
        "1 Year",
        "2 Years"
    ).grid(
        row=7,
        column=1,
        sticky="w"
    )

    # ======================================
    # BILL SUMMARY
    # ======================================

    summary_frame = tk.LabelFrame(
        win,
        text="Bill Summary",
        padx=10,
        pady=10,
        font=("Arial", 11, "bold")
    )

    summary_frame.pack(
        fill="x",
        padx=10,
        pady=5
    )

    subtotal_var = tk.StringVar(value="0.00")
    gst_var = tk.StringVar(value="0.00")
    total_var = tk.StringVar(value="0.00")

    tk.Label(summary_frame, text="Subtotal").grid(row=0, column=0, sticky="w")
    tk.Label(summary_frame, textvariable=subtotal_var).grid(row=0, column=1)

    tk.Label(summary_frame, text="GST Amount").grid(row=1, column=0, sticky="w")
    tk.Label(summary_frame, textvariable=gst_var).grid(row=1, column=1)

    tk.Label(summary_frame, text="Grand Total").grid(row=2, column=0, sticky="w")
    tk.Label(
        summary_frame,
        textvariable=total_var,
        font=("Arial", 12, "bold"),
        fg="green"
    ).grid(row=2, column=1)
    # ======================================
    # FUNCTIONS
    # ======================================

    def calculate_total():

        try:

            qty = int(e_qty.get())

            rate = float(e_rate.get())

            gst_percent = float(e_gst.get())

            subtotal = qty * rate

            gst_amount = subtotal * gst_percent / 100

            grand_total = subtotal + gst_amount

            subtotal_var.set(f"{subtotal:.2f}")

            gst_var.set(f"{gst_amount:.2f}")

            total_var.set(f"{grand_total:.2f}")

        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter valid Quantity, Rate and GST."
            )

    # ======================================
    # EMAIL VALIDATION
    # ======================================

    def validate_email(email):

        if email == "":
            return True

        return (
            "@" in email
            and "." in email
        )

    # ======================================
    # SAVE SALE
    # ======================================

    def save_sale():

        calculate_total()

        if e_customer.get().strip() == "":

            messagebox.showerror(
                "Error",
                "Customer Name is required."
            )

            return

        if len(e_mobile.get().strip()) != 10:

            messagebox.showerror(
                "Error",
                "Enter a valid 10-digit mobile number."
            )

            return

        if not validate_email(e_email.get().strip()):

            messagebox.showerror(
                "Error",
                "Invalid Email Address."
            )

            return

        payload = {

            "customer_name": e_customer.get().strip(),

            "mobile_number": e_mobile.get().strip(),

            "email": e_email.get().strip(),

            "address": e_address.get().strip(),

            "product_name": e_product.get().strip(),

            "brand": e_brand.get().strip(),

            "model": e_model.get().strip(),

            "imei": e_imei.get().strip(),

            "qty": e_qty.get().strip(),

            "rate": e_rate.get().strip(),

            "gst": e_gst.get().strip(),

            "warranty": warranty_var.get()

        }

        result = sales_module.handle(payload)

        if result.get("status") == "success":

            messagebox.showinfo(

                "Sale Saved",

                f"Invoice No : {result['invoice_no']}\n\n"
                f"Customer : {result['customer_name']}\n"
                f"Grand Total : ₹{result['grand_total']}\n\n"
                f"Invoice PDF Generated Successfully."

            )

            clear_form()

        else:

            messagebox.showerror(

                "Error",

                result.get("message")

            )

    # ======================================
    # CLEAR FORM
    # ======================================

    def clear_form():

        e_customer.delete(0, tk.END)
        e_mobile.delete(0, tk.END)
        e_email.delete(0, tk.END)
        e_address.delete(0, tk.END)

        e_product.delete(0, tk.END)
        e_brand.delete(0, tk.END)
        e_model.delete(0, tk.END)
        e_imei.delete(0, tk.END)

        e_qty.delete(0, tk.END)
        e_qty.insert(0, "1")

        e_rate.delete(0, tk.END)

        e_gst.delete(0, tk.END)
        e_gst.insert(0, "18")

        warranty_var.set("1 Year")

        subtotal_var.set("0.00")
        gst_var.set("0.00")
        total_var.set("0.00")

        e_customer.focus()

    # ======================================
    # BUTTONS
    # ======================================

    button_frame = tk.Frame(win)

    button_frame.pack(pady=20)

        # Calculate Button

    tk.Button(

        button_frame,

        text="Calculate Total",

        width=20,

        bg="orange",

        fg="black",

        font=("Arial", 10, "bold"),

        command=calculate_total

    ).grid(
        row=0,
        column=0,
        padx=10
    )

        # Save Button

    tk.Button(

        button_frame,

        text="Save & Generate PDF",

        width=22,
        bg="green",

        fg="white",

        font=("Arial", 10, "bold"),

        command=save_sale

     ).grid(
        row=0,
        column=1,
        padx=10
    )

        # Clear Button

    tk.Button(

        button_frame,

        text="Clear",

        width=15,

        bg="red",

        fg="white",

        font=("Arial", 10, "bold"),

        command=clear_form

    ).grid(
        row=0,
        column=2,
        padx=10

    )



    win.bind(

        "<F5>",

        lambda event: calculate_total()

     )

    win.bind(

         "<Control-s>",

         lambda event: save_sale()

    )

    win.bind(

         "<Escape>",

        lambda event: clear_form()

    )


    e_customer.focus()

        # ======================================
        # MAIN LOOP
        # ======================================

    if not parent:
            win.mainloop()

    # ==========================================
    # MAIN
    # ==========================================

    if __name__ == "__main__":
        open_sales_window()
