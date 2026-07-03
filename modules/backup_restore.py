# modules/backup_restore.py

import os
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_NAME = os.path.join(
    BASE_DIR,
    "mobile_shop.db"
)

BACKUP_DIR = os.path.join(
    BASE_DIR,
    "backups"
)

os.makedirs(
    BACKUP_DIR,
    exist_ok=True
)


def create_backup():

    try:

        if not os.path.exists(DB_NAME):

            return {
                "status": "error",
                "message": "Database file not found."
            }

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_file = os.path.join(
            BACKUP_DIR,
            f"mobile_shop_{timestamp}.db"
        )

        shutil.copy2(
            DB_NAME,
            backup_file
        )

        return {

            "status": "success",

            "message": "Backup Created Successfully",

            "path": backup_file

        }

    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }


def restore_backup(path):

    try:

        if not path:

            return {

                "status": "error",

                "message": "Backup path is required."

            }

        if not os.path.exists(path):

            return {

                "status": "error",

                "message": "Backup file not found."

            }

        shutil.copy2(
            path,
            DB_NAME
        )

        return {

            "status": "success",

            "message": "Database Restored Successfully"

        }

    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }


def list_backups():

    try:

        backups = sorted(

            [

                file

                for file in os.listdir(BACKUP_DIR)

                if file.endswith(".db")

            ],

            reverse=True

        )

        return {

            "status": "success",

            "backups": backups

        }

    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }


def handle(payload):

    action = payload.get(
        "action",
        "list"
    )

    if action == "backup":

        return create_backup()

    elif action == "restore":

        return restore_backup(
            payload.get("path")
        )

    return list_backups()


if __name__ == "__main__":

    print(
        handle({
            "action": "backup"
        })
    )
