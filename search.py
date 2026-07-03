# modules/search.py

import logging
from database import get_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("modules.search")


def search_sales(keyword, limit=100):

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM sales
            WHERE
                customer_name LIKE ?
                OR mobile_number LIKE ?
                OR product_name LIKE ?
                OR brand LIKE ?
                OR model LIKE ?
                OR imei LIKE ?
            ORDER BY id DESC
            LIMIT ?
        """, (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            limit
        ))

        return [dict(row) for row in cur.fetchall()]

    except Exception as e:
        logger.exception("Sales Search Failed")
        return []

    finally:
        conn.close()


def search_service(keyword, limit=100):

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM services
            WHERE
                customer_name LIKE ?
                OR mobile_number LIKE ?
                OR imei LIKE ?
                OR complaint LIKE ?
                OR brand LIKE ?
                OR model LIKE ?
            ORDER BY id DESC
            LIMIT ?
        """, (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            limit
        ))

        return [dict(row) for row in cur.fetchall()]

    except Exception as e:
        logger.exception("Service Search Failed")
        return []

    finally:
        conn.close()


def get_suggestions(keyword):

    conn = get_connection()

    try:

        cur = conn.cursor()

        suggestions = set()

        cur.execute("""
            SELECT DISTINCT customer_name
            FROM sales
            WHERE customer_name LIKE ?
            LIMIT 5
        """, (f"{keyword}%",))

        for row in cur.fetchall():
            suggestions.add(row["customer_name"])

        cur.execute("""
            SELECT DISTINCT customer_name
            FROM services
            WHERE customer_name LIKE ?
            LIMIT 5
        """, (f"{keyword}%",))

        for row in cur.fetchall():
            suggestions.add(row["customer_name"])

        return sorted(suggestions)

    except Exception as e:
        logger.exception("Suggestion Search Failed")
        return []

    finally:
        conn.close()


def handle(payload):

    try:

        keyword = str(payload.get("keyword", "")).strip()

        if not keyword:
            return {
                "status": "error",
                "message": "Search keyword required"
            }

        scope = str(payload.get("scope", "both")).lower()
        limit = int(payload.get("limit", 100))

        sales_results = []
        service_results = []

        if scope in ("sales", "both"):
            sales_results = search_sales(keyword, limit)

        if scope in ("service", "both"):
            service_results = search_service(keyword, limit)

        if scope == "sales":
            return {
                "status": "success",
                "scope": "sales",
                "results": sales_results,
                "count": len(sales_results)
            }

        if scope == "service":
            return {
                "status": "success",
                "scope": "service",
                "results": service_results,
                "count": len(service_results)
            }

        return {
            "status": "success",
            "scope": "both",
            "sales": sales_results,
            "service": service_results,
            "sales_count": len(sales_results),
            "service_count": len(service_results)
        }

    except Exception as e:

        logger.exception("Search Failed")

        return {
            "status": "error",
            "message": str(e)
        }


if __name__ == "__main__":

    print(handle({
        "keyword": "test",
        "scope": "both"
    }))