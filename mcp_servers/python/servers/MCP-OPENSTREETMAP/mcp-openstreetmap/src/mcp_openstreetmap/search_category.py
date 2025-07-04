import json
from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent
from mcp.server.fastmcp import Context

class SearchCategoryToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("search_category")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Search for specific types of places within a defined geographic area.",
            inputSchema={
                "category": {
                    "type": "string",
                    "description": "Main OSM category to search for (e.g., amenity, shop, tourism, building)"
                },
                "min_latitude": {
                    "type": "number",
                    "description": "Southern boundary of search area (decimal degrees)"
                },
                "min_longitude": {
                    "type": "number",
                    "description": "Western boundary of search area (decimal degrees)"
                },
                "max_latitude": {
                    "type": "number",
                    "description": "Northern boundary of search area (decimal degrees)"
                },
                "max_longitude": {
                    "type": "number",
                    "description": "Eastern boundary of search area (decimal degrees)"
                },
                "subcategories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Specific subcategories to filter by (e.g., restaurant, cafe)",
                    "optional": True
                }
            }
        )

    async def run_tool(self, args, ctx: Context):
        # Extract and validate input parameters
        category = args.get("category")
        subcategories = args.get("subcategories", [])
        min_lat = args.get("min_latitude")
        min_lon = args.get("min_longitude")
        max_lat = args.get("max_latitude")
        max_lon = args.get("max_longitude")

        if None in (category, min_lat, min_lon, max_lat, max_lon):
            return [TextContent(
                type="text",
                text="Missing required parameters: category, min_latitude, min_longitude, max_latitude, max_longitude"
            )]

        bbox = (min_lon, min_lat, max_lon, max_lat)

        # Safe logging if 'info' is available
        if hasattr(ctx, "info") and callable(ctx.info):
            ctx.info(f"Searching for '{category}' in bounding box: {bbox}")

        # Access the OSM client
        osm_client = ctx.request_context.lifespan_context.osm_client

        try:
            features = await osm_client.search_features_by_category(bbox, category, subcategories)
        except Exception as e:
            return [TextContent(type="text", text=f"Error while searching features: {str(e)}")]

        results = []
        for feature in features:
            props = feature.get("tags", {})
            center = {
                "latitude": feature.get("lat") or feature.get("center", {}).get("lat"),
                "longitude": feature.get("lon") or feature.get("center", {}).get("lon")
            }

            if center["latitude"] is None or center["longitude"] is None:
                continue

            results.append({
                "id": feature.get("id"),
                "name": props.get("name", "Unnamed"),
                "latitude": center["latitude"],
                "longitude": center["longitude"],
                "tags": props
            })

        output = {
            "query": {
                "category": category,
                "subcategories": subcategories,
                "bounding_box": {
                    "min_latitude": min_lat,
                    "min_longitude": min_lon,
                    "max_latitude": max_lat,
                    "max_longitude": max_lon
                }
            },
            "results": results,
            "total_count": len(results)
        }

        return [TextContent(type="text", text=json.dumps(output, indent=2, ensure_ascii=False))]

