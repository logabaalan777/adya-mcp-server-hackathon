from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .looker_client import looker_client

class GetLooksToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_looker_looks")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Retrieve all looks from the Looker instance.",
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

        result = await looker_client.get_looks()
        
        if result["success"]:
            looks = result["data"]
            if not looks:
                return [TextContent(type="text", text="No looks found.")]
            
            result_text = "Available Looks:\n"
            result_text += "=" * 50 + "\n"
            
            for look in looks:
                look_id = look.get("id", "N/A")
                title = look.get("title", "Untitled")
                description = look.get("description", "No description")
                created_at = look.get("created_at", "Unknown")
                model = look.get("model", {}).get("name", "Unknown")
                explore = look.get("explore", "Unknown")
                
                result_text += f"ID: {look_id}\n"
                result_text += f"Title: {title}\n"
                result_text += f"Description: {description}\n"
                result_text += f"Model: {model}\n"
                result_text += f"Explore: {explore}\n"
                result_text += f"Created: {created_at}\n"
                result_text += "-" * 30 + "\n"
            
            return [TextContent(type="text", text=result_text)]
        else:
            return [TextContent(type="text", text=result["error"])]


class CreateLookToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("create_looker_look")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Create a new look in Looker with specified query parameters.",
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
                    "title": {
                        "type": "string",
                        "description": "Title for the new look"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description for the new look"
                    },
                    "model": {
                        "type": "string",
                        "description": "The Looker model name (e.g., 'my_model')"
                    },
                    "explore": {
                        "type": "string",
                        "description": "The explore name within the model (e.g., 'my_explore')"
                    },
                    "fields": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of fields to select (e.g., ['table.field1', 'table.field2'])"
                    },
                    "filters": {
                        "type": "object",
                        "description": "Optional filters to apply to the query"
                    },
                    "sorts": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional sort fields (e.g., ['field1 desc', 'field2 asc'])"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of rows to return (default: 1000)"
                    }
                },
                "required": ["base_url", "client_id", "client_secret", "title", "model", "explore", "fields"]
            }
        )

    async def run_tool(self, args: dict) -> list[TextContent]:
        base_url = args.get("base_url")
        client_id = args.get("client_id")
        client_secret = args.get("client_secret")
        title = args.get("title")
        description = args.get("description", "")
        model = args.get("model")
        explore = args.get("explore")
        fields = args.get("fields")
        filters = args.get("filters", {})
        sorts = args.get("sorts", [])
        limit = args.get("limit", 1000)

        # Initialize client if not already done
        if not looker_client.is_initialized():
            looker_client.initialize(base_url, client_id, client_secret)

        # Build look data
        look_data = {
            "title": title,
            "description": description,
            "query": {
                "model": model,
                "view": explore,
                "fields": fields,
                "filters": filters,
                "sorts": sorts,
                "limit": limit
            }
        }

        result = await looker_client.create_look(look_data)
        
        if result["success"]:
            look = result["data"]
            look_id = look.get("id", "Unknown")
            return [TextContent(type="text", text=f"Successfully created look '{title}' with ID: {look_id}")]
        else:
            return [TextContent(type="text", text=result["error"])] 