from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .gemini_client import gemini_client

class SummarizeTextToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("summarize_text")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Summarize the provided text using Gemini API.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "summarize the following text"},
                    "api_key": {"type": "string", "description": "Gemini API key"}
                },
                "required": ["text", "api_key"]
            }
        )

    def run_tool(self, args: dict) -> list[TextContent]:
        text = args.get("text")
        api_key = args.get("api_key")
        if api_key:
            success = gemini_client.initialize(api_key)
            if not success:
                return [TextContent(type="text", text="❌ Failed to initialize Gemini client. Please check your API key and network connection.")]
        prompt = f"Summarize the following text:\n{text}"
        response = gemini_client.generate_response([
            {"role": "user", "content": prompt}
        ])
        return [TextContent(type="text", text=response)]