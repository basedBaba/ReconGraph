from dotenv import load_dotenv
import requests
import os
load_dotenv()

api_key = os.getenv("ipAPI_KEY")
batch_url = "http://ip-api.com/batch"
dns_url = "http://edns.ip-api.com/json"


def ipapi(ip_addr):
    IP = [
            {
                "query": ip_addr,
                "fields": "status,message,country,countryCode,region,regionName,city,zip,timezone,isp,org,as",
                "lang" : "us",
            }
        ]

    response_batch = requests.post(batch_url, json=IP)
    response_batch.raise_for_status()

    response_dns = requests.get(dns_url)
    response_dns.raise_for_status()

    response = {"ip_info": response_batch.json(), "dns_info": response_dns.json()}

    return response

print(ipapi("208.80.152.201"))