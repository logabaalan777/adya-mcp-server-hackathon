# mcp_servers/python/servers/MCP-CLAUDE/mcp-claude/src/mcp_claude/server.py

import logging
from mcp.server import Server
from .tools_chat import ChatToolHandler
from .tools_conversation import ClearConversationToolHandler, GetConversationHistoryToolHandler
from .tools_model import GetModelInfoToolHandler
from .tools_summarize import SummarizeTextToolHandler
from .tools_translate import TranslateTextToolHandler
from .tools_sentiment import SentimentAnalysisToolHandler
from .tools_keywords import KeywordExtractionToolHandler
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

app = Server("mcp-claude")
tool_handlers = {}

def add_tool_handler(handler):
    tool_handlers[handler.name] = handler

# Register all tool handlers
add_tool_handler(ChatToolHandler())
add_tool_handler(ClearConversationToolHandler())
add_tool_handler(GetConversationHistoryToolHandler())
add_tool_handler(GetModelInfoToolHandler())
add_tool_handler(SummarizeTextToolHandler())
add_tool_handler(TranslateTextToolHandler())
add_tool_handler(SentimentAnalysisToolHandler())
add_tool_handler(KeywordExtractionToolHandler())

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [th.get_tool_description() for th in tool_handlers.values()]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
    handler = tool_handlers.get(name)
    if not handler:
        raise ValueError(f"Unknown tool: {name}")
    return handler.run_tool(arguments)

def main():
    import asyncio
    asyncio.run(_main_async())

async def _main_async():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    main()

