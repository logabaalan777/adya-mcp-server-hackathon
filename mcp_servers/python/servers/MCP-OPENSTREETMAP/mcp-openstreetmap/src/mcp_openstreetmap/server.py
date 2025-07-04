from mcp.server import Server
from dataclasses import dataclass
from typing import AsyncIterator, List, Dict, Optional, Tuple, Any, Union
import aiohttp
import json
import asyncio
from contextlib import asynccontextmanager
import math
from datetime import datetime
import traceback

# Import your tool handlers
from .geocode import GeoCodeToolHandler
from .reverse_geocode import ReverseGeocodeToolHandler
from .find_nearby_places import FindNearbyPlacesToolHandler
from .get_route_directions import GetRouteDirectionsToolHandler
from .search_category import SearchCategoryToolHandler
from .suggest_meeting_point import SuggestMeetingPointToolHandler
from .explore_area import ExploreAreaToolHandler
from .find_schools_nearby import FindSchoolsNearbyToolHandler
from .analyze_commute import AnalyzeCommuteToolHandler
from .find_ev_charging_stations import FindEVChargingStationsToolHandler
from .analyze_neighborhood import AnalyzeNeighborhoodToolHandler
from .find_parking_facilities import FindParkingFacilitiesToolHandler


# -----------------------------
# OSM Client
# -----------------------------
class OSMClient:
    def __init__(self, base_url="https://api.openstreetmap.org/api/0.6"):
        self.base_url = base_url
        self.session = None
        self.cache = {}

    async def connect(self):
        self.session = aiohttp.ClientSession()

    async def disconnect(self):
        if self.session:
            await self.session.close()

    async def geocode(self, query: str):
        if not self.session:
            raise RuntimeError("OSM client not connected")
        nominatim_url = "https://nominatim.openstreetmap.org/search"
        async with self.session.get(
            nominatim_url,
            params={"q": query, "format": "json", "limit": 5},
            headers={"User-Agent": "mcp-openstreetmap/1.0"}
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to geocode '{query}': {response.status}")

    async def reverse_geocode(self, lat: float, lon: float):
        if not self.session:
            raise RuntimeError("OSM client not connected")
        nominatim_url = "https://nominatim.openstreetmap.org/reverse"
        async with self.session.get(
            nominatim_url,
            params={"lat": lat, "lon": lon, "format": "json"},
            headers={"User-Agent": "mcp-openstreetmap/1.0"}
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to reverse geocode ({lat}, {lon}): {response.status}")

    async def get_route(self, from_lat, from_lon, to_lat, to_lon, mode="car", steps=False, overview="overview", annotations=True):
        if not self.session:
            raise RuntimeError("OSM client not connected")
        osrm_url = f"http://router.project-osrm.org/route/v1/{mode}/{from_lon},{from_lat};{to_lon},{to_lat}"
        params = {
            "overview": overview,
            "geometries": "geojson",
            "steps": str(steps).lower(),
            "annotations": str(annotations).lower()
        }
        async with self.session.get(osrm_url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to get route: {response.status}")

    async def get_nearby_pois(self, lat, lon, radius=1000, categories=None):
        if not self.session:
            raise RuntimeError("OSM client not connected")
        lat_delta = radius / 111000
        lon_delta = radius / (111000 * math.cos(math.radians(lat)))
        bbox = (lon - lon_delta, lat - lat_delta, lon + lon_delta, lat + lat_delta)
        overpass_url = "https://overpass-api.de/api/interpreter"
        if not categories:
            categories = ["amenity", "shop", "tourism", "leisure"]
        tag_filters = [f'node["{category}"]({{bbox}});' for category in categories]
        query = f"""
        [out:json];
        (
            {' '.join(tag_filters)}
        );
        out body;
        """
        query = query.replace("{bbox}", f"{bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]}")
        async with self.session.post(overpass_url, data={"data": query}) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("elements", [])
            else:
                raise Exception(f"Failed to get nearby POIs: {response.status}")

    async def search_features_by_category(self, bbox, category, subcategories=None):
        if not self.session:
            raise RuntimeError("OSM client not connected")
        overpass_url = "https://overpass-api.de/api/interpreter"
        if subcategories:
            subcategory_filters = " or ".join([f'"{category}"="{sub}"' for sub in subcategories])
            query_filter = f'({subcategory_filters})'
        else:
            query_filter = f'"{category}"'
        query = f"""
        [out:json];
        (
          node[{query_filter}]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
          way[{query_filter}]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
          relation[{query_filter}]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
        );
        out body;
        """
        async with self.session.post(overpass_url, data={"data": query}) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("elements", [])
            else:
                raise Exception(f"Failed to search features by category: {response.status}")


# -----------------------------
# Context Management
# -----------------------------
@dataclass
class AppContext:
    osm_client: OSMClient


# Global context variable
_app_context: Optional[AppContext] = None


async def get_app_context() -> AppContext:
    """Get the current application context."""
    global _app_context
    if _app_context is None:
        raise RuntimeError("Application context not initialized")
    return _app_context


async def set_app_context(context: AppContext):
    """Set the application context."""
    global _app_context
    _app_context = context


@asynccontextmanager
async def app_lifespan():
    """Application lifespan manager."""
    osm_client = OSMClient()
    try:
        await osm_client.connect()
        app_ctx = AppContext(osm_client=osm_client)
        await set_app_context(app_ctx)
        yield app_ctx
    finally:
        await osm_client.disconnect()


# -----------------------------
# MCP Server Setup
# -----------------------------
app = Server("mcp-openstreetmap")


# -----------------------------
# Tool Handler Registration
# -----------------------------
_tool_handlers = {}

def add_tool_handler(handler):
    print("Registering handler:", handler.name)
    _tool_handlers[handler.name] = handler

def get_tool_handler(name):
    return _tool_handlers.get(name)


# Register your tools here
add_tool_handler(GeoCodeToolHandler())
add_tool_handler(ReverseGeocodeToolHandler())
add_tool_handler(FindNearbyPlacesToolHandler())
add_tool_handler(GetRouteDirectionsToolHandler())
add_tool_handler(SearchCategoryToolHandler())
add_tool_handler(SuggestMeetingPointToolHandler())
add_tool_handler(ExploreAreaToolHandler())
add_tool_handler(FindSchoolsNearbyToolHandler())
add_tool_handler(AnalyzeCommuteToolHandler())
add_tool_handler(FindEVChargingStationsToolHandler())
add_tool_handler(AnalyzeNeighborhoodToolHandler())
add_tool_handler(FindParkingFacilitiesToolHandler())


# -----------------------------
# API Endpoints
# -----------------------------
@app.list_tools()
async def list_tools():
    return [handler.get_tool_description() for handler in _tool_handlers.values()]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        # Get the application context
        app_ctx = await get_app_context()
        
        # Find the handler
        handler = _tool_handlers.get(name)
        if not handler:
            raise ValueError(f"Unknown tool: {name}")
        
        # Create a context object that matches what handlers expect
        class LifespanContext:
            def __init__(self, app_context):
                self.osm_client = app_context.osm_client
        
        class RequestContext:
            def __init__(self, app_context):
                self.lifespan_context = LifespanContext(app_context)
        
        class SimpleContext:
            def __init__(self, app_context):
                self.app_context = app_context
                self.osm_client = app_context.osm_client
                self.request_context = RequestContext(app_context)
        
        ctx = SimpleContext(app_ctx)
        return await handler.run_tool(arguments, ctx)
        
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}


# -----------------------------
# Main Entry Point
# -----------------------------
def main():
    asyncio.run(_main_async())

async def _main_async():
    from mcp.server.stdio import stdio_server
    
    async with app_lifespan():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    main()
