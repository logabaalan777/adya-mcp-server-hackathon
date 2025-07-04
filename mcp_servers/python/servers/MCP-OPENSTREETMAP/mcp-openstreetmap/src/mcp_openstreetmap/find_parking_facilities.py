import json
import math
from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent
import aiohttp
from mcp.server.fastmcp import Context

class FindParkingFacilitiesToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("find_parking_facilities")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Locate parking facilities near a specific location.",
            inputSchema={
                "latitude": {"type": "number", "description": "Center point latitude (decimal degrees)"},
                "longitude": {"type": "number", "description": "Center point longitude (decimal degrees)"},
                "radius": {
                    "type": "number",
                    "description": "Search radius in meters (default 1000)",
                    "optional": True
                },
                "parking_type": {
                    "type": "string",
                    "description": "Type of parking facility (surface, underground, multi-storey, etc.)",
                    "optional": True
                }
            }
        )

    async def run_tool(self, args, ctx: Context):
        latitude = args.get("latitude")
        longitude = args.get("longitude")
        radius = args.get("radius", 1000)
        parking_type = args.get("parking_type")

        if latitude is None or longitude is None:
            return [TextContent(type="text", text="Missing required parameters: latitude and longitude")]

        # Calculate bounding box
        lat_delta = radius / 111000
        lon_delta = radius / (111000 * math.cos(math.radians(latitude)))
        bbox = (
            longitude - lon_delta,
            latitude - lat_delta,
            longitude + lon_delta,
            latitude + lat_delta
        )

        # Format Overpass query
        overpass_url = "https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        (
            node["amenity"="parking"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
            way["amenity"="parking"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
            relation["amenity"="parking"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
        );
        out center tags;
        """

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(overpass_url, data={"data": query}) as response:
                    if response.status != 200:
                        return [TextContent(type="text", text=f"Failed to retrieve parking data: HTTP {response.status}")]
                    data = await response.json()
                    parking_facilities = data.get("elements", [])
        except Exception as e:
            return [TextContent(type="text", text=f"Error contacting Overpass API: {str(e)}")]

        # Distance calculation helper
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371000
            dLat = math.radians(lat2 - lat1)
            dLon = math.radians(lon2 - lon1)
            a = math.sin(dLat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2)**2
            return 2 * R * math.asin(math.sqrt(a))

        results = []
        for facility in parking_facilities:
            tags = facility.get("tags", {})
            if parking_type and tags.get("parking") != parking_type:
                continue

            coords = {}
            if facility.get("type") == "node":
                coords = {"latitude": facility.get("lat"), "longitude": facility.get("lon")}
            elif "center" in facility:
                coords = {"latitude": facility["center"].get("lat"), "longitude": facility["center"].get("lon")}

            if not coords.get("latitude") or not coords.get("longitude"):
                continue

            distance = haversine(latitude, longitude, coords["latitude"], coords["longitude"])
            results.append({
                "id": facility.get("id"),
                "name": tags.get("name", "Unnamed Parking"),
                "type": tags.get("parking", "surface"),
                "coordinates": coords,
                "distance": round(distance, 1),
                "capacity": tags.get("capacity", "Unknown"),
                "fee": tags.get("fee", "Unknown"),
                "access": tags.get("access", "public"),
                "opening_hours": tags.get("opening_hours", "Unknown"),
                "levels": tags.get("levels", "1"),
                "address": {
                    "street": tags.get("addr:street", ""),
                    "housenumber": tags.get("addr:housenumber", ""),
                    "city": tags.get("addr:city", ""),
                    "postcode": tags.get("addr:postcode", "")
                },
                "tags": tags
            })

        results.sort(key=lambda x: x["distance"])

        output = {
            "query": {
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius,
                "parking_type": parking_type
            },
            "parking_facilities": results,
            "count": len(results)
        }

        return [TextContent(type="text", text=json.dumps(output, ensure_ascii=False, indent=2))]
