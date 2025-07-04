import os
import logging
from mcp.server import Server
from .toolhandler import ToolHandler
from .tools_config import GetConfigToolHandler
from .tools_theme import GetThemeToolHandler
from .tools_font import GetFontToolHandler
from .tools_keybindings import GetKeybindingsToolHandler
from .tools_window import GetWindowSettingsToolHandler
from .tools_performance import GetPerformanceToolHandler
from .tools_usage import GetAlacrittyUsageToolHandler
from .tools_export import ExportConfigToolHandler
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .alacritty_client import alacritty_client

app = Server("mcp-alacritty")
tool_handlers = {}

def add_tool_handler(handler):
    tool_handlers[handler.name] = handler

# Register all tool handlers
add_tool_handler(GetConfigToolHandler())
add_tool_handler(GetThemeToolHandler())
add_tool_handler(GetFontToolHandler())
add_tool_handler(GetKeybindingsToolHandler())
add_tool_handler(GetWindowSettingsToolHandler())
add_tool_handler(GetPerformanceToolHandler())
add_tool_handler(GetAlacrittyUsageToolHandler())
add_tool_handler(ExportConfigToolHandler())

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [th.get_tool_description() for th in tool_handlers.values()]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
    handler = tool_handlers.get(name)
    if not handler:
        raise ValueError(f"Unknown tool: {name}")
    return await handler.run_tool(arguments)

def main():
    import asyncio

    if os.name == 'nt':  # Windows
        config_path = os.path.expandvars(r"%APPDATA%\alacritty\alacritty.toml")
    else:
        config_path = os.path.expanduser("~/.config/alacritty/alacritty.toml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"alacritty.toml not found at: {config_path}")

    # Initialize the config client
    alacritty_client.initialize(config_path)
    asyncio.run(_main_async())

async def _main_async():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    main()
