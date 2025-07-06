# MCP-OMNISEARCH JSON Examples

Below are example POST requests for each tool supported by MCP-OMNISEARCH. Replace API keys and arguments with your actual values.

---

## Brave Search
```json
{
  "selected_server_credentials": {
    "MCP-OMNISEARCH": {
      "BRAVE_API_KEY": "your_brave_api_key_here"
    }
  },
  "client_details": {
    "tool_name": "brave",
    "arguments": {
      "api_key": "your_brave_api_key_here",
      "query": "python async tutorial",
      "limit": 5,
      "include_domains": ["realpython.com", "docs.python.org"],
      "exclude_domains": ["reddit.com"]
    }
  },
  "selected_client": "MCP_CLIENT_OMNISEARCH",
  "selected_servers": ["MCP-OMNISEARCH"]
}
```

---

## Tavily Search
```json
{
  "selected_server_credentials": {
    "MCP-OMNISEARCH": {
      "TAVILY_API_KEY": "your_tavily_api_key_here"
    }
  },
  "client_details": {
    "tool_name": "tavily",
    "arguments": {
      "api_key": "your_tavily_api_key_here",
      "query": "latest AI research papers",
      "limit": 5,
      "include_domains": ["arxiv.org", "nature.com"],
      "exclude_domains": ["wikipedia.org"]
    }
  },
  "selected_client": "MCP_CLIENT_OMNISEARCH",
  "selected_servers": ["MCP-OMNISEARCH"]
}
```

---

## Jina Reader
```json
{
  "selected_server_credentials": {
    "MCP-OMNISEARCH": {
      "JINA_API_KEY": "your_jina_api_key_here"
    }
  },
  "client_details": {
    "tool_name": "jina_reader",
    "arguments": {
      "api_key": "your_jina_api_key_here",
      "url": "https://example.com"
    }
  },
  "selected_client": "MCP_CLIENT_OMNISEARCH",
  "selected_servers": ["MCP-OMNISEARCH"]
}
```

---

## Jina Grounding
```json
{
  "selected_server_credentials": {
    "MCP-OMNISEARCH": {
      "JINA_API_KEY": "your_jina_api_key_here"
    }
  },
  "client_details": {
    "tool_name": "jina_grounding",
    "arguments": {
      "api_key": "your_jina_api_key_here",
      "content": "The James Webb Space Telescope is the most powerful space telescope ever built."
    }
  },
  "selected_client": "MCP_CLIENT_OMNISEARCH",
  "selected_servers": ["MCP-OMNISEARCH"]
}
```

---

## Firecrawl Actions
```json
{
  "selected_server_credentials": {
    "MCP-OMNISEARCH": {
      "FIRECRAWL_API_KEY": "your_firecrawl_api_key_here"
    }
  },
  "client_details": {
    "tool_name": "firecrawl_actions",
    "arguments": {
      "api_key": "your_firecrawl_api_key_here",
      "url": "https://example.com",
      "extract_depth": "advanced"
    }
  },
  "selected_client": "MCP_CLIENT_OMNISEARCH",
  "selected_servers": ["MCP-OMNISEARCH"]
}
```

---

## Firecrawl Crawl
```json
{
  "selected_server_credentials": {
    "MCP-OMNISEARCH": {
      "FIRECRAWL_API_KEY": "your_firecrawl_api_key_here"
    }
  },
  "client_details": {
    "tool_name": "firecrawl_crawl",
    "arguments": {
      "api_key": "your_firecrawl_api_key_here",
      "url": "https://docs.crewai.com/",
      "extract_depth": "basic"
    }
  },
  "selected_client": "MCP_CLIENT_OMNISEARCH",
  "selected_servers": ["MCP-OMNISEARCH"]
}
```

---

## Firecrawl Extract
```json
{
  "selected_server_credentials": {
    "MCP-OMNISEARCH": {
      "FIRECRAWL_API_KEY": "your_firecrawl_api_key_here"
    }
  },
  "client_details": {
    "tool_name": "firecrawl_extract",
    "arguments": {
      "api_key": "your_firecrawl_api_key_here",
      "url": "https://example.com",
      "extract_depth": "basic"
    }
  },
  "selected_client": "MCP_CLIENT_OMNISEARCH",
  "selected_servers": ["MCP-OMNISEARCH"]
}
```

---

## Firecrawl Scrape
```json
{
  "selected_server_credentials": {
    "MCP-OMNISEARCH": {
      "FIRECRAWL_API_KEY": "your_firecrawl_api_key_here"
    }
  },
  "client_details": {
    "tool_name": "firecrawl_scrape",
    "arguments": {
      "api_key": "your_firecrawl_api_key_here",
      "url": "https://example.com",
      "extract_depth": "basic"
    }
  },
  "selected_client": "MCP_CLIENT_OMNISEARCH",
  "selected_servers": ["MCP-OMNISEARCH"]
}
```

---

## Perplexity
```json
{
  "selected_server_credentials": {
    "MCP-OMNISEARCH": {
      "PERPLEXITY_API_KEY": "your_perplexity_api_key_here"
    }
  },
  "client_details": {
    "tool_name": "perplexity",
    "arguments": {
      "api_key": "your_perplexity_api_key_here",
      "query": "What are the latest breakthroughs in quantum computing?",
      "limit": 3
    }
  },
  "selected_client": "MCP_CLIENT_OMNISEARCH",
  "selected_servers": ["MCP-OMNISEARCH"]
}
``` 