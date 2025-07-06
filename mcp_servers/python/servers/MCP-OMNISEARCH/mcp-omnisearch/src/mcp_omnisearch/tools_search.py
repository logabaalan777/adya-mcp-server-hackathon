from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent
from .omnisearch_client import OmnisearchClient

class BraveSearchToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("brave")

    def get_tool_description(self) -> Tool:
        return Tool(
            name="brave",
            description="Privacy-focused search engine with good coverage of technical topics. Features native support for search operators (site:, filetype:, intitle:, inurl:, before:, after:, and exact phrases). Best for technical documentation, developer resources, and privacy-sensitive queries.",
            inputSchema={
                "api_key": {"type": "string", "description": "Brave API key (required)"},
                "query": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "description": "Number of results to return", "default": 3},
                "include_domains": {"type": "array", "items": {"type": "string"}, "description": "Domains to include in search results", "default": []},
                "exclude_domains": {"type": "array", "items": {"type": "string"}, "description": "Domains to exclude from search results", "default": []},
            },
            required=["api_key", "query"]
        )

    def run_tool(self, args: dict):
        api_key = args.get("api_key")
        client = OmnisearchClient(api_key)
        query = args.get("query", "")
        limit = args.get("limit", 3)
        include_domains = args.get("include_domains", [])
        exclude_domains = args.get("exclude_domains", [])
        results = client.search_brave(query, limit, include_domains, exclude_domains)
        formatted = "\n\n".join(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['snippet']}" for r in results
        )
        return [TextContent(type="text", text=formatted)]

class TavilySearchToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("tavily")

    def get_tool_description(self) -> Tool:
        return Tool(
            name="tavily",
            description="Search the web using Tavily Search API. Best for factual queries requiring reliable sources and citations. Supports domain filtering through API parameters (include_domains/exclude_domains). Provides high-quality results for technical, scientific, and academic topics. Use when you need verified information with strong citation support.",
            inputSchema={
                "api_key": {"type": "string", "description": "Tavily API key (required)"},
                "query": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "description": "Number of results to return", "default": 3},
                "include_domains": {"type": "array", "items": {"type": "string"}, "description": "Domains to include in search results", "default": []},
                "exclude_domains": {"type": "array", "items": {"type": "string"}, "description": "Domains to exclude from search results", "default": []},
            },
            required=["api_key", "query"]
        )

    def run_tool(self, args: dict):
        api_key = args.get("api_key")
        client = OmnisearchClient(api_key)
        query = args.get("query", "")
        limit = args.get("limit", 3)
        include_domains = args.get("include_domains", [])
        exclude_domains = args.get("exclude_domains", [])
        results = client.search_tavily(query, limit, include_domains, exclude_domains)
        formatted = "\n\n".join(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['snippet']}" for r in results
        )
        return [TextContent(type="text", text=formatted)]

class PerplexitySearchToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("perplexity")

    def get_tool_description(self) -> Tool:
        return Tool(
            name="perplexity",
            description="AI-powered response generation combining real-time web search with advanced language models. Best for complex queries requiring reasoning and synthesis across multiple sources. Features contextual memory for follow-up questions.",
            inputSchema={
                "api_key": {"type": "string", "description": "Perplexity API key (required)"},
                "query": {"type": "string", "description": "Query for Perplexity AI"},
                "limit": {"type": "integer", "description": "Number of results to return", "default": 2},
            },
            required=["api_key", "query"]
        )

    def run_tool(self, args: dict):
        api_key = args.get("api_key")
        client = OmnisearchClient(api_key)
        query = args.get("query", "")
        limit = args.get("limit", 2)
        results = client.search_perplexity(query, limit)
        formatted = "\n\n".join(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['snippet']}" for r in results
        )
        return [TextContent(type="text", text=formatted)]