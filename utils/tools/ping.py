from ..tool import Tool
import requests

api_timeout_sec = 2

@Tool()
def ping(url: str) -> str:
    """
    Pings the given URL by sending an HTTP GET request and returns the HTTP status code.
    """
    try:
        response = requests.get(url, timeout=api_timeout_sec)
        return f"Ping successful! Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Ping failed: {e}"