# modules/analytics.py

from database import get_connection


def sales_summary():

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*) AS total_sales
            FROM sales
        """)

        total_sales = cur.fetchone()["total_sales"]

        cur.execute("""
            SELECT IFNULL(SUM(grand_total),0) AS revenue
            FROM sales
        """)

        revenue = cur.fetchone()["revenue"]

        return {
            "total_sales": total_sales,
            "revenue": float(revenue)
        }

    finally:

        conn.close()


def top_products():

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute("""
            SELECT
                product_name,
                SUM(qty) AS total_qty
            FROM sales
            GROUP BY product_name
            ORDER BY total_qty DESC
            LIMIT 10
        """)

        return [dict(row) for row in cur.fetchall()]

    finally:

        conn.close()


def top_brands():

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute("""
            SELECT
                brand,
                COUNT(*) AS total
            FROM sales
            GROUP BY brand
            ORDER BY total DESC
            LIMIT 10
        """)

        return [dict(row) for row in cur.fetchall()]

    finally:

        conn.close()


def service_status():

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute("""
            SELECT
                status,
                COUNT(*) AS total
            FROM services
            GROUP BY status
        """)

        return [dict(row) for row in cur.fetchall()]

    finally:

        conn.close()


def handle(payload):

    try:

        return {

            "status": "success",

            "sales_summary": sales_summary(),

            "top_products": top_products(),

            "top_brands": top_brands(),

            "service_status": service_status()

        }

    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }


if __name__ == "__main__":

    print(handle({}))