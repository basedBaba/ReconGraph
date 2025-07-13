import json
import os
import requests

def threatfox(query: str):
    auth_key = os.getenv("THREATFOX_API_KEY")
    url = "https://threatfox-api.abuse.ch/api/v1/"
    payload = {"query": "search_ioc", "search_term": query}
    headers = {
        "Content-Type": "application/json",
        "Auth-Key": auth_key
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            print(f"[ERROR] ThreatFox API returned status code {response.status_code}")
            return None

        result = response.json()
        data = result.get("data", [])
        if data and isinstance(data, list):
            for element in data:
                ioc_id = element.get("id", "")
                return {
                    "id": ioc_id,
                    "ioc": element.get("ioc", ""),
                    "threat_type": element.get("threat_type", ""),
                    "malware": element.get("malware_printable", ""),
                    "confidence_level": element.get("confidence_level", ""),
                    "reference": element.get("reference", ""),
                    "link": f"https://threatfox.abuse.ch/ioc/{ioc_id}" if ioc_id else None
                }

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] ThreatFox API request failed: {e}")
        return None

