import json
from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent
from mcp.server.fastmcp import Context

class ExploreAreaToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("explore_area")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Generate a comprehensive profile of an area including all amenities and features.",
            inputSchema={
                "latitude": {"type": "number", "description": "Center point latitude (decimal degrees)"},
                "longitude": {"type": "number", "description": "Center point longitude (decimal degrees)"},
                "radius": {"type": "number", "description": "Search radius in meters (default 500)", "optional": True}
            }
        )

    async def run_tool(self, args, ctx: Context):
        latitude = args.get("latitude")
        longitude = args.get("longitude")
        radius = args.get("radius", 500)

        if latitude is None or longitude is None:
            return [TextContent(type="text", text="Missing required parameters: latitude and longitude")]

        osm_client = ctx.request_context.lifespan_context.osm_client
        categories = ["amenity", "shop", "tourism", "leisure", "natural", "historic", "public_transport"]
        results = {}
        import math

        for category in categories:
            # Bounding box computation
            lat_delta = radius / 111000
            lon_delta = radius / (111000 * math.cos(math.radians(latitude)))
            bbox = (
                longitude - lon_delta,
                latitude - lat_delta,
                longitude + lon_delta,
                latitude + lat_delta
            )
            try:
                features = await osm_client.search_features_by_category(bbox, category)
                subcategories = {}

                for feature in features:
                    tags = feature.get("tags", {})
                    subcategory = tags.get(category, "unspecified")

                    coords = {}
                    if feature.get("type") == "node":
                        coords = {
                            "latitude": feature.get("lat"),
                            "longitude": feature.get("lon")
                        }
                    elif "center" in feature:
                        coords = {
                            "latitude": feature["center"].get("lat"),
                            "longitude": feature["center"].get("lon")
                        }

                    if coords:
                        subcategories.setdefault(subcategory, []).append({
                            "id": feature.get("id"),
                            "name": tags.get("name", "Unnamed"),
                            "coordinates": coords,
                            "type": feature.get("type"),
                            "tags": tags
                        })

                results[category] = subcategories
            except Exception as e:
                results[category] = {"error": str(e)}

        # Reverse geocoding
        try:
            address_info = await osm_client.reverse_geocode(latitude, longitude)
        except Exception:
            address_info = {"error": "Could not retrieve address information"}

        # Total feature count
        total_features = 0
        for category_data in results.values():
            if isinstance(category_data, dict):
                for value in category_data.values():
                    if isinstance(value, list):
                        total_features += len(value)

        from datetime import datetime
        output = {
            "query": {
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius
            },
            "address": address_info,
            "categories": results,
            "total_features": total_features,
            "timestamp": datetime.now().isoformat()
        }

        return [TextContent(type="text", text=json.dumps(output, ensure_ascii=False, indent=2))]
