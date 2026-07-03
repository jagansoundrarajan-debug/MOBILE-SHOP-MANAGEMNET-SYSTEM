# ==========================================
# modules/service.py
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

SERVICE_PDF_DIR = os.path.join(
    BASE_DIR,
    "service_receipts"
)

os.makedirs(
    SERVICE_PDF_DIR,
    exist_ok=True
)

# ==========================================
# N8N WEBHOOK
# ==========================================

# Development
N8N_WEBHOOK = "http://localhost:5678/webhook-test/mobile-sale"

# Production
# N8N_WEBHOOK = "http://localhost:5678/webhook/mobile-service"

# ==========================================
# GENERATE JOB NUMBER
# ==========================================

def generate_job_no():

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute(
            "SELECT COUNT(*) FROM services"
        )

        count = cur.fetchone()[0] + 1

        return f"JOB{count:04d}"

    finally:

        conn.close()
# ==========================================
# SEND DATA TO N8N
# ==========================================

def send_to_n8n(

        action,
        job_no,
        customer_name,
        mobile_number,
        email,
        complaint,
        service_charge,
        pdf_path,
        status
):

    payload = {
        "action":"service",

        "job_no": job_no,

        "customer_name": customer_name,

        "mobile_number": mobile_number,

        "email": email,

        "complaint": complaint,

        "service_charge": service_charge,

        "status": status,

        "pdf_path": pdf_path

    }

    try:

        response = requests.post(

            N8N_WEBHOOK,

            json=payload,

            timeout=10

        )

        logger.info(
            "N8N Status : %s",
            response.status_code
        )

    except Exception as e:

        logger.error(e)


# ==========================================
# GENERATE PDF
# ==========================================

def generate_pdf(
        job_no,
        data
):

    pdf_path = os.path.join(

        SERVICE_PDF_DIR,

        f"{job_no}.pdf"

    )

    pdf = FPDF()

    pdf.add_page()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    # ======================================
    # TITLE
    # ======================================

    pdf.set_font(
        "Arial",
        "B",
        18
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
        "SERVICE RECEIPT",
        ln=True,
        align="C"
    )

    pdf.ln(5)

    pdf.cell(
        95,
        8,
        f"Job No : {job_no}"
    )

    pdf.cell(
        95,
        8,
        f"Date : {data['received_date']}",
        ln=True
    )

    pdf.ln(5)

    pdf.line(
        10,
        pdf.get_y(),
        200,
        pdf.get_y()
    )

    pdf.ln(5)

    # ======================================
    # CUSTOMER DETAILS
    # ======================================

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        190,
        8,
        "CUSTOMER DETAILS",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        11
    )

    pdf.cell(
        190,
        7,
        f"Customer : {data['customer_name']}",
        ln=True
    )

    pdf.cell(
        190,
        7,
        f"Mobile : {data['mobile_number']}",
        ln=True
    )

    pdf.cell(
        190,
        7,
        f"Email : {data['email']}",
        ln=True
    )

    pdf.cell(
        190,
        7,
        f"Address : {data['address']}",
        ln=True
    )

    pdf.ln(5)

    # ======================================
    # DEVICE DETAILS
    # ======================================

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        190,
        8,
        "DEVICE DETAILS",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        11
    )

    pdf.cell(
        190,
        7,
        f"Brand : {data['brand']}",
        ln=True
    )

    pdf.cell(
        190,
        7,
        f"Model : {data['model']}",
        ln=True
    )

    pdf.cell(
        190,
        7,
        f"IMEI : {data['imei']}",
        ln=True
    )

    pdf.cell(
        190,
        7,
        f"Lock Type : {data['lock_type']}",
        ln=True
    )

    pdf.cell(
        190,
        7,
        f"Lock Value : {data['lock_value']}",
        ln=True
    )

    pdf.ln(5)

    # ======================================
    # SERVICE DETAILS
    # ======================================

    pdf.set_font("Arial", "B", 12)

    pdf.cell(
        190,
        8,
        "SERVICE DETAILS",
        ln=True
    )

    pdf.set_font("Arial", "", 11)

    pdf.multi_cell(
        190,
        7,
        f"Complaint : {data['complaint']}"
    )

    pdf.multi_cell(
        190,
        7,
        f"Work Done : {data['work_done']}"
    )

    pdf.multi_cell(
        190,
        7,
        f"Spare Parts : {data['spare_parts']}"
    )

    pdf.cell(
        190,
        7,
        f"Technician : {data['technician']}",
        ln=True
    )

    pdf.cell(
        190,
        7,
        f"Estimated Cost : {data['estimation_amount']}",
        ln=True
    )

    pdf.cell(
        190,
        7,
        f"Estimated Delivery : {data['estimated_delivery_date']}",
        ln=True
    )

    pdf.cell(
        190,
        7,
        f"Service Charge : {data['service_charge']}",
        ln=True
    )

    pdf.cell(
        190,
        7,
        f"Status : {data['status']}",
        ln=True
    )

    pdf.output(pdf_path)

    return pdf_path


