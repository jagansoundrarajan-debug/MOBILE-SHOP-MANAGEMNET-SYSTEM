# modules/usermanagement.py

import logging
import bcrypt
from database import get_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("modules.usermanagement")


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def create_user(username, password, role="User"):

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute("""
            SELECT id
            FROM users
            WHERE username=?
        """, (username,))

        if cur.fetchone():

            return {

                "status": "error",

                "message": "Username Already Exists"

            }

        cur.execute("""
            INSERT INTO users(
                username,
                password,
                role
            )
            VALUES(?,?,?)
        """, (

            username,

            hash_password(password),

            role

        ))

        conn.commit()

        return {

            "status": "success",

            "message": "User Created Successfully"

        }

    except Exception as e:

        logger.exception("Create User Error")

        return {

            "status": "error",

            "message": str(e)

        }

    finally:

        conn.close()


def delete_user(user_id):

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute(

            "DELETE FROM users WHERE id=?",

            (user_id,)

        )

        conn.commit()

        return {

            "status": "success",

            "message": "User Deleted Successfully"

        }

    except Exception as e:

        logger.exception("Delete User Error")

        return {

            "status": "error",

            "message": str(e)

        }

    finally:

        conn.close()


def list_users():

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                username,
                role
            FROM users
            ORDER BY id
        """)

        users = [

            dict(row)

            for row in cur.fetchall()

        ]

        return {

            "status": "success",

            "users": users

        }

    except Exception as e:

        logger.exception("List User Error")

        return {

            "status": "error",

            "message": str(e)

        }

    finally:

        conn.close()


def handle(payload):

    action = payload.get("action", "list")

    if action == "create":

        return create_user(

            payload.get("username"),

            payload.get("password"),

            payload.get("role", "User")

        )

    elif action == "delete":

        return delete_user(

            payload.get("user_id")

        )

    elif action == "list":

        return list_users()

    return {

        "status": "error",

        "message": "Invalid Action"

    }


if __name__ == "__main__":

    print(

        handle({

            "action": "list"

        })

    )