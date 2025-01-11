import requests


def internetdb(ip: str) -> dict:
    url = f"https://internetdb.shodan.io/{ip}"

    results = requests.get(url).json()

    hostnames = results["hostnames"]

    ports = results["ports"]

    tags = results["tags"]

    cves = []
    for vuln in results["vulns"]:
        cves.append({vuln: f"https://nvd.nist.gov/vuln/detail/{vuln.lower()}"})

    results = {"hostnames": hostnames, "ports": ports, "tags": tags, "cves": cves}

    return results