# ==========================================
# HANDLE SERVICE
# ==========================================

def handle(payload):
    try:
        job_no = generate_job_no()

        received_date = datetime.now().strftime("%d-%m-%Y")

        pdf_path = ""

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("""

            INSERT INTO services(

                job_no,

                customer_name,

                mobile_number,

                email,

                address,

                brand,

                model,

                imei,

                lock_type,

                lock_value,

                complaint,

                technician,

                work_done,

                spare_parts,

                estimation_amount,

                estimated_delivery_date,

                service_charge,

                status,

                received_date,

                pdf_path,

                created_at

            )

            VALUES(

                ?,?,?,?,?,?,
                ?,?,?,?,
                ?,?,?,?,
                ?,?,?,?,
                ?,?,?

            )

            """, (


            job_no,

            payload["customer_name"],

            payload["mobile_number"],

            payload["email"],

            payload["address"],

            payload["brand"],

            payload["model"],

            payload["imei"],

            payload["lock_type"],

            payload["lock_value"],

            payload["complaint"],

            payload["technician"],

            payload["work_done"],

            payload["spare_parts"],

            payload["estimation_amount"],

            payload["estimated_delivery_date"],

            payload["service_charge"],

            payload["status"],

            received_date,

            pdf_path,

            datetime.now().isoformat()

        ))

        conn.commit()
        conn.close()
        # ======================================
        # GENERATE PDF
        # ======================================

        pdf_path = generate_pdf(

            job_no,

            {

                **payload,

                "received_date": received_date

            }

        )

        # ======================================
        # UPDATE PDF PATH
        # ======================================

        conn = get_connection()

        try:

            cur = conn.cursor()

            cur.execute(

                """

                UPDATE services

                SET pdf_path=?

                WHERE job_no=?

                """,

                (

                    pdf_path,

                    job_no

                )

            )

            conn.commit()

        finally:

            conn.close()


        # ======================================
        # SEND DATA TO N8N
        # ======================================

        send_to_n8n(
            "service",
            job_no,
            payload["customer_name"],
            payload["mobile_number"],
            payload["email"],
            payload["complaint"],
            payload["service_charge"],
            pdf_path,
            payload["status"]
        )


        # ======================================
        # RETURN SUCCESS
        # ======================================

        return {

            "status": "success",

            "message": "Service Saved Successfully",

            "job_no": job_no,

            "customer_name": payload["customer_name"],

            "pdf": pdf_path

        }


    except Exception as e:

        logger.exception(e)

        # Send error to n8n

        try:

            requests.post(

                N8N_WEBHOOK,

                json={

                    "action": "error",

                    "module": "service",

                    "error": str(e)

                },

                timeout=5

            )

        except:

            pass

        return {

            "status": "error",

            "message": str(e)

        }

try:
    raise Exception("Test Error from Service Module")

except Exception as e:
    payload = {
        "action": "error",
        "module": "service",
        "error": str(e)
    }

    requests.post(N8N_WEBHOOK, json=payload)
