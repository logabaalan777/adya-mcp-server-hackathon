from .toolhandler import ToolHandler
from mcp.types import Tool, TextContent
from .omnisearch_client import OmnisearchClient

class FirecrawlActionsToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("firecrawl_actions")

    def get_tool_description(self) -> Tool:
        return Tool(
            name="firecrawl_actions",
            description="Support for page interactions (clicking, scrolling, etc.) before extraction for dynamic content using Firecrawl. Enables extraction from JavaScript-heavy sites, single-page applications, and content behind user interactions. Best for accessing content that requires navigation, form filling, or other interactions.",
            inputSchema={
                "api_key": {"type": "string", "description": "Firecrawl API key (required)"},
                "url": {"type": "string", "description": "URL to process"},
                "extract_depth": {"type": "string", "enum": ["basic", "advanced"], "default": "basic", "description": "Extraction depth"},
            },
            required=["api_key", "url"]
        )

    def run_tool(self, args: dict):
        api_key = args.get("api_key")
        client = OmnisearchClient(api_key)
        url = args.get("url", "")
        extract_depth = args.get("extract_depth", "basic")
        result = client.firecrawl_actions(url, extract_depth)
        return [TextContent(type="text", text=result.get("result", str(result)))]

class FirecrawlCrawlToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("firecrawl_crawl")

    def get_tool_description(self) -> Tool:
        return Tool(
            name="firecrawl_crawl",
            description="Deep crawling of all accessible subpages on a website with configurable depth limits using Firecrawl. Efficiently discovers and extracts content from multiple pages within a domain. Best for comprehensive site analysis, content indexing, and data collection from entire websites.",
            inputSchema={
                "api_key": {"type": "string", "description": "Firecrawl API key (required)"},
                "url": {"type": "string", "description": "URL to crawl"},
                "extract_depth": {"type": "string", "enum": ["basic", "advanced"], "default": "basic", "description": "Crawl depth"},
            },
            required=["api_key", "url"]
        )

    def run_tool(self, args: dict):
        api_key = args.get("api_key")
        client = OmnisearchClient(api_key)
        url = args.get("url", "")
        extract_depth = args.get("extract_depth", "basic")
        result = client.firecrawl_crawl(url, extract_depth)
        return [TextContent(type="text", text=result.get("result", str(result)))]

class FirecrawlExtractToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("firecrawl_extract")

    def get_tool_description(self) -> Tool:
        return Tool(
            name="firecrawl_extract",
            description="Structured data extraction with AI using natural language prompts via Firecrawl. Extracts specific information from web pages based on custom extraction instructions. Best for targeted data collection, information extraction, and converting unstructured web content into structured data.",
            inputSchema={
                "api_key": {"type": "string", "description": "Firecrawl API key (required)"},
                "url": {"type": "string", "description": "URL to extract from"},
                "extract_depth": {"type": "string", "enum": ["basic", "advanced"], "default": "basic", "description": "Extraction depth"},
            },
            required=["api_key", "url"]
        )

    def run_tool(self, args: dict):
        api_key = args.get("api_key")
        client = OmnisearchClient(api_key)
        url = args.get("url", "")
        extract_depth = args.get("extract_depth", "basic")
        result = client.firecrawl_extract(url, extract_depth)
        return [TextContent(type="text", text=result.get("result", str(result)))]

class FirecrawlScrapeToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("firecrawl_scrape")

    def get_tool_description(self) -> Tool:
        return Tool(
            name="firecrawl_scrape",
            description="Extract clean, LLM-ready data from single URLs with enhanced formatting options using Firecrawl. Efficiently converts web content into markdown, plain text, or structured data with configurable extraction options. Best for content analysis, data collection, and AI training data preparation.",
            inputSchema={
                "api_key": {"type": "string", "description": "Firecrawl API key (required)"},
                "url": {"type": "string", "description": "URL to scrape"},
                "extract_depth": {"type": "string", "enum": ["basic", "advanced"], "default": "basic", "description": "Scrape depth"},
            },
            required=["api_key", "url"]
        )

    def run_tool(self, args: dict):
        api_key = args.get("api_key")
        client = OmnisearchClient(api_key)
        url = args.get("url", "")
        extract_depth = args.get("extract_depth", "basic")
        result = client.firecrawl_scrape(url, extract_depth)
        return [TextContent(type="text", text=result.get("result", str(result)))]

class TavilyExtractToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("tavily_extract")

    def get_tool_description(self) -> Tool:
        return Tool(
            name="tavily_extract",
            description="Extract structured data from a web page using Tavily Extract. Best for extracting factual, structured information from technical, scientific, and academic sources.",
            inputSchema={
                "api_key": {"type": "string", "description": "Tavily API key (required)"},
                "url": {"type": "string", "description": "URL to extract from"},
                "extract_depth": {"type": "string", "enum": ["basic", "advanced"], "default": "basic", "description": "Extraction depth"},
            },
            required=["api_key", "url"]
        )

    def run_tool(self, args: dict):
        api_key = args.get("api_key")
        client = OmnisearchClient(api_key)
        url = args.get("url", "")
        extract_depth = args.get("extract_depth", "basic")
        result = client.tavily_extract(url, extract_depth)
        return [TextContent(type="text", text=result.get("result", str(result)))] 

class FirecrawlMapToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("firecrawl_map")

    def get_tool_description(self) -> Tool:
        return Tool(
            name="firecrawl_map",
            description="Fast URL collection from websites for comprehensive site mapping using Firecrawl. Efficiently discovers all accessible URLs within a domain without extracting content. Best for site auditing, URL discovery, and preparing for targeted content extraction.",
            inputSchema={
                "api_key": {"type": "string", "description": "Firecrawl API key (required)"},
                "url": {"type": "string", "description": "URL to map"},
                "extract_depth": {"type": "string", "enum": ["basic", "advanced"], "default": "basic", "description": "Mapping depth"},
            },
            required=["api_key", "url"]
        )

    def run_tool(self, args: dict):
        api_key = args.get("api_key")
        client = OmnisearchClient(api_key)
        url = args.get("url", "")
        extract_depth = args.get("extract_depth", "basic")
        result = client.firecrawl_map(url, extract_depth)
        return [TextContent(type="text", text=result.get("result", str(result)))]

class JinaReaderToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("jina_reader")

    def get_tool_description(self) -> Tool:
        return Tool(
            name="jina_reader",
            description="Convert any URL to clean, LLM-friendly text using Jina Reader API.",
            inputSchema={
                "api_key": {"type": "string", "description": "Jina API key (required)"},
                "url": {"type": "string", "description": "URL to read"},
            },
            required=["api_key", "url"]
        )

    def run_tool(self, args: dict):
        api_key = args.get("api_key")
        client = OmnisearchClient(api_key)
        url = args.get("url", "")
        result = client.jina_reader(url)
        return [TextContent(type="text", text=result.get("result", str(result)))]