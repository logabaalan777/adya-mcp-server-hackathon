# import json
# from .toolhandler import ToolHandler
# from mcp.types import Tool, TextContent

# class GeoCodeToolHandler(ToolHandler):
#     def __init__(self):
#         super().__init__("geocode_address")

#     def get_tool_description(self) -> Tool:
#         return {
#             "name": self.name,
#             "description": "Convert an address or place name to geographic coordinates with detailed location information.",
#             "parameters": {
#                 "address": {"type": "string", "description": "The address or place name to geocode"}
#             }
#         }

#     async def run_tool(self, args, ctx):
#         address = args.get("address")
#         if not address:
#             return [TextContent(type="text", text="Missing required parameter: address")]
#         osm_client = ctx.request_context.lifespan_context.osm_client
#         results = await osm_client.geocode(address)
#         # Enhance results with coordinates
#         for result in results:
#             if "lat" in result and "lon" in result:
#                 result["coordinates"] = {
#                     "latitude": float(result["lat"]),
#                     "longitude": float(result["lon"])
#                 }
#         return [TextContent(type="text", text=json.dumps(results, ensure_ascii=False))]

import json
from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent, EmbeddedResource
from mcp.server.fastmcp import Context

class GeoCodeToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("geocode_address")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Convert an address or place name to geographic coordinates with detailed location information.",
            inputSchema={
                "address": {
                    "type": "string",
                    "description": "The address or place name to geocode"
                }
            }
        )

    async def run_tool(self, args, ctx: Context):
        address = args.get("address")
        if not address:
            return [TextContent(type="text", text="Missing required parameter: address")]

        osm_client = ctx.request_context.lifespan_context.osm_client
        
        try:
            results = await osm_client.geocode(address)
        except Exception as e:
            return [TextContent(type="text", text=f"Geocoding error: {str(e)}")]

        for result in results:
            if "lat" in result and "lon" in result:
                result["coordinates"] = {
                    "latitude": float(result["lat"]),
                    "longitude": float(result["lon"])
                }

        return [
            TextContent(type="text", text=f"Found {len(results)} result(s) for '{address}'"),
            TextContent(type="text", text=json.dumps(results, indent=2, ensure_ascii=False))
        ]
