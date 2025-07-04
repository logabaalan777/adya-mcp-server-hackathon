import json
from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent
from mcp.server.fastmcp import Context

class GetRouteDirectionsToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_route_directions")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Calculate detailed route directions between two geographic points.",
            inputSchema={
                "from_latitude": {"type": "number", "description": "Starting point latitude (decimal degrees)"},
                "from_longitude": {"type": "number", "description": "Starting point longitude (decimal degrees)"},
                "to_latitude": {"type": "number", "description": "Destination latitude (decimal degrees)"},
                "to_longitude": {"type": "number", "description": "Destination longitude (decimal degrees)"},
                "mode": {
                    "type": "string",
                    "description": "Transportation mode (car, bike, foot). Default is car.",
                    "optional": True
                },
                "steps": {
                    "type": "boolean",
                    "description": "Include turn-by-turn instructions. Default is false.",
                    "optional": True
                },
                "overview": {
                    "type": "string",
                    "description": "Geometry detail (full, simplified, false). Default is simplified.",
                    "optional": True
                },
                "annotations": {
                    "type": "boolean",
                    "description": "Include extra route data like speed/duration. Default is false.",
                    "optional": True
                }
            }
        )

    async def run_tool(self, args, ctx: Context):
        # Extract parameters
        from_latitude = args.get("from_latitude")
        from_longitude = args.get("from_longitude")
        to_latitude = args.get("to_latitude")
        to_longitude = args.get("to_longitude")
        mode = args.get("mode", "car")
        steps = args.get("steps", False)
        overview = args.get("overview", "simplified")
        annotations = args.get("annotations", False)

        # Validate coordinates
        if None in (from_latitude, from_longitude, to_latitude, to_longitude):
            return [TextContent(type="text", text="Missing required parameters: from_latitude, from_longitude, to_latitude, to_longitude")]

        # Validate mode
        valid_modes = ["car", "bike", "foot"]
        if mode not in valid_modes:
            # Use safe logging
            if hasattr(ctx, "warning"):
                ctx.warning(f"Invalid mode '{mode}'. Falling back to 'car'.")
            mode = "car"

        # Safe info log
        if hasattr(ctx, "info"):
            ctx.info(f"Calculating {mode} route from ({from_latitude}, {from_longitude}) to ({to_latitude}, {to_longitude})")

        # Get OSM client
        osm_client = ctx.request_context.lifespan_context.osm_client

        try:
            route_data = await osm_client.get_route(
                from_latitude, from_longitude,
                to_latitude, to_longitude,
                mode,
                steps=steps,
                overview=overview,
                annotations=annotations
            )
        except Exception as e:
            return [TextContent(type="text", text=f"Error while retrieving route: {str(e)}")]

        # Process response
        if "routes" in route_data and route_data["routes"]:
            route = route_data["routes"][0]
            steps_list = []

            for leg in route.get("legs", []):
                for step in leg.get("steps", []):
                    maneuver = step.get("maneuver", {})
                    steps_list.append({
                        "instruction": maneuver.get("instruction") or f"{maneuver.get('type', '')} {step.get('name', '')}",
                        "distance": round(step.get("distance", 0), 2),
                        "duration": round(step.get("duration", 0), 2),
                        "name": step.get("name", "")
                    })

            output = {
                "summary": {
                    "distance_meters": round(route.get("distance", 0), 2),
                    "duration_seconds": round(route.get("duration", 0), 2),
                    "mode": mode
                },
                "directions": steps_list if steps else [],
                "geometry": route.get("geometry") if overview != "false" else None,
                "waypoints": route_data.get("waypoints", [])
            }

            return [TextContent(type="text", text=json.dumps(output, ensure_ascii=False, indent=2))]

        else:
            return [TextContent(type="text", text="No route found between the specified points.")]
