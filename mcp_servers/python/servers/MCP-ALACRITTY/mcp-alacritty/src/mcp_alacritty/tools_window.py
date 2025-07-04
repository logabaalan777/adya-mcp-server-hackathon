import os
from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .alacritty_client import alacritty_client
import toml
import yaml

class GetWindowSettingsToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_alacritty_window_settings")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get the window settings (dimensions, decorations, etc.) from the Alacritty config (YAML or TOML).",
            inputSchema={
                "type": "object",
                "properties": {
                    "config_path": {
                        "type": "string",
                        "description": "Path to the Alacritty config file (.yml/.yaml/.toml)"
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
                window = config.get("window", {})
                output = yaml.safe_dump(window)

            elif ext == ".toml":
                config = toml.loads(content)
                window = config.get("window", {})
                import json
                output = json.dumps(window, indent=2)

            else:
                return [TextContent(type="text", text="Unsupported config file format. Use .yml, .yaml, or .toml")]

            return [TextContent(type="text", text=output)]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]
