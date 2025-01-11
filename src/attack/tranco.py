import requests

def tranco(query):
    url: str = "https://tranco-list.eu/api/ranks/domain/"
    observable_to_analyze = query
    url = url + observable_to_analyze

    # Send GET request
    response = requests.get(url)
    response.raise_for_status()

    # Parse JSON from the response
    response_data = response.json()  # Parse JSON into a Python dictionary

    # Check if "ranks" exists and extract the latest rank
    if response_data.get("ranks"):  # Use .get() to safely access "ranks"
        latest_rank = response_data["ranks"][0]["rank"]  # The first rank is the latest
        result = {"rank": latest_rank}
    else:
        result = {"found": False}

    return result  # Return the processed result

# Example usage
print(tranco("wolfram.com"))