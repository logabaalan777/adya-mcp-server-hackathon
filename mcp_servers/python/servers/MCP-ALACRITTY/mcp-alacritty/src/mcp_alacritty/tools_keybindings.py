import os
from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .alacritty_client import alacritty_client

class GetKeybindingsToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_alacritty_keybindings")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get the keybindings from the Alacritty config (TOML or YAML).",
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
                import yaml
                config = yaml.safe_load(content)
                keybindings = config.get("key_bindings", [])
                output = yaml.safe_dump(keybindings, sort_keys=False)
            elif ext == ".toml":
                import toml
                config = toml.loads(content)
                keybindings = config.get("key_bindings", [])
                import json
                output = json.dumps(keybindings, indent=2)
            else:
                return [TextContent(type="text", text="Unsupported file format. Use .toml, .yml, or .yaml")]

            if not keybindings:
                return [TextContent(type="text", text="No key bindings found in the configuration.")]

            return [TextContent(type="text", text=output)]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]
