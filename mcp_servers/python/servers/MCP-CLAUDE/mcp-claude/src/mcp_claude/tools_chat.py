# mcp_servers/python/servers/MCP-CLAUDE/mcp-claude/src/mcp_claude/tools_chat.py

from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .gemini_client import gemini_client, conversation_manager  # Assume you modularize GeminiClient

class ChatToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("chat_completion")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Generate chat completion using Gemini API",
            inputSchema={
                "type": "object",
                "properties": {
                    "messages": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "role": {"type": "string"},
                                "content": {"type": "string"}
                            },
                            "required": ["role", "content"]
                        },
                        "description": "List of message dicts with 'role' and 'content'"
                    },
                    "conversation_id": {"type": "string", "description": "Conversation ID"},
                    "system_prompt": {"type": "string", "description": "System prompt"},
                    "temperature": {"type": "number", "description": "Temperature"},
                    "max_tokens": {"type": "integer", "description": "Max output tokens"},
                    "api_key": {"type": "string", "description": "Gemini API key"}
                },
                "required": ["messages"]
            }
        )

    def run_tool(self, args: dict) -> list[TextContent]:
        # Extract arguments
        messages = args.get("messages", [])
        conversation_id = args.get("conversation_id", "default")
        system_prompt = args.get("system_prompt")
        temperature = args.get("temperature")
        max_tokens = args.get("max_tokens")
        api_key = args.get("api_key")

        # Initialize client if needed
        if api_key and not gemini_client.client:
            gemini_client.initialize(api_key)

        # Set system prompt if provided
        if system_prompt:
            conversation_manager.set_system_prompt(conversation_id, system_prompt)

        # Add messages to conversation history
        for msg in messages:
            conversation_manager.add_message(conversation_id, msg.get("role", "user"), msg.get("content", ""))

        # Prepare generation parameters
        gen_params = {}
        if temperature is not None:
            gen_params["temperature"] = max(0.0, min(1.0, temperature))
        if max_tokens is not None:
            gen_params["max_output_tokens"] = max_tokens

        # Generate response
        response = gemini_client.generate_response(messages, conversation_manager.get_system_prompt(conversation_id), **gen_params)
        conversation_manager.add_message(conversation_id, "assistant", response)

        return [TextContent(type="text", text=response)]