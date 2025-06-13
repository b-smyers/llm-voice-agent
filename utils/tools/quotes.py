from ..tool import Tool
import requests

api_timeout_sec = 2

@Tool()
def get_random_quote():
    """
    Fetches a random inspirational quote
    """
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=api_timeout_sec)
        if response.ok:
            data = response.json()
            quote = data[0]['q']
            author = data[0]['a']
            return f'"{quote}" — {author}'
        return "Sorry, couldn't fetch a quote right now."
    except requests.exceptions.Timeout:
        return "Request timed out."
    except Exception as e:
        return f"Error: {str(e)}"