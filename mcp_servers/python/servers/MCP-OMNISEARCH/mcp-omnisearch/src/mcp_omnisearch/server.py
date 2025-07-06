import logging
from collections.abc import Sequence
from typing import Any
import traceback
import inspect
from mcp.server import Server
import asyncio
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from . import toolhandler
from .tools_search import (
    BraveSearchToolHandler, TavilySearchToolHandler, PerplexitySearchToolHandler
)
from .tools_processing import (
    FirecrawlActionsToolHandler, FirecrawlCrawlToolHandler, FirecrawlExtractToolHandler, FirecrawlScrapeToolHandler, TavilyExtractToolHandler, JinaReaderToolHandler, FirecrawlMapToolHandler
)
from .tools_enhancement import (
    JinaGroundingToolHandler
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-omnisearch")

app = Server("mcp-omnisearch")

tool_handlers = {}
def add_tool_handler(tool_class: toolhandler.ToolHandler):
    global tool_handlers
    tool_handlers[tool_class.name] = tool_class

def get_tool_handler(name: str) -> toolhandler.ToolHandler | None:
    return tool_handlers.get(name)

# Register tool handlers
add_tool_handler(BraveSearchToolHandler())
add_tool_handler(TavilySearchToolHandler())
add_tool_handler(PerplexitySearchToolHandler())
add_tool_handler(FirecrawlActionsToolHandler())
add_tool_handler(FirecrawlCrawlToolHandler())
add_tool_handler(FirecrawlExtractToolHandler())
add_tool_handler(FirecrawlScrapeToolHandler())
add_tool_handler(TavilyExtractToolHandler())
add_tool_handler(JinaGroundingToolHandler())
add_tool_handler(JinaReaderToolHandler())
add_tool_handler(FirecrawlMapToolHandler()) 

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [th.get_tool_description() for th in tool_handlers.values()]

# @app.call_tool()
# async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
#     try:
#         if not isinstance(arguments, dict):
#             raise RuntimeError("arguments must be dictionary")
#         tool_handler = get_tool_handler(name)
#         if not tool_handler:
#             raise ValueError(f"Unknown tool: {name}")
#         return await tool_handler.run_tool(arguments)
#     except Exception as e:
#         logging.error(traceback.format_exc())
#         logging.error(f"Error during call_tool: str(e)")
#         raise RuntimeError(f"Caught Exception. Error: {str(e) , e}")

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    try:
        if not isinstance(arguments, dict):
            raise RuntimeError("arguments must be dictionary")
        tool_handler = get_tool_handler(name)
        if not tool_handler:
            raise ValueError(f"Unknown tool: {name}")
        result = tool_handler.run_tool(arguments)
        if inspect.isawaitable(result):
            return await result
        return result
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error during call_tool: str(e)")
        raise RuntimeError(f"Caught Exception. Error: {str(e) , e}")

def main():
    asyncio.run(_main_async())

async def _main_async():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    main()