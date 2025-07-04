from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from typing import Union, Any
from mcp.server.fastmcp import Context
ToolOutput = Union[TextContent, ImageContent, EmbeddedResource]

class ToolHandler:
    def __init__(self, name: str):
        self.name = name

    def get_tool_description(self) -> Tool:
        raise NotImplementedError()

    async def run_tool(self, args: dict, ctx: Context) -> list[ToolOutput]:
        raise NotImplementedError()