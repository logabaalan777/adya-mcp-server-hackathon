import json
from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent
from mcp.server.fastmcp import Context

class FindNearbyPlacesToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("find_nearby_places")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Discover points of interest and amenities near a specific location.",
            inputSchema={
                "latitude": {"type": "number", "description": "Center point latitude (decimal degrees)"},
                "longitude": {"type": "number", "description": "Center point longitude (decimal degrees)"},
                "radius": {
                    "type": "number",
                    "description": "Search radius in meters (default 1000)",
                    "optional": True
                },
                "categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "OSM categories to search for (e.g., amenity, shop, tourism)",
                    "optional": True
                },
                "limit": {
                    "type": "number",
                    "description": "Maximum number of total results to return (default 20)",
                    "optional": True
                }
            }
        )

    async def run_tool(self, args, ctx: Context):
        latitude = args.get("latitude")
        longitude = args.get("longitude")
        radius = args.get("radius", 1000)
        categories = args.get("categories", ["amenity", "shop", "tourism", "leisure"])
        limit = args.get("limit", 20)

        if latitude is None or longitude is None:
            return [TextContent(type="text", text="Missing required parameters: latitude and longitude")]

        osm_client = ctx.request_context.lifespan_context.osm_client

        # Safe logging
        if hasattr(ctx, "info"):
            ctx.info(f"Searching for places within {radius}m of ({latitude}, {longitude})")

        try:
            places = await osm_client.get_nearby_pois(latitude, longitude, radius, categories)
        except Exception as e:
            return [TextContent(type="text", text=f"Error retrieving POIs: {str(e)}")]

        results_by_category = {}
        total_added = 0

        for place in places:
            if total_added >= limit:
                break

            tags = place.get("tags", {})
            coords = {
                "latitude": place.get("lat") or place.get("center", {}).get("lat"),
                "longitude": place.get("lon") or place.get("center", {}).get("lon")
            }

            if coords["latitude"] is None or coords["longitude"] is None:
                continue  # skip invalid location

            for category in categories:
                if category in tags:
                    subcategory = tags[category]
                    results_by_category.setdefault(category, {}).setdefault(subcategory, []).append({
                        "id": place.get("id"),
                        "name": tags.get("name", "Unnamed"),
                        "latitude": coords["latitude"],
                        "longitude": coords["longitude"],
                        "tags": tags
                    })
                    total_added += 1
                    break  # Only tag one category per POI

        total_count = sum(
            len(subcats)
            for category_data in results_by_category.values()
            for subcats in category_data.values()
        )

        output = {
            "query": {
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius,
                "categories": categories,
                "limit": limit
            },
            "categories": results_by_category,
            "total_count": total_count
        }

        return [TextContent(type="text", text=json.dumps(output, ensure_ascii=False, indent=2))]
