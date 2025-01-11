import os

import requests

database_location = "media/talos.txt"

def talos(query: str):
        result = {"found": False}
        if not os.path.isfile(database_location):
            if not update():
                raise Exception("Failed extraction of talos db")

        if not os.path.exists(database_location):
            raise Exception(
                f"database location {database_location} does not exist"
            )

        with open(database_location, "r", encoding="utf-8") as f:
            db = f.read()

        db_list = db.split("\n")
        if query in db_list:
            result["found"] = True

        return result

def update():
    try:
        print("starting download of db from talos")
        url = "https://snort.org/downloads/ip-block-list"
        r = requests.get(url)
        r.raise_for_status()

        with open(database_location, "w", encoding="utf-8") as f:
            f.write(r.content.decode())

        if not os.path.exists(database_location):
            return False
        print("ended download of db from talos")
        return True
    except Exception as e:
        raise Exception

    return False

print(talos("109.196.187.208"))