from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .gemini_client import gemini_client

class SentimentAnalysisToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("sentiment_analysis")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Analyze the sentiment of the provided text using Gemini API.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to analyze"},
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
        prompt = f"Analyze the sentiment (positive, negative, neutral) of the following text:\n{text}"
        response = gemini_client.generate_response([
            {"role": "user", "content": prompt}
        ])
        return [TextContent(type="text", text=response)] 