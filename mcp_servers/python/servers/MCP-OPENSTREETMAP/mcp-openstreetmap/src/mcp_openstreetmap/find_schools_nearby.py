import json
import math
import aiohttp
from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent
from mcp.server.fastmcp import Context

class FindSchoolsNearbyToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("find_schools_nearby")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Locate educational institutions near a specific location, filtered by education level.",
            inputSchema={
                "latitude": {"type": "number", "description": "Center point latitude (decimal degrees)"},
                "longitude": {"type": "number", "description": "Center point longitude (decimal degrees)"},
                "radius": {
                    "type": "number",
                    "description": "Search radius in meters (default 2000)",
                    "optional": True
                },
                "education_levels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Education levels to filter by (e.g., elementary, secondary, university)",
                    "optional": True
                }
            }
        )

    async def run_tool(self, args, ctx: Context):
        latitude = args.get("latitude")
        longitude = args.get("longitude")
        radius = args.get("radius", 2000)
        education_levels = args.get("education_levels")

        if latitude is None or longitude is None:
            return [TextContent(type="text", text="Missing required parameters: latitude and longitude")]

        # Calculate bounding box
        lat_delta = radius / 111000
        lon_delta = radius / (111000 * math.cos(math.radians(latitude)))
        bbox = (
            latitude - lat_delta,
            longitude - lon_delta,
            latitude + lat_delta,
            longitude + lon_delta
        )

        # Construct Overpass query
        overpass_url = "https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        (
            node["amenity"~"school|university|kindergarten|college"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
            way["amenity"~"school|university|kindergarten|college"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
            relation["amenity"~"school|university|kindergarten|college"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        );
        out center tags;
        """

        # Query Overpass API
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(overpass_url, data={"data": query}) as response:
                    if response.status != 200:
                        return [TextContent(type="text", text=f"Failed to retrieve schools: HTTP {response.status}")]
                    data = await response.json()
                    schools = data.get("elements", [])
        except Exception as e:
            return [TextContent(type="text", text=f"Overpass API error: {str(e)}")]

        # Distance calculation
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371000
            dLat = math.radians(lat2 - lat1)
            dLon = math.radians(lon2 - lon1)
            a = math.sin(dLat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2)**2
            return 2 * R * math.asin(math.sqrt(a))

        # Filter and format results
        results = []
        for school in schools:
            tags = school.get("tags", {})
            coords = {}

            if school.get("type") == "node":
                coords = {"latitude": school.get("lat"), "longitude": school.get("lon")}
            elif "center" in school:
                coords = {"latitude": school["center"].get("lat"), "longitude": school["center"].get("lon")}

            if not coords.get("latitude") or not coords.get("longitude"):
                continue

            distance = haversine(latitude, longitude, coords["latitude"], coords["longitude"])

            school_type = tags.get("school", "")
            isced_level = tags.get("isced", "")

            # Optional education level filtering
            if education_levels:
                matched = (
                    school_type in education_levels or
                    isced_level in education_levels or
                    tags.get("amenity") in education_levels
                )
                if not matched:
                    continue

            results.append({
                "id": school.get("id"),
                "name": tags.get("name", "Unnamed School"),
                "amenity_type": tags.get("amenity", ""),
                "school_type": school_type,
                "education_level": isced_level,
                "coordinates": coords,
                "distance": round(distance, 1),
                "address": {
                    "street": tags.get("addr:street", ""),
                    "housenumber": tags.get("addr:housenumber", ""),
                    "city": tags.get("addr:city", ""),
                    "postcode": tags.get("addr:postcode", "")
                },
                "tags": tags
            })

        # Sort by distance
        results.sort(key=lambda x: x["distance"])

        output = {
            "query": {
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius,
                "education_levels": education_levels
            },
            "schools": results,
            "count": len(results)
        }

        return [TextContent(type="text", text=json.dumps(output, ensure_ascii=False, indent=2))]
