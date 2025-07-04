import json
import math
from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent
from mcp.server.fastmcp import Context

class FindEVChargingStationsToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("find_ev_charging_stations")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Locate electric vehicle charging stations near a specific location.",
            inputSchema={
                "latitude": {"type": "number", "description": "Center point latitude (decimal degrees)"},
                "longitude": {"type": "number", "description": "Center point longitude (decimal degrees)"},
                "radius": {"type": "number", "description": "Search radius in meters (default 5000)", "optional": True},
                "connector_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Connector types to filter by (e.g., type2, ccs, tesla)",
                    "optional": True
                },
                "min_power": {"type": "number", "description": "Minimum charging power in kW", "optional": True}
            }
        )

    async def run_tool(self, args, ctx: Context):
        latitude = args.get("latitude")
        longitude = args.get("longitude")
        radius = args.get("radius", 5000)
        connector_types = args.get("connector_types")
        min_power = args.get("min_power")

        if latitude is None or longitude is None:
            return [TextContent(type="text", text="Missing required parameters: latitude and longitude")]

        # Bounding box calculation
        lat_delta = radius / 111000
        lon_delta = radius / (111000 * math.cos(math.radians(latitude)))
        bbox = (
            longitude - lon_delta,
            latitude - lat_delta,
            longitude + lon_delta,
            latitude + lat_delta
        )

        # Build Overpass query
        overpass_url = "https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        (
            node["amenity"="charging_station"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
            way["amenity"="charging_station"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
        );
        out center;
        """

        # Fetch from Overpass API
        import aiohttp
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(overpass_url, data={"data": query}) as response:
                    if response.status == 200:
                        data = await response.json()
                        stations = data.get("elements", [])
                    else:
                        return [TextContent(type="text", text=f"Failed to retrieve charging stations: HTTP {response.status}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error connecting to Overpass API: {str(e)}")]

        # Haversine distance calculator
        from math import radians, sin, cos, sqrt, asin

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371000
            dLat = radians(lat2 - lat1)
            dLon = radians(lon2 - lon1)
            a = sin(dLat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon / 2) ** 2
            c = 2 * asin(sqrt(a))
            return R * c

        results = []

        for station in stations:
            tags = station.get("tags", {})
            coords = {}

            if station.get("type") == "node":
                coords = {
                    "latitude": station.get("lat"),
                    "longitude": station.get("lon")
                }
            elif "center" in station:
                coords = {
                    "latitude": station["center"].get("lat"),
                    "longitude": station["center"].get("lon")
                }

            if not coords:
                continue  # skip if coordinates can't be resolved

            # Parse connectors
            connectors = []
            for key, value in tags.items():
                if key.startswith("socket:"):
                    connector_type = key.split(":", 1)[1]
                    try:
                        count = int(value) if value.isdigit() else 1
                    except:
                        count = 1
                    connectors.append({
                        "type": connector_type,
                        "count": count
                    })

            # Filter connectors
            if connector_types:
                if not any(connector["type"] in connector_types for connector in connectors):
                    continue

            # Parse power
            power = None
            if "maxpower" in tags:
                try:
                    power = float(tags["maxpower"])
                except ValueError:
                    pass

            # Filter power
            if min_power is not None and (power is None or power < min_power):
                continue

            distance = haversine(latitude, longitude, coords["latitude"], coords["longitude"])

            results.append({
                "id": station.get("id"),
                "name": tags.get("name", "Unnamed Charging Station"),
                "operator": tags.get("operator", "Unknown"),
                "coordinates": coords,
                "distance": round(distance, 1),
                "connectors": connectors,
                "capacity": tags.get("capacity", "Unknown"),
                "power": power,
                "fee": tags.get("fee", "Unknown"),
                "access": tags.get("access", "public"),
                "opening_hours": tags.get("opening_hours", "Unknown"),
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
                "connector_types": connector_types,
                "min_power": min_power
            },
            "stations": results,
            "count": len(results)
        }

        return [TextContent(type="text", text=json.dumps(output, ensure_ascii=False, indent=2))]
