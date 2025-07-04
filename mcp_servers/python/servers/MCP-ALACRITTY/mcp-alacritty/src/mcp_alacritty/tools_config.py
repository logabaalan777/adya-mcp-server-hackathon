import os
from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .alacritty_client import alacritty_client
import toml

class GetConfigToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_alacritty_config")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get the full Alacritty configuration as YAML or TOML.",
            inputSchema={
                "type": "object",
                "properties": {
                    "config_path": {
                        "type": "string",
                        "description": "Path to the Alacritty config file (YAML or TOML)"
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
                import yaml
                config = yaml.safe_load(content)
                config_text = yaml.safe_dump(config)
            elif ext == ".toml":
                config = toml.loads(content)
                import json
                config_text = json.dumps(config, indent=2)  # TOML to JSON for readability
            else:
                return [TextContent(type="text", text="Unsupported config file format.")]
            return [TextContent(type="text", text=config_text)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]