from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .looker_client import looker_client
import httpx

class GetDashboardsToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_looker_dashboards")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Retrieve all dashboards from the Looker instance.",
            inputSchema={
                "type": "object",
                "properties": {
                    "base_url": {
                        "type": "string",
                        "description": "Looker instance base URL (e.g., https://your-company.looker.com)"
                    },
                    "client_id": {
                        "type": "string",
                        "description": "Looker API client ID"
                    },
                    "client_secret": {
                        "type": "string",
                        "description": "Looker API client secret"
                    }
                },
                "required": ["base_url", "client_id", "client_secret"]
            }
        )

    async def run_tool(self, args: dict) -> list[TextContent]:
        base_url = args.get("base_url")
        client_id = args.get("client_id")
        client_secret = args.get("client_secret")

        # Initialize client if not already done
        if not looker_client.is_initialized():
            looker_client.initialize(base_url, client_id, client_secret)

        result = await looker_client.get_dashboards()
        
        if result["success"]:
            dashboards = result["data"]
            if not dashboards:
                return [TextContent(type="text", text="No dashboards found.")]
            
            result_text = "Available Dashboards:\n"
            result_text += "=" * 50 + "\n"
            
            for dashboard in dashboards:
                dashboard_id = dashboard.get("id", "N/A")
                title = dashboard.get("title", "Untitled")
                description = dashboard.get("description", "No description")
                created_at = dashboard.get("created_at", "Unknown")
                
                result_text += f"ID: {dashboard_id}\n"
                result_text += f"Title: {title}\n"
                result_text += f"Description: {description}\n"
                result_text += f"Created: {created_at}\n"
                result_text += "-" * 30 + "\n"
            
            return [TextContent(type="text", text=result_text)]
        else:
            return [TextContent(type="text", text=result["error"])]


class GetDashboardDetailsToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_dashboard_details")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get detailed information about a specific dashboard including its elements and filters.",
            inputSchema={
                "type": "object",
                "properties": {
                    "base_url": {
                        "type": "string",
                        "description": "Looker instance base URL (e.g., https://your-company.looker.com)"
                    },
                    "client_id": {
                        "type": "string",
                        "description": "Looker API client ID"
                    },
                    "client_secret": {
                        "type": "string",
                        "description": "Looker API client secret"
                    },
                    "dashboard_id": {
                        "type": "string",
                        "description": "The ID of the dashboard to get details for"
                    }
                },
                "required": ["base_url", "client_id", "client_secret", "dashboard_id"]
            }
        )

    async def run_tool(self, args: dict) -> list[TextContent]:
        base_url = args.get("base_url")
        client_id = args.get("client_id")
        client_secret = args.get("client_secret")
        dashboard_id = args.get("dashboard_id")

        # Initialize client if not already done
        if not looker_client.is_initialized():
            looker_client.initialize(base_url, client_id, client_secret)

        # Get dashboard details
        url = f"{looker_client.base_url}/api/4.0/dashboards/{dashboard_id}"
        headers = looker_client.get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            dashboard = response.json()
            
            result_text = f"Dashboard Details for ID: {dashboard_id}\n"
            result_text += "=" * 50 + "\n"
            result_text += f"Title: {dashboard.get('title', 'Untitled')}\n"
            result_text += f"Description: {dashboard.get('description', 'No description')}\n"
            result_text += f"Created: {dashboard.get('created_at', 'Unknown')}\n"
            result_text += f"Updated: {dashboard.get('updated_at', 'Unknown')}\n"
            result_text += f"User ID: {dashboard.get('user_id', 'Unknown')}\n"
            
            # Dashboard elements
            elements = dashboard.get('dashboard_elements', [])
            result_text += f"\nDashboard Elements ({len(elements)}):\n"
            result_text += "-" * 30 + "\n"
            
            for i, element in enumerate(elements, 1):
                result_text += f"{i}. Type: {element.get('type', 'Unknown')}\n"
                result_text += f"   Title: {element.get('title', 'Untitled')}\n"
                result_text += f"   Look ID: {element.get('look_id', 'N/A')}\n"
                result_text += f"   Query ID: {element.get('query_id', 'N/A')}\n"
                result_text += "\n"
            
            return [TextContent(type="text", text=result_text)]
        else:
            return [TextContent(type="text", text=f"Failed to get dashboard details: HTTP {response.status_code} - {response.text}")] 