# modules/inventory.py

from datetime import datetime
import requests

from database import get_connection

# ==============================
# n8n Webhook URL
# Replace with your actual webhook URL
# ==============================
WEBHOOK_URL = "http://localhost:5678/webhook-test/mobile-sale"


def add_stock(payload):

    conn = get_connection()

    try:

        cur = conn.cursor()

        purchase_price = float(payload.get("purchase_price", 0))
        selling_price = float(payload.get("selling_price", 0))
        quantity = int(payload.get("quantity", 0))

        cur.execute("""
            INSERT INTO inventory(
                product_name,
                brand,
                model,
                purchase_price,
                selling_price,
                quantity,
                created_at
            )
            VALUES(?,?,?,?,?,?,?)
        """, (

            payload.get("product_name"),

            payload.get("brand"),

            payload.get("model"),

            purchase_price,

            selling_price,

            quantity,

            datetime.now().isoformat()

        ))

        conn.commit()

        # ==========================
        # Send Inventory to n8n
        # ==========================
        try:

            requests.post(

                WEBHOOK_URL,

                json={

                    "action": "inventory",

                    "product_name": payload.get("product_name"),

                    "brand": payload.get("brand"),

                    "model": payload.get("model"),

                    "purchase_price": purchase_price,

                    "selling_price": selling_price,

                    "quantity": quantity,

                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                },

                timeout=5

            )

            print("Inventory sent to n8n successfully.")

        except Exception as e:

            print("n8n webhook error:", e)

        return {

            "status": "success",

            "message": "Stock Added Successfully"

        }

    except Exception as e:

        conn.rollback()

        return {

            "status": "error",

            "message": str(e)

        }

    finally:

        conn.close()


def list_stock():

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM inventory
            ORDER BY id DESC
        """)

        items = [dict(row) for row in cur.fetchall()]

        return {

            "status": "success",

            "items": items

        }

    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }

    finally:

        conn.close()


def search_stock(keyword):

    conn = get_connection()

    try:

        cur = conn.cursor()

        keyword = f"%{keyword}%"

        cur.execute("""
            SELECT *
            FROM inventory
            WHERE
                product_name LIKE ?
                OR brand LIKE ?
                OR model LIKE ?
            ORDER BY id DESC
        """, (

            keyword,

            keyword,

            keyword

        ))

        items = [dict(row) for row in cur.fetchall()]

        return {

            "status": "success",

            "items": items

        }

    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }

    finally:

        conn.close()


def update_quantity(product_id, quantity):

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute("""
            UPDATE inventory
            SET quantity=?
            WHERE id=?
        """, (

            int(quantity),

            int(product_id)

        ))

        conn.commit()

        return {

            "status": "success",

            "message": "Quantity Updated Successfully"

        }

    except Exception as e:

        conn.rollback()

        return {

            "status": "error",

            "message": str(e)

        }

    finally:

        conn.close()


def handle(payload):

    action = payload.get("action", "list")

    if action == "add":
        return add_stock(payload)

    elif action == "search":
        return search_stock(
            payload.get("keyword", "")
        )

    elif action == "update":
        return update_quantity(
            payload.get("id"),
            payload.get("quantity")
        )

    return list_stock()


if __name__ == "__main__":

    print(

        handle({

            "action": "list"

        })

    )
