# mcp_servers/python/servers/MCP-CLAUDE/mcp-claude/src/mcp_claude/tools_conversation.py

from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .gemini_client import conversation_manager
import json

class ClearConversationToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("clear_conversation")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Clear a specific conversation history",
            inputSchema={
                "type": "object",
                "properties": {
                    "conversation_id": {
                        "type": "string",
                        "description": "Conversation ID"
                    }
                },
                "required": ["conversation_id"]
            }
        )

    def run_tool(self, args: dict) -> list[TextContent]:
        conversation_id = args.get("conversation_id", "default")
        success = conversation_manager.clear_conversation(conversation_id)
        msg = f"Conversation '{conversation_id}' cleared successfully" if success else f"Conversation '{conversation_id}' not found"
        return [TextContent(type="text", text=msg)]

class GetConversationHistoryToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_conversation_history")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get the conversation history for a specific ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "conversation_id": {"type": "string", "description": "Conversation ID"},
                    "include_metadata": {"type": "boolean", "description": "Include metadata"}
                },
                "required": ["conversation_id"]
            }
        )

    def run_tool(self, args: dict) -> list[TextContent]:
        conversation_id = args.get("conversation_id", "default")
        include_metadata = args.get("include_metadata", True)
        if include_metadata:
            history = conversation_manager.get_conversation_summary(conversation_id)
        else:
            history = {
                "conversation_id": conversation_id,
                "messages": conversation_manager.get_conversation(conversation_id)
            }
        return [TextContent(type="text", text=json.dumps(history, indent=2))]