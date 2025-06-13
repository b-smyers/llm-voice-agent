from ..tool import Tool
from datetime import datetime

@Tool()
def get_date():
    """
    Gets the current date of the user
    """
    current_date = datetime.now().strftime('%Y-%m-%d')
    return current_date