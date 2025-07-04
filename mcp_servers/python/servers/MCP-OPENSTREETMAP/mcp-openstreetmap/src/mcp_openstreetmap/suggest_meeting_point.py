import json
import logging
from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent
from mcp.server.fastmcp import Context

logger = logging.getLogger(__name__)

class SuggestMeetingPointToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("suggest_meeting_point")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Find the optimal meeting place for multiple people coming from different locations.",
            inputSchema={
                "locations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "latitude": {"type": "number"},
                            "longitude": {"type": "number"}
                        },
                        "required": ["latitude", "longitude"]
                    },
                    "description": "List of locations, each with latitude and longitude"
                },
                "venue_type": {
                    "type": "string",
                    "description": "Type of venue to suggest as a meeting point (e.g., cafe, restaurant, bar, library, park, etc.)",
                    "optional": True
                }
            }
        )

    async def run_tool(self, args, ctx: Context):
        locations = args.get("locations")
        venue_type = args.get("venue_type", "cafe")

        if not locations or not isinstance(locations, list) or len(locations) < 2:
            return [TextContent(type="text", text="Need at least two locations to suggest a meeting point.")]

        osm_client = ctx.request_context.lifespan_context.osm_client

        # Calculate average (central) latitude and longitude
        avg_lat = sum(loc.get("latitude", 0) for loc in locations) / len(locations)
        avg_lon = sum(loc.get("longitude", 0) for loc in locations) / len(locations)

        logger.info(f"Center point for {len(locations)} locations: ({avg_lat}, {avg_lon})")
        
        # Try searching in radius = 500m first
        matching_venues = await self._search_venues(osm_client, avg_lat, avg_lon, venue_type, 500)

        # If no match, try with 1000m
        if not matching_venues:
            logger.info(f"No '{venue_type}' found within 500m. Expanding to 1000m...")
            matching_venues = await self._search_venues(osm_client, avg_lat, avg_lon, venue_type, 1000)

        output = {
            "center_point": {
                "latitude": avg_lat,
                "longitude": avg_lon
            },
            "venue_type": venue_type,
            "total_options": len(matching_venues),
            "suggested_venues": matching_venues[:5]  # Return top 5 matches
        }

        return [TextContent(type="text", text=json.dumps(output, ensure_ascii=False, indent=2))]

    async def _search_venues(self, osm_client, lat, lon, venue_type, radius):
        results = []
        try:
            venues = await osm_client.get_nearby_pois(
                lat, lon, radius=radius, categories=["amenity"]
            )
        except Exception as e:
            logger.warning(f"OSM query failed: {e}")
            return results

        for venue in venues:
            tags = venue.get("tags", {})
            if tags.get("amenity") == venue_type:
                results.append({
                    "id": venue.get("id"),
                    "name": tags.get("name", "Unnamed Venue"),
                    "latitude": venue.get("lat"),
                    "longitude": venue.get("lon"),
                    "tags": tags
                })
        return results
