class ToolRegistry:
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state # do i need this?
        self.tools = {}

    def register(self, tool_name: str, tool_function):
        self.tools[tool_name] = tool_function
        print(f"[TOOLS]: ({len(self.tools)}) {tool_name} registered")

    def get_tools_for_gemini_api(self) -> list:
        if not self.tools:
            return None
        return list(self.tools.values())

tool_registry = ToolRegistry()