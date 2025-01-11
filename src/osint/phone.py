import requests
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

def validate_phone_number(number, country_code=None):
    """
    Validate a phone number using the NumVerify API.
    
    Args:
        number (str): The phone number to validate.
        country_code (str): Optional country code for the phone number.

    Returns:
        dict: The API response in JSON format.
    """
    # Load the API key from the .env file
    api_key = os.getenv("NUMVERIFY_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set NUMVERIFY_API_KEY in the .env file.")

    # Define the API endpoint and parameters
    url = "http://apilayer.net/api/validate"
    params = {
        "access_key": api_key,
        "number": number,
        "country_code": country_code or "",
        "format": 1
    }

    # Make the API request
    try:
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()
        
        # Check if the number is valid
        if not data.get("valid", False):
            return {"phone_no": False}
        
        return data
    except requests.RequestException as e:
        # Handle request errors
        return {"phone_no": False, "error": str(e)}

# Example usage

# Replace with a phone number to test
result = validate_phone_number("141585862")
print(result)