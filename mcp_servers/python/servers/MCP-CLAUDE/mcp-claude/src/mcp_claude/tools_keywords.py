from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .gemini_client import gemini_client

class KeywordExtractionToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("extract_keywords")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Extract keywords from the provided text using Gemini API.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to extract keywords from"},
                    "api_key": {"type": "string", "description": "Gemini API key"}
                },
                "required": ["text", "api_key"]
            }
        )

    def run_tool(self, args: dict) -> list[TextContent]:
        text = args.get("text")
        api_key = args.get("api_key")
        if api_key and not gemini_client.client:
            gemini_client.initialize(api_key)
        prompt = f"Extract the main keywords from the following text:\n{text}"
        response = gemini_client.generate_response([
            {"role": "user", "content": prompt}
        ])
        return [TextContent(type="text", text=response)]