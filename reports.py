# modules/reports.py

from database import get_connection


def gather_reports():

    conn = get_connection()

    try:

        cur = conn.cursor()

        # Total Sales
        cur.execute("SELECT COUNT(*) AS cnt FROM sales")
        total_sales = cur.fetchone()["cnt"]

        # Total Services
        cur.execute("SELECT COUNT(*) AS cnt FROM services")
        total_services = cur.fetchone()["cnt"]

        # Revenue
        cur.execute("""
            SELECT IFNULL(SUM(grand_total),0) AS total
            FROM sales
        """)
        total_revenue = cur.fetchone()["total"]

        # Pending Services
        cur.execute("""
            SELECT COUNT(*) AS cnt
            FROM services
            WHERE status='Pending'
        """)
        pending_services = cur.fetchone()["cnt"]

        # Inventory Count
        cur.execute("""
            SELECT COUNT(*) AS cnt
            FROM inventory
        """)
        inventory_count = cur.fetchone()["cnt"]

        # Recent Sales
        cur.execute("""
            SELECT
                invoice_no,
                customer_name,
                product_name,
                grand_total,
                sale_date
            FROM sales
            ORDER BY id DESC
            LIMIT 10
        """)

        recent_sales = [
            dict(row)
            for row in cur.fetchall()
        ]

        # Recent Services
        cur.execute("""
            SELECT
                job_no,
                customer_name,
                complaint,
                status,
                receive_date
            FROM services
            ORDER BY id DESC
            LIMIT 10
        """)

        recent_services = [
            dict(row)
            for row in cur.fetchall()
        ]

        return {

            "status": "success",

            "total_sales": total_sales,

            "total_services": total_services,

            "total_revenue": float(total_revenue),

            "pending_services": pending_services,

            "inventory_count": inventory_count,

            "recent_sales": recent_sales,

            "recent_services": recent_services

        }

    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }

    finally:

        conn.close()


def handle(payload):

    return gather_reports()


if __name__ == "__main__":

    print(handle({}))