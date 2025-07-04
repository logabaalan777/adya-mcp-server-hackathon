import json
from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent, EmbeddedResource
from mcp.server.fastmcp import Context

class ReverseGeocodeToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("reverse_geocode")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Convert geographic coordinates to a detailed address and location description.",
            inputSchema={
                "latitude": {"type": "number", "description": "The latitude coordinate (decimal degrees, WGS84)"},
                "longitude": {"type": "number", "description": "The longitude coordinate (decimal degrees, WGS84)"}
            }
        )

    async def run_tool(self, args, ctx: Context):
        try:
            latitude = float(args.get("latitude"))
            longitude = float(args.get("longitude"))
        except (TypeError, ValueError):
            return [TextContent(type="text", text="Missing or invalid parameters: latitude and longitude must be numbers")]

        osm_client = ctx.request_context.lifespan_context.osm_client

        try:
            result = await osm_client.reverse_geocode(latitude, longitude)
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error during reverse geocoding: {str(e)}")]
