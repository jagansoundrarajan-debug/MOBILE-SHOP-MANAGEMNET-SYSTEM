import os
import sqlite3

# ==========================================
# DATABASE CONFIGURATION
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "mobile_shop.db")


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# ADD COLUMN IF NOT EXISTS
# ==========================================

def add_column_if_not_exists(cursor, table_name, column_name, column_type):

    cursor.execute(f"PRAGMA table_info({table_name})")

    columns = [row["name"] for row in cursor.fetchall()]

    if column_name not in columns:
        cursor.execute(
            f"ALTER TABLE {table_name} "
            f"ADD COLUMN {column_name} {column_type}"
        )


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def initialize_database():

    conn = get_connection()

    cur = conn.cursor()

    # ======================================
    # USERS
    # ======================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT,

        role TEXT

    )
    """)

    # ======================================
    # SALES
    # ======================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        invoice_no TEXT UNIQUE,

        customer_name TEXT,

        mobile_number TEXT,

        email TEXT,

        address TEXT,

        product_name TEXT,

        brand TEXT,

        model TEXT,

        imei TEXT,

        qty INTEGER,

        rate REAL,

        subtotal REAL,

        gst REAL,

        grand_total REAL,

        warranty TEXT,

        sale_date TEXT,

        pdf_path TEXT,

        created_at TEXT

    )
    """)

    # ======================================
    # SERVICES
    # ======================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS services(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        job_no TEXT UNIQUE,

        customer_name TEXT,

        mobile_number TEXT,

        email TEXT,

        address TEXT,

        brand TEXT,

        model TEXT,

        imei TEXT,

        device_password TEXT,

        accessories TEXT,

        complaint TEXT,

        technician TEXT,

        work_done TEXT,

        spare_parts TEXT,

        service_charge REAL,

        status TEXT,

        received_date TEXT,

        delivery_date TEXT,

        pdf_path TEXT,

        created_at TEXT

    )
    """)
    # Add missing columns if they don't exist
    add_column_if_not_exists(cur, "services", "lock_type", "TEXT")
    add_column_if_not_exists(cur, "services", "lock_value", "TEXT")
    add_column_if_not_exists(cur, "services", "estimation_amount", "REAL")
    add_column_if_not_exists(cur, "services", "estimated_delivery_date", "TEXT")
    add_column_if_not_exists(cur, "services", "email", "TEXT")
    add_column_if_not_exists(cur, "services", "pdf_path", "TEXT")
    add_column_if_not_exists(cur, "services", "email", "TEXT")
    add_column_if_not_exists(cur, "services", "lock_type", "TEXT")
    add_column_if_not_exists(cur, "services", "lock_value", "TEXT")
    add_column_if_not_exists(cur, "services", "estimation_amount", "REAL")
    add_column_if_not_exists(cur, "services", "estimated_delivery_date", "TEXT")
    add_column_if_not_exists(cur, "services", "received_date", "TEXT")
    add_column_if_not_exists(cur, "services", "delivery_date", "TEXT")
    add_column_if_not_exists(cur, "services", "pdf_path", "TEXT")

    # ======================================
    # INVENTORY
    # ======================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS inventory(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        brand TEXT,

        model TEXT,

        imei TEXT UNIQUE,

        purchase_price REAL,

        selling_price REAL,

        stock INTEGER

    )
    """)

    # ======================================
    # DATABASE UPGRADE
    # ======================================

    # Sales
    add_column_if_not_exists(cur, "sales", "email", "TEXT")
    add_column_if_not_exists(cur, "sales", "pdf_path", "TEXT")

    # Services
    add_column_if_not_exists(cur, "services", "email", "TEXT")
    add_column_if_not_exists(cur, "services", "pdf_path", "TEXT")

    conn.commit()

    conn.close()


# ==========================================
# INITIALIZE DATABASE
# ==========================================

if __name__ == "__main__":
    initialize_database()