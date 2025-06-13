from .tool_registry import tool_registry

class Tool(object):
    def __init__(self, args: dict = None):
        self._args_override = args

    def __call__(self, function):
        function_name = function.__name__

        # Register the tool with the global registry
        tool_registry.register(function_name, function)

        # Return the original function so it can still be called normally
        return function