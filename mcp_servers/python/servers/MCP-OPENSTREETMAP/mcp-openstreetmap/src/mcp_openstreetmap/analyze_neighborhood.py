import json
import math
from datetime import datetime
from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent
from mcp.server.fastmcp import Context

class AnalyzeNeighborhoodToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("analyze_neighborhood")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Generate a comprehensive neighborhood analysis focused on livability factors.",
            inputSchema={
                "latitude": {"type": "number", "description": "Center point latitude (decimal degrees)"},
                "longitude": {"type": "number", "description": "Center point longitude (decimal degrees)"},
                "radius": {"type": "number", "description": "Analysis radius in meters (default 1000)", "optional": True}
            }
        )

    async def run_tool(self, args, ctx: Context):
        latitude = args.get("latitude")
        longitude = args.get("longitude")
        radius = args.get("radius", 1000)

        if latitude is None or longitude is None:
            return [TextContent(type="text", text="Missing required parameters: latitude and longitude")]

        osm_client = ctx.request_context.lifespan_context.osm_client

        categories = [
            {"name": "groceries", "tags": ["shop=supermarket", "shop=convenience", "shop=grocery"]},
            {"name": "restaurants", "tags": ["amenity=restaurant", "amenity=cafe", "amenity=fast_food"]},
            {"name": "healthcare", "tags": ["amenity=hospital", "amenity=doctors", "amenity=pharmacy"]},
            {"name": "education", "tags": ["amenity=school", "amenity=kindergarten", "amenity=university"]},
            {"name": "public_transport", "tags": ["public_transport=stop_position", "railway=station", "amenity=bus_station"]},
            {"name": "parks", "tags": ["leisure=park", "leisure=garden", "leisure=playground"]},
            {"name": "sports", "tags": ["leisure=sports_centre", "leisure=fitness_centre", "leisure=swimming_pool"]},
            {"name": "entertainment", "tags": ["amenity=theatre", "amenity=cinema", "amenity=arts_centre"]},
            {"name": "shopping", "tags": ["shop=mall", "shop=department_store", "shop=clothes"]},
            {"name": "services", "tags": ["amenity=bank", "amenity=post_office", "amenity=atm"]}
        ]

        results = {}
        scores = {}

        lat_delta = radius / 111000
        lon_delta = radius / (111000 * math.cos(math.radians(latitude)))
        bbox = (
            longitude - lon_delta,
            latitude - lat_delta,
            longitude + lon_delta,
            latitude + lat_delta
        )

        import aiohttp
        from math import radians, sin, cos, sqrt, asin

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371000
            d_lat = radians(lat2 - lat1)
            d_lon = radians(lon2 - lon1)
            a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
            c = 2 * asin(sqrt(a))
            return R * c

        for category in categories:
            tag_filters = []
            for tag in category["tags"]:
                key, value = tag.split("=")
                tag_filters.append(f'node["{key}"="{value}"]({{bbox}});')
                tag_filters.append(f'way["{key}"="{value}"]({{bbox}});')

            query = f"""
            [out:json];
            (
                {' '.join(tag_filters)}
            );
            out center;
            """.replace("{bbox}", f"{bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]}")

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post("https://overpass-api.de/api/interpreter", data={"data": query}) as response:
                        if response.status == 200:
                            data = await response.json()
                            features = data.get("elements", [])
                        else:
                            features = []

                feature_list = []
                distances = []

                for feature in features:
                    tags = feature.get("tags", {})
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

                    if not coords:
                        continue

                    distance = haversine(latitude, longitude, coords["latitude"], coords["longitude"])
                    distances.append(distance)
                    feature_list.append({
                        "id": feature.get("id"),
                        "name": tags.get("name", "Unnamed"),
                        "type": feature.get("type"),
                        "coordinates": coords,
                        "distance": round(distance, 1),
                        "tags": tags
                    })

                feature_list.sort(key=lambda x: x["distance"])
                count = len(feature_list)
                avg_distance = sum(distances) / count if count > 0 else None
                min_distance = min(distances) if count > 0 else None

                if count == 0:
                    category_score = 0
                else:
                    count_score = min(count / 5, 1) * 5
                    proximity_score = 5 - min(min_distance / radius, 1) * 5
                    category_score = round(count_score + proximity_score, 1)

                results[category["name"]] = {
                    "count": count,
                    "features": feature_list[:10],
                    "metrics": {
                        "total_count": count,
                        "avg_distance": round(avg_distance, 1) if avg_distance else None,
                        "min_distance": round(min_distance, 1) if min_distance else None
                    }
                }
                scores[category["name"]] = category_score

            except Exception as e:
                ctx.warning(f"Error analyzing category {category['name']}: {e}")
                results[category["name"]] = {"error": str(e)}
                scores[category["name"]] = 0

        # Scores
        overall_score = round(sum(scores.values()) / len(scores), 1) if scores else 0

        walkable_amenities = 0
        walkable_categories = 0
        for category_name, category_data in results.items():
            if "features" in category_data:
                walking_count = sum(1 for feature in category_data["features"] if feature["distance"] <= 500)
                if walking_count > 0:
                    walkable_amenities += walking_count
                    walkable_categories += 1
        walkability_score = min(walkable_amenities + walkable_categories, 10)

        try:
            address_info = await osm_client.reverse_geocode(latitude, longitude)
        except Exception:
            address_info = {"display_name": "Unknown location"}

        output = {
            "location": {
                "coordinates": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "address": address_info.get("display_name", "Unknown location")
            },
            "scores": {
                "overall": overall_score,
                "walkability": walkability_score,
                "categories": {k: round(v, 1) for k, v in scores.items()}
            },
            "categories": results,
            "analysis_radius": radius,
            "timestamp": datetime.now().isoformat()
        }

        return [TextContent(type="text", text=json.dumps(output, ensure_ascii=False, indent=2))]
