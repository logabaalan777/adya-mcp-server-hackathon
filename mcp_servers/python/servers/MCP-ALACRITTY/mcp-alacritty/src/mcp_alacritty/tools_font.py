import os
from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .alacritty_client import alacritty_client
import toml
import yaml

class GetFontToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_alacritty_font")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get the current font settings from the Alacritty config (TOML or YAML).",
            inputSchema={
                "type": "object",
                "properties": {
                    "config_path": {
                        "type": "string",
                        "description": "Path to the Alacritty config file (.toml/.yml/.yaml)"
                    }
                },
                "required": ["config_path"]
            }
        )

    async def run_tool(self, args: dict) -> list[TextContent]:
        config_path = args.get("config_path")
        if not alacritty_client.is_initialized():
            alacritty_client.initialize(config_path)

        try:
            ext = os.path.splitext(config_path)[1].lower()
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()

            if ext in [".yml", ".yaml"]:
                config = yaml.safe_load(content)
                font = config.get("font", {})
                output = yaml.safe_dump(font, sort_keys=False)

            elif ext == ".toml":
                config = toml.loads(content)
                font = config.get("font", {})
                import json
                output = json.dumps(font, indent=2)

            else:
                return [TextContent(type="text", text="Unsupported config file format. Use .yml, .yaml, or .toml")]

            if not font:
                return [TextContent(type="text", text="No font settings found in the configuration.")]

            return [TextContent(type="text", text=output)]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]
