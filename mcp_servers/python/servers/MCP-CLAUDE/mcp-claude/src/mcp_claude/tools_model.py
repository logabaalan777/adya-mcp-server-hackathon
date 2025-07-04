# mcp_servers/python/servers/MCP-CLAUDE/mcp-claude/src/mcp_claude/tools_model.py

from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .gemini_client import gemini_client, conversation_manager
from datetime import datetime
import json

class GetModelInfoToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_model_info")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get current model information and client status",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )

    def run_tool(self, args: dict) -> list[TextContent]:
        model_info = gemini_client.get_model_info()
        status = {
            "model_info": model_info,
            "server_status": {
                "active_conversations": len(conversation_manager.conversations),
                "total_messages": sum(len(conv) for conv in conversation_manager.conversations.values()),
                "timestamp": datetime.now().isoformat()
            }
        }
        return [TextContent(type="text", text=json.dumps(status, indent=2))]