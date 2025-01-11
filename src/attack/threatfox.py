import json

import requests


def threatfox(query : str):
    url: str = "https://threatfox-api.abuse.ch/api/v1/"
    payload = {"query": "search_ioc", "search_term": query}

    response = requests.post(url, data=json.dumps(payload))
    response.raise_for_status()

    result = response.json()
    data = result.get("data", [])
    if data and isinstance(data, list):
        for index, element in enumerate(data):
            # Extract specific fields
            ioc_id = element.get("id", "")
            ioc = element.get("ioc", "")
            threat_type = element.get("threat_type", "")
            malware = element.get("malware_printable", "")
            confidence = element.get("confidence_level", "")
            reference = element.get("reference", "")
            link = f"https://threatfox.abuse.ch/ioc/{ioc_id}" if ioc_id else None

            # Print the selected fields
            result = {
                "id": ioc_id,
                "ioc": ioc,
                "threat_type": threat_type,
                "malware": malware,
                "confidence_level": confidence,
                "reference": reference,
                "link": link
            }

            return result



print(threatfox("62.60.226.62"))