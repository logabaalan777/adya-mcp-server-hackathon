from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
from .joomla_client import joomla_client

class GetArticlesToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_joomla_articles")
    
    # mcp-joomla get_joomla_articles
    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Retrieve all articles from the Joomla website.",
            inputSchema={
                "type": "object",
                "properties": {
                    "base_url": {
                        "type": "string",
                        "description": "Joomla website base URL (e.g., https://example.com)"
                    },
                    "bearer_token": {
                        "type": "string",
                        "description": "Bearer token for Joomla API authentication"
                    }
                },
                "required": ["base_url", "bearer_token"]
            }
        )

    async def run_tool(self, args: dict) -> list[TextContent]:
        base_url = args.get("base_url")
        bearer_token = args.get("bearer_token")

        # Initialize client if not already done
        if not joomla_client.is_initialized():
            joomla_client.initialize(base_url, bearer_token)

        result = await joomla_client.get_articles()
        
        if result["success"]:
            return [TextContent(type="text", text=result["data"])]
        else:
            return [TextContent(type="text", text=result["error"])]


class CreateArticleToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("create_article")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Create a new article on the Joomla website.",
            inputSchema={
                "type": "object",
                "properties": {
                    "base_url": {
                        "type": "string",
                        "description": "Joomla website base URL (e.g., https://example.com)"
                    },
                    "bearer_token": {
                        "type": "string",
                        "description": "Bearer token for Joomla API authentication"
                    },
                    "article_text": {
                        "type": "string",
                        "description": "The content of the article (plain text or HTML)"
                    },
                    "title": {
                        "type": "string",
                        "description": "The article title. Inferred from content if not provided"
                    },
                    "category_id": {
                        "type": "integer",
                        "description": "The ID of the category"
                    },
                    "convert_plain_text": {
                        "type": "boolean",
                        "description": "Convert plain text to HTML if True",
                        "default": True
                    },
                    "published": {
                        "type": "boolean",
                        "description": "Publish the article (True for state=1, False for state=0)",
                        "default": True
                    }
                },
                "required": ["base_url", "bearer_token", "article_text", "category_id"]
            }
        )

    async def run_tool(self, args: dict) -> list[TextContent]:
        base_url = args.get("base_url")
        bearer_token = args.get("bearer_token")
        article_text = args.get("article_text")
        title = args.get("title")
        category_id = args.get("category_id")
        convert_plain_text = args.get("convert_plain_text", True)
        published = args.get("published", True)

        # Initialize client if not already done
        if not joomla_client.is_initialized():
            joomla_client.initialize(base_url, bearer_token)

        # Validate category_id
        if not isinstance(category_id, int):
            return [TextContent(type="text", text="Error: Category ID must be an integer.")]

        # Convert text if needed
        if convert_plain_text:
            article_text = joomla_client.convert_text_to_html(article_text)

        # Generate title if not provided
        if not title:
            title = (
                article_text[:50].strip() + "..."
                if len(article_text) > 50
                else article_text
            )
            title = title.replace("\n", " ").strip()

        # Generate alias
        alias = joomla_client.generate_alias(title)

        # Validate category exists
        categories_result = await joomla_client.get_categories()
        if not categories_result["success"]:
            return [TextContent(type="text", text=categories_result["error"])]

        categories = categories_result["data"]
        if not categories:
            return [TextContent(type="text", text="Failed to create article: No valid categories found.")]

        valid_category = any(
            category.get("attributes", {}).get("id") == category_id
            for category in categories
        )
        if not valid_category:
            return [TextContent(type="text", text=f"Error: Category ID {category_id} is not valid.")]

        # Prepare payload
        payload = {
            "alias": alias,
            "articletext": article_text,
            "catid": category_id,
            "language": "*",
            "metadesc": "",
            "metakey": "",
            "title": title,
            "state": 1 if published else 0,
        }

        # Create article
        result = await joomla_client.create_article(payload)
        
        if result["success"]:
            status = "published" if published else "unpublished"
            return [TextContent(type="text", text=f"Successfully created {status} article '{title}' in category ID {category_id}")]
        else:
            return [TextContent(type="text", text=result["error"])] 