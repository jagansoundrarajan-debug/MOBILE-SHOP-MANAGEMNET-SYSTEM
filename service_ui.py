# ==========================================
# ui/service_ui.py
# PART 1
# ==========================================

import tkinter as tk
from tkinter import ttk, messagebox

from modules import service as service_module


def open_service_window(parent=None):

    # ===============================
    # WINDOW
    # ===============================

    if parent:
        win = tk.Toplevel(parent)
    else:
        win = tk.Tk()

    win.title("JAYAM MOBILES - SERVICE ENTRY")
    win.geometry("1200x750")
    win.configure(bg="white")

    # ===============================
    # TITLE
    # ===============================

    title = tk.Label(

        win,

        text="JAYAM MOBILES SERVICE ENTRY",

        font=("Arial",20,"bold"),

        fg="blue",

        bg="white"

    )

    title.pack(pady=10)

    # ===============================
    # MAIN CONTAINER
    # ===============================

    main_frame = tk.Frame(
        win,
        bg="white"
    )

    main_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=5
    )

    # LEFT PANEL

    left_frame = tk.Frame(
        main_frame,
        bg="white"
    )

    left_frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

    # RIGHT PANEL

    right_frame = tk.Frame(
        main_frame,
        bg="white"
    )

    right_frame.pack(
        side="right",
        fill="both",
        expand=True,
        padx=5
    )

    # ===============================
    # CUSTOMER DETAILS
    # ===============================

    customer_frame = tk.LabelFrame(

        left_frame,

        text="Customer Details",

        font=("Arial",11,"bold"),

        padx=10,

        pady=10

    )

    customer_frame.pack(
        fill="x",
        pady=5
    )

    tk.Label(
        customer_frame,
        text="Customer Name"
    ).grid(row=0,column=0,sticky="w",pady=5)

    e_customer = tk.Entry(
        customer_frame,
        width=35
    )

    e_customer.grid(
        row=0,
        column=1,
        padx=10
    )

    tk.Label(
        customer_frame,
        text="Mobile Number"
    ).grid(row=1,column=0,sticky="w",pady=5)

    e_mobile = tk.Entry(
        customer_frame,
        width=35
    )

    e_mobile.grid(
        row=1,
        column=1,
        padx=10
    )

    tk.Label(
        customer_frame,
        text="Email"
    ).grid(row=2,column=0,sticky="w",pady=5)

    e_email = tk.Entry(
        customer_frame,
        width=35
    )

    e_email.grid(
        row=2,
        column=1,
        padx=10
    )

    tk.Label(
        customer_frame,
        text="Address"
    ).grid(row=3,column=0,sticky="w",pady=5)

    e_address = tk.Entry(
        customer_frame,
        width=35
    )

    e_address.grid(
        row=3,
        column=1,
        padx=10
    )
    # ==========================================
    # DEVICE DETAILS
    # ==========================================

    device_frame = tk.LabelFrame(

        left_frame,

        text="Device Details",

        font=("Arial",11,"bold"),

        padx=10,

        pady=10

    )

    device_frame.pack(
        fill="x",
        pady=10
    )

    # Brand

    tk.Label(
        device_frame,
        text="Brand"
    ).grid(
        row=0,
        column=0,
        sticky="w",
        pady=5
    )

    e_brand = tk.Entry(
        device_frame,
        width=35
    )

    e_brand.grid(
        row=0,
        column=1,
        padx=10
    )

    # Model

    tk.Label(
        device_frame,
        text="Model"
    ).grid(
        row=1,
        column=0,
        sticky="w",
        pady=5
    )

    e_model = tk.Entry(
        device_frame,
        width=35
    )

    e_model.grid(
        row=1,
        column=1,
        padx=10
    )

    # IMEI Number

    tk.Label(
        device_frame,
        text="IMEI Number"
    ).grid(
        row=2,
        column=0,
        sticky="w",
        pady=5
    )

    e_imei = tk.Entry(
        device_frame,
        width=35
    )

    e_imei.grid(
        row=2,
        column=1,
        padx=10
    )

    # ==========================================
    # LOCK TYPE
    # ==========================================

    tk.Label(
        device_frame,
        text="Lock Type"
    ).grid(
        row=3,
        column=0,
        sticky="nw",
        pady=5
    )

    lock_type = tk.StringVar(
        value="No Lock"
    )

    lock_frame = tk.Frame(
        device_frame
    )

    lock_frame.grid(
        row=3,
        column=1,
        sticky="w"
    )

    tk.Radiobutton(

        lock_frame,

        text="No Lock",

        variable=lock_type,

        value="No Lock"

    ).pack(anchor="w")

    tk.Radiobutton(

        lock_frame,

        text="Pattern Lock",

        variable=lock_type,

        value="Pattern Lock"

    ).pack(anchor="w")

    tk.Radiobutton(

        lock_frame,

        text="PIN Lock",

        variable=lock_type,

        value="PIN Lock"

    ).pack(anchor="w")

    tk.Radiobutton(

        lock_frame,

        text="Password",

        variable=lock_type,

        value="Password"

    ).pack(anchor="w")

    # ==========================================
    # LOCK VALUE
    # ==========================================

    tk.Label(
        device_frame,
        text="Lock Value"
    ).grid(
        row=4,
        column=0,
        sticky="w",
        pady=5
    )

    e_lock_value = tk.Entry(
        device_frame,
        width=35,
        show="*"
    )

    e_lock_value.grid(
        row=4,
        column=1,
        padx=10
    )

    # ==========================================
    # SERVICE DETAILS
    # ==========================================

    service_frame = tk.LabelFrame(

        right_frame,

        text="Service Details",

        font=("Arial",11,"bold"),

        padx=10,

        pady=10

    )

    service_frame.pack(
        fill="x",
        pady=5
    )

    # Complaint

    tk.Label(
        service_frame,
        text="Complaint"
    ).grid(
        row=0,
        column=0,
        sticky="nw",
        pady=5
    )

    txt_complaint = tk.Text(
        service_frame,
        width=35,
        height=3
    )

    txt_complaint.grid(
        row=0,
        column=1,
        padx=10
    )

    # Technician

    tk.Label(
        service_frame,
        text="Technician"
    ).grid(
        row=1,
        column=0,
        sticky="w",
        pady=5
    )

    e_technician = tk.Entry(
        service_frame,
        width=35
    )

    e_technician.grid(
        row=1,
        column=1,
        padx=10
    )

    # Work Done

    tk.Label(
        service_frame,
        text="        Work Done"
    ).grid(
        row=2,
        column=0,
        sticky="nw",
        pady=5
    )

    txt_work_done = tk.Text(
        service_frame,
        width=35,
        height=3
    )

    txt_work_done.grid(
        row=2,
        column=1,
        padx=10
    )

    # Spare Parts Changed

    tk.Label(
        service_frame,
        text="Spare Parts Changed"
    ).grid(
        row=3,
        column=0,
        sticky="nw",
        pady=5
    )

    txt_spare_parts = tk.Text(
        service_frame,
        width=35,
        height=3
    )

    txt_spare_parts.grid(
        row=3,
        column=1,
        padx=10
    )

    # Estimated Cost

    tk.Label(
        service_frame,
        text="Estimated Cost (₹)"
    ).grid(
        row=4,
        column=0,
        sticky="w",
        pady=5
    )

    e_estimation = tk.Entry(
        service_frame,
        width=35
    )

    e_estimation.grid(
        row=4,
        column=1,
        padx=10
    )

    # Estimated Delivery Date

    tk.Label(
        service_frame,
        text="Estimated Delivery Date"
    ).grid(
        row=5,
        column=0,
        sticky="w",
        pady=5
    )

    e_delivery = tk.Entry(
        service_frame,
        width=35
    )

    e_delivery.grid(
        row=5,
        column=1,
        padx=10
    )

    # Service Charge

    tk.Label(
        service_frame,
        text="Service Charge (₹)"
    ).grid(
        row=6,
        column=0,
        sticky="w",
        pady=5
    )

    e_charge = tk.Entry(
        service_frame,
        width=35
    )

    e_charge.grid(
        row=6,
        column=1,
        padx=10
    )

    # Status

    tk.Label(
        service_frame,
        text="Status"
    ).grid(
        row=7,
        column=0,
        sticky="w",
        pady=5
    )

    status_var = tk.StringVar(value="Received")

    status_combo = ttk.Combobox(
        service_frame,
        textvariable=status_var,
        width=32,
        state="readonly",
        values=[
            "Received",
            "Inspection",
            "Waiting Approval",
            "Approved",
            "Repairing",
            "Completed",
            "Delivered"
        ]
    )

    status_combo.grid(
        row=7,
        column=1,
        padx=10,
        pady=5
    )

    status_combo.current(0)

    def clear_form():

        e_customer.delete(0, tk.END)
        e_mobile.delete(0, tk.END)
        e_email.delete(0, tk.END)
        e_address.delete(0, tk.END)

        e_brand.delete(0, tk.END)
        e_model.delete(0, tk.END)
        e_imei.delete(0, tk.END)

        e_lock_value.delete(0, tk.END)

        txt_complaint.delete("1.0", tk.END)
        txt_work_done.delete("1.0", tk.END)
        txt_spare_parts.delete("1.0", tk.END)

        e_technician.delete(0, tk.END)

        e_estimation.delete(0, tk.END)
        e_delivery.delete(0, tk.END)
        e_charge.delete(0, tk.END)

        status_combo.current(0)

        lock_type.set("No Lock")

        e_customer.focus()

    def save_service():

        payload = {

            "customer_name": e_customer.get().strip(),

            "mobile_number": e_mobile.get().strip(),

            "email": e_email.get().strip(),

            "address": e_address.get().strip(),

            "brand": e_brand.get().strip(),

            "model": e_model.get().strip(),

            "imei": e_imei.get().strip(),

            "lock_type": lock_type.get(),

            "lock_value": e_lock_value.get().strip(),

            "complaint": txt_complaint.get(
                "1.0",
                tk.END
            ).strip(),

            "technician": e_technician.get().strip(),

            "work_done": txt_work_done.get(
                "1.0",
                tk.END
            ).strip(),

            "spare_parts": txt_spare_parts.get(
                "1.0",
                tk.END
            ).strip(),

            "estimation_amount": e_estimation.get().strip(),

            "estimated_delivery_date": e_delivery.get().strip(),

            "service_charge": e_charge.get().strip(),

            "status": status_var.get()

        }

        result = service_module.handle(payload)

        if result["status"] == "success":

            messagebox.showinfo(

                "Success",

                f"Job No : {result['job_no']}\n\n"
                "Service Saved Successfully.\n"
                "PDF Generated Successfully."

            )

            clear_form()

        else:

            messagebox.showerror(

                "Error",

                result["message"]

            )

    # ==========================================
    # KEYBOARD SHORTCUTS
    # ==========================================

    win.bind(

        "<Control-s>",

        lambda event: save_service()

    )
    win.bind(

         "<Escape>",

         lambda event: clear_form()

    )

    # DEFAULT VALUES

    status_combo.current(0)

    lock_type.set("No Lock")

    e_customer.focus()

    e_customer.focus()
    # ==========================================
    # BUTTONS
    # ==========================================

    button_frame = tk.Frame(right_frame, bg="white")

    button_frame.pack(
        pady=20
    )

    tk.Button(
        button_frame,
        text="Save & Generate PDF",
        width=22,
        bg="green",
        fg="white",
        font=("Arial", 10, "bold"),
        command=save_service
    ).grid(
        row=0,
        column=0,
        padx=10
    )

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
        column=1,
        padx=10
    )

    # ==========================================
    # MAIN LOOP
    # ==========================================

    if not parent:

        win.mainloop()


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    open_service_window()