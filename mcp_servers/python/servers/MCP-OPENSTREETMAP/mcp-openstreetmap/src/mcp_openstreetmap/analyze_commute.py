import json
from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent
from mcp.server.fastmcp import Context

class AnalyzeCommuteToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("analyze_commute")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Perform a detailed commute analysis between home and work locations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "home_latitude": {
                        "type": "number",
                        "description": "Home location latitude (decimal degrees)"
                    },
                    "home_longitude": {
                        "type": "number",
                        "description": "Home location longitude (decimal degrees)"
                    },
                    "work_latitude": {
                        "type": "number",
                        "description": "Workplace location latitude (decimal degrees)"
                    },
                    "work_longitude": {
                        "type": "number",
                        "description": "Workplace location longitude (decimal degrees)"
                    },
                    "modes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Transportation modes to analyze (car, foot, bike)",
                        "optional": True
                    },
                    "depart_at": {
                        "type": "string",
                        "description": "Optional departure time (format: HH:MM)",
                        "optional": True
                    }
                }
            }
        )

    async def run_tool(self, args, ctx: Context):
        home_latitude = args.get("home_latitude")
        home_longitude = args.get("home_longitude")
        work_latitude = args.get("work_latitude")
        work_longitude = args.get("work_longitude")
        modes = args.get("modes") or ["car", "foot", "bike"]
        depart_at = args.get("depart_at")

        if None in (home_latitude, home_longitude, work_latitude, work_longitude):
            return [TextContent(type="text", text="Missing required parameters: home_latitude, home_longitude, work_latitude, work_longitude")]

        osm_client = ctx.request_context.lifespan_context.osm_client

        try:
            home_info = await osm_client.reverse_geocode(home_latitude, home_longitude)
        except Exception as e:
            home_info = {"display_name": f"Error fetching home address: {e}"}

        try:
            work_info = await osm_client.reverse_geocode(work_latitude, work_longitude)
        except Exception as e:
            work_info = {"display_name": f"Error fetching work address: {e}"}

        commute_options = []

        for mode in modes:
            try:
                route_data = await osm_client.get_route(
                    home_latitude, home_longitude,
                    work_latitude, work_longitude,
                    mode
                )
                if "routes" in route_data and route_data["routes"]:
                    route = route_data["routes"][0]
                    steps = []
                    for leg in route.get("legs", []):
                        for step in leg.get("steps", []):
                            steps.append({
                                "instruction": step.get("maneuver", {}).get("instruction", ""),
                                "distance_m": step.get("distance"),
                                "duration_s": step.get("duration"),
                                "road_name": step.get("name", "")
                            })
                    commute_options.append({
                        "mode": mode,
                        "distance_km": round(route.get("distance", 0) / 1000, 2),
                        "duration_minutes": round(route.get("duration", 0) / 60, 1),
                        "directions": steps
                    })
            except Exception as e:
                print(f"[Warning] Error getting {mode} route: {str(e)}")  # Replaced ctx.warning
                commute_options.append({
                    "mode": mode,
                    "error": str(e)
                })

        commute_options.sort(key=lambda x: x.get("duration_minutes", float("inf")))

        result = {
            "home": {
                "coordinates": {
                    "latitude": home_latitude,
                    "longitude": home_longitude
                },
                "address": home_info.get("display_name", "Unknown location")
            },
            "work": {
                "coordinates": {
                    "latitude": work_latitude,
                    "longitude": work_longitude
                },
                "address": work_info.get("display_name", "Unknown location")
            },
            "commute_options": commute_options,
            "fastest_option": commute_options[0]["mode"] if commute_options and "mode" in commute_options[0] else None,
            "depart_at": depart_at
        }

        # return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        # return [TextContent(type="text", text=json.dumps(result, separators=(',', ':')))]
        # return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False, separators=(',', ':')))]
        # return [{"type": "text", "text": json.dumps(result, indent=2, ensure_ascii=False)}]
        return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False, separators=(',', ':')))]

