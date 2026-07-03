# modules/login.py

import bcrypt
from database import get_connection


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password, hashed):
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed.encode("utf-8")
        )
    except Exception:
        return False


def create_user(username, password, role="User"):

    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id
            FROM users
            WHERE username=?
            """,
            (username,)
        )

        if cur.fetchone():
            return {
                "status": "error",
                "message": "Username Already Exists"
            }

        cur.execute(
            """
            INSERT INTO users(
                username,
                password,
                role
            )
            VALUES(?,?,?)
            """,
            (
                username,
                hash_password(password),
                role
            )
        )

        conn.commit()

        return {
            "status": "success",
            "message": "User Created Successfully"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }

    finally:
        conn.close()


def authenticate(username, password):

    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM users
            WHERE username=?
            """,
            (username,)
        )

        user = cur.fetchone()

        if user is None:

            return {
                "status": "error",
                "message": "Invalid Username"
            }

        if verify_password(password, user["password"]):

            return {
                "status": "success",
                "username": user["username"],
                "role": user["role"]
            }

        return {
            "status": "error",
            "message": "Invalid Password"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }

    finally:
        conn.close()


def handle(payload):

    action = payload.get("action", "authenticate")

    if action == "create":
        return create_user(
            payload.get("username"),
            payload.get("password"),
            payload.get("role", "User")
        )

    if action == "authenticate":
        return authenticate(
            payload.get("username"),
            payload.get("password")
        )

    return {
        "status": "error",
        "message": "Invalid Action"
    }
