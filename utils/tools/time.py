from ..tool import Tool
from datetime import datetime

@Tool()
def get_time():
    """
    Gets the current time of the user
    """
    current_time = datetime.now().strftime('%-H:%M')
    return current_time