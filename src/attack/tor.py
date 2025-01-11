import os
import requests
import re

database_location = "media/tor.txt"

def tor(query:str):
    result = {"found": False}
    if not os.path.isfile(database_location) and not update():
        raise Exception("Failed extraction of tor db")

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
        print("tor exit nodes download started")
        url = "https://check.torproject.org/exit-addresses"
        r = requests.get(url)
        r.raise_for_status()

        data_extracted = r.content.decode()
        findings = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", data_extracted)

        with open(database_location, "w", encoding="utf-8") as f:
            for ip in findings:
                if ip:
                    f.write(f"{ip}\n")

        if not os.path.exists(database_location):
            return False

        print("ended download of db from tor project")
        return True
    except Exception as e:
        return False
    
print(tor("198.98.51.189"))