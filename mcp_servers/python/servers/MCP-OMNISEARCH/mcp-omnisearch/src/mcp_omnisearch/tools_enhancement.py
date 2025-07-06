import asyncio
from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent
from .omnisearch_client import OmnisearchClient

class JinaGroundingToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("jina_grounding")

    def get_tool_description(self) -> Tool:
        return Tool(
            name="jina_grounding",
            description="Content enrichment and grounding using Jina AI. Adds context, references, and factual grounding to input content. Best for improving factuality and traceability of generated content.",
            inputSchema={
                "api_key": {"type": "string", "description": "Jina AI API key (required)"},
                "content": {"type": "string", "description": "Content to enhance and ground"},
            },
            required=["api_key", "content"]
        )

    async def run_tool(self, args: dict):
        api_key = args.get("api_key")
        client = OmnisearchClient(api_key)
        content = args.get("content", "")
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, client.jina_grounding, content)
        return [TextContent(type="text", text=result.get("result", str(result)))]