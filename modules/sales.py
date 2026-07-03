# ==========================================
# modules/sales.py
# PART 1
# ==========================================

import os
import logging
from datetime import datetime

import requests
from fpdf import FPDF

from database import get_connection

# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

INVOICE_DIR = os.path.join(
    BASE_DIR,
    "invoices"
)

os.makedirs(INVOICE_DIR, exist_ok=True)

# ==========================================
# N8N WEBHOOK
# ==========================================

# Testing
N8N_WEBHOOK = "http://localhost:5678/webhook-test/mobile-sale"

# Production
# N8N_WEBHOOK = "http://localhost:5678/webhook/mobile-sale"

# ==========================================
# GENERATE INVOICE NUMBER
# ==========================================

def generate_invoice_no():

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute(
            "SELECT COUNT(*) FROM sales"
        )

        count = cur.fetchone()[0] + 1

        return f"INV{count:04d}"

    finally:

        conn.close()

# ==========================================
# GENERATE PDF
# ==========================================

def generate_pdf(invoice_no, data):

    pdf_path = os.path.join(
        INVOICE_DIR,
        f"{invoice_no}.pdf"
    )

    pdf = FPDF()

    pdf.add_page()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.set_font(
        "Arial",
        "B",
        16
    )

    pdf.cell(
        190,
        10,
        "JAYAM MOBILES",
        ln=True,
        align="C"
    )

    pdf.set_font(
        "Arial",
        "",
        12
    )

    pdf.cell(
        190,
        8,
        "SALES INVOICE",
        ln=True,
        align="C"
    )

    pdf.ln(5)

    pdf.cell(
        95,
        8,
        f"Invoice : {invoice_no}"
    )

    pdf.cell(
        95,
        8,
        f"Date : {data['sale_date']}",
        ln=True
    )

    pdf.ln(5)

    pdf.cell(
        190,
        8,
        f"Customer : {data['customer_name']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Mobile : {data['mobile_number']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Email : {data['email']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Address : {data['address']}",
        ln=True
    )

    pdf.ln(5)
    # ==========================================
    # PRODUCT DETAILS
    # ==========================================

    pdf.cell(
        190,
        8,
        f"Product : {data['product_name']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Brand : {data['brand']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Model : {data['model']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"IMEI : {data['imei']}",
        ln=True
    )

    pdf.ln(5)

    # ==========================================
    # BILL DETAILS
    # ==========================================

    pdf.cell(
        190,
        8,
        f"Quantity : {data['qty']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Rate : {data['rate']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Subtotal : {data['subtotal']:.2f}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"GST : {data['gst']:.2f}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Grand Total : {data['grand_total']:.2f}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Warranty : {data['warranty']}",
        ln=True
    )

    pdf.ln(15)

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        190,
        10,
        "Thank You! Visit Again.",
        ln=True,
        align="C"
    )

    pdf.output(pdf_path)

    return pdf_path


# ==========================================
# SAVE SALE
# ==========================================

def handle(payload):
    try:

        customer_name = payload["customer_name"].strip()

        mobile_number = payload["mobile_number"].strip()

        email = payload["email"].strip()

        qty = int(payload["qty"])

        rate = float(payload["rate"])

        gst_percent = float(payload["gst"])

        subtotal = qty * rate

        gst_amount = subtotal * gst_percent / 100

        grand_total = subtotal + gst_amount

        invoice_no = generate_invoice_no()

        sale_date = datetime.now().strftime("%d-%m-%Y")
        # ==========================================
        # SAVE TO DATABASE
        # ==========================================

        conn = get_connection()

        try:

            cur = conn.cursor()

            pdf_path = ""

            cur.execute(
                """
                INSERT INTO sales(

                    invoice_no,
                    customer_name,
                    mobile_number,
                    email,
                    address,

                    product_name,
                    brand,
                    model,
                    imei,

                    qty,
                    rate,
                    subtotal,
                    gst,
                    grand_total,

                    warranty,

                    sale_date,

                    pdf_path,

                    created_at

                )

                VALUES(

                    ?,?,?,?,?,?,
                    ?,?,?,?,
                    ?,?,?,?,
                    ?,?,?,?

                )
                """,

                (

                    invoice_no,

                    customer_name,

                    mobile_number,

                    email,

                    payload["address"],

                    payload["product_name"],

                    payload["brand"],

                    payload["model"],

                    payload["imei"],

                    qty,

                    rate,

                    subtotal,

                    gst_amount,

                    grand_total,

                    payload["warranty"],

                    sale_date,

                    pdf_path,

                    datetime.now().isoformat()

                )

            )

            conn.commit()

        finally:

            conn.close()

        # ==========================================
        # GENERATE PDF
        # ==========================================

        pdf_path = generate_pdf(

            invoice_no,

            {

                **payload,

                "qty": qty,

                "rate": rate,

                "subtotal": subtotal,

                "gst": gst_amount,

                "grand_total": grand_total,

                "sale_date": sale_date

            }

        )

        # ==========================================
        # UPDATE PDF PATH
        # ==========================================

        conn = get_connection()

        try:

            cur = conn.cursor()

            cur.execute(

                """

                UPDATE sales

                SET pdf_path=?

                WHERE invoice_no=?

                """,

                (

                    pdf_path,

                    invoice_no

                )

            )

            conn.commit()

        finally:

            conn.close()

        # ==========================================
        # SEND TO N8N
        # ==========================================

        payload_n8n = {
            "action": "sales",

            "invoice_no": invoice_no,

            "customer_name": customer_name,

            "mobile_number": mobile_number,

            "email": email,

            "product_name": payload["product_name"],

            "amount": grand_total,

            "pdf_path": pdf_path

        }

        try:

            response = requests.post(

                N8N_WEBHOOK,

                json=payload_n8n,

                timeout=10

            )

            logger.info(

                "N8N Status : %s",

                response.status_code

            )

        except Exception as e:

            logger.error(

                "N8N Error : %s",

                e

            )

        # ==========================================
        # RETURN SUCCESS
        # ==========================================

        return {

            "status": "success",

            "message": "Sale Saved Successfully",

            "invoice_no": invoice_no,

            "customer_name": customer_name,

            "grand_total": grand_total,

            "pdf": pdf_path

        }

    except Exception as e:

        logger.exception(e)

        return {

            "status": "error",

            "message": str(e)

        }
