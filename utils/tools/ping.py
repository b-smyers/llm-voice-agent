from ..tool import Tool
import requests

@Tool()
def ping(url: str) -> str:
    """
    Pings the given URL by sending an HTTP GET request and returns the HTTP status code.
    """
    try:
        response = requests.get(url, timeout=3)  # 3 second timeout
        return f"Ping successful! Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Ping failed: {e}"