from dotenv import load_dotenv
import os
import requests

load_dotenv()



def onphe(query:str , type:str):    
    url: str = "https://www.onyphe.io/api/v2/summary/"

    _api_key_name: str = os.getenv("onypheAPI_KEY")

    headers = {
        "Authorization": f"apikey {_api_key_name}",
        "Content-Type": "application/json",
    }

    if type == "domain":
        uri = f"domain/{query}"
    elif type == "ip":
        uri = f"ip/{query}"
    elif type == "url":
        uri = f"hostname/{query}"
    else:
        raise Exception(
            f"not supported observable type {type}."
            " Supported are: ip, domain and url."
        )

    try:
        response = requests.get(url + uri, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(e)

    return response.json()

print(onphe("aegisclub.tech", "domain"))