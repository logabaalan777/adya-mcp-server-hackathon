import logging
from mcp.server import Server
from .tools_articles import GetArticlesToolHandler, CreateArticleToolHandler
from .tools_categories import GetCategoriesToolHandler
from .tools_management import ManageArticleStateToolHandler, MoveArticleToTrashToolHandler, UpdateArticleToolHandler
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

app = Server("mcp-joomla")
tool_handlers = {}

def add_tool_handler(handler):
    tool_handlers[handler.name] = handler

# Register all tool handlers
add_tool_handler(GetArticlesToolHandler())
add_tool_handler(GetCategoriesToolHandler())
add_tool_handler(CreateArticleToolHandler())
add_tool_handler(ManageArticleStateToolHandler())
add_tool_handler(MoveArticleToTrashToolHandler())
add_tool_handler(UpdateArticleToolHandler())

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
    asyncio.run(_main_async())

async def _main_async():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    main()