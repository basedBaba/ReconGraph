import requests


def breachAnalytics(email: str) -> dict:
    url = f"https://api.xposedornot.com/v1/breach-analytics?email={email}"

    results = requests.get(url).json()

    return results


def checkEmail(email: str) -> dict:
    url = f"https://api.xposedornot.com/v1/check-email/{email}"

    results = requests.get(url).json()

    if "Error" in results:
        return {"error": "Email address not found in any breach database!"}

    breach_analytics = breachAnalytics(email)

    breaches = []
    for breach in breach_analytics["ExposedBreaches"]["breaches_details"]:
        breaches.append(breach)

    password_strengths = breach_analytics["BreachMetrics"]["passwords_strength"]

    risk = breach_analytics["BreachMetrics"]["risk"]

    results = {
        "breaches": breaches,
        "password_strength": password_strengths,
        "risk": risk,
    }

    return results
