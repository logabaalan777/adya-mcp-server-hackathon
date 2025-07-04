import os
from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .alacritty_client import alacritty_client
import toml
import yaml

class ExportConfigToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("export_alacritty_config")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Export the current Alacritty config to a specified file (.yaml/.yml/.toml).",
            inputSchema={
                "type": "object",
                "properties": {
                    "config_path": {
                        "type": "string",
                        "description": "Path to the Alacritty config file"
                    },
                    "export_path": {
                        "type": "string",
                        "description": "Path to export the config file (.yaml/.yml/.toml)"
                    }
                },
                "required": ["config_path", "export_path"]
            }
        )

    async def run_tool(self, args: dict) -> list[TextContent]:
        config_path = args.get("config_path")
        export_path = args.get("export_path")

        if not alacritty_client.is_initialized():
            alacritty_client.initialize(config_path)

        try:
            config = alacritty_client.load_config()
            ext = os.path.splitext(export_path)[1].lower()

            with open(export_path, "w", encoding="utf-8") as f:
                if ext in [".yaml", ".yml"]:
                    yaml.safe_dump(config, f)
                elif ext == ".toml":
                    toml.dump(config, f)
                else:
                    return [TextContent(type="text", text="Unsupported export file format. Use .yaml, .yml, or .toml")]

            return [TextContent(type="text", text=f"Config exported successfully to {export_path}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]
