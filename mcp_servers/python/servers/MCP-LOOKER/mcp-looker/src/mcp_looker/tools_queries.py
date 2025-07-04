from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .looker_client import looker_client
import json

class RunLookerQueryToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("run_looker_query")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Run a Looker query and return the results in a formatted table.",
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
                "required": ["base_url", "client_id", "client_secret", "model", "explore", "fields"]
            }
        )

    async def run_tool(self, args: dict) -> list[TextContent]:
        base_url = args.get("base_url")
        client_id = args.get("client_id")
        client_secret = args.get("client_secret")
        model = args.get("model")
        explore = args.get("explore")
        fields = args.get("fields")
        filters = args.get("filters", {})
        sorts = args.get("sorts", [])
        limit = args.get("limit", 1000)

        # Initialize client if not already done
        if not looker_client.is_initialized():
            looker_client.initialize(base_url, client_id, client_secret)

        # Build query
        query = {
            "model": model,
            "view": explore,
            "fields": fields,
            "filters": filters,
            "sorts": sorts,
            "limit": limit
        }

        result = await looker_client.run_query(query)
        
        if result["success"]:
            data = result["data"]
            formatted_results = looker_client.format_query_results(data)
            return [TextContent(type="text", text=formatted_results)]
        else:
            return [TextContent(type="text", text=result["error"])]


class GetModelsToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_looker_models")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Retrieve all available data models from the Looker instance.",
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

        result = await looker_client.get_models()
        
        if result["success"]:
            models = result["data"]
            if not models:
                return [TextContent(type="text", text="No models found.")]
            
            result_text = "Available Data Models:\n"
            result_text += "=" * 50 + "\n"
            
            for model in models:
                name = model.get("name", "Unknown")
                label = model.get("label", "No label")
                description = model.get("description", "No description")
                
                result_text += f"Name: {name}\n"
                result_text += f"Label: {label}\n"
                result_text += f"Description: {description}\n"
                result_text += "-" * 30 + "\n"
            
            return [TextContent(type="text", text=result_text)]
        else:
            return [TextContent(type="text", text=result["error"])]


class GetExploresToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_looker_explores")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get all explores (views) available in a specific Looker model.",
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
                    "model_name": {
                        "type": "string",
                        "description": "The name of the model to get explores for"
                    }
                },
                "required": ["base_url", "client_id", "client_secret", "model_name"]
            }
        )

    async def run_tool(self, args: dict) -> list[TextContent]:
        base_url = args.get("base_url")
        client_id = args.get("client_id")
        client_secret = args.get("client_secret")
        model_name = args.get("model_name")

        # Initialize client if not already done
        if not looker_client.is_initialized():
            looker_client.initialize(base_url, client_id, client_secret)

        result = await looker_client.get_explores(model_name)
        
        if result["success"]:
            explores = result["data"]
            if not explores:
                return [TextContent(type="text", text=f"No explores found for model '{model_name}'.")]
            
            result_text = f"Available Explores in Model '{model_name}':\n"
            result_text += "=" * 50 + "\n"
            
            for explore in explores:
                name = explore.get("name", "Unknown")
                label = explore.get("label", "No label")
                description = explore.get("description", "No description")
                
                result_text += f"Name: {name}\n"
                result_text += f"Label: {label}\n"
                result_text += f"Description: {description}\n"
                result_text += "-" * 30 + "\n"
            
            return [TextContent(type="text", text=result_text)]
        else:
            return [TextContent(type="text", text=result["error"])] 