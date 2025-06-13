from ..tool import Tool
import requests

api_timeout_sec = 2

@Tool()
def get_random_advice():
    """
    Fetches a random piece of advice
    """
    try:
        response = requests.get("https://api.adviceslip.com/advice", timeout=api_timeout_sec)
        if response.ok:
            return response.json()['slip']['advice']
        return "Sorry, couldn't fetch advice right now."
    except requests.exceptions.Timeout:
        return "Request timed out."
    except Exception as e:
        return f"Error: {str(e)}"