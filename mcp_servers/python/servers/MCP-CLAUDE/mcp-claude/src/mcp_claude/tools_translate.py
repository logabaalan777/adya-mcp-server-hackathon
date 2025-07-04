from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .gemini_client import gemini_client

class TranslateTextToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("translate_text")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Translate text from one language to another using Gemini API.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to translate"},
                    "source_lang": {"type": "string", "description": "Source language (e.g., 'en')"},
                    "target_lang": {"type": "string", "description": "Target language (e.g., 'fr')"},
                    "api_key": {"type": "string", "description": "Gemini API key"}
                },
                "required": ["text", "source_lang", "target_lang", "api_key"]
            }
        )

    def run_tool(self, args: dict) -> list[TextContent]:
        text = args.get("text")
        source_lang = args.get("source_lang")
        target_lang = args.get("target_lang")
        api_key = args.get("api_key")
        if api_key and not gemini_client.client:
            gemini_client.initialize(api_key)
        prompt = f"Translate the following text from {source_lang} to {target_lang}:\n{text}"
        response = gemini_client.generate_response([
            {"role": "user", "content": prompt}
        ])
        return [TextContent(type="text", text=response)]