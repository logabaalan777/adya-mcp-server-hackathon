# MCP-OMNISEARCH Server Features

MCP-OMNISEARCH provides unified access to multiple search and enrichment APIs. Below are the supported tools and their features.

## Supported Tools

### 1. Brave Search (`brave`)
- **Description:** Privacy-focused search engine with technical coverage and search operators.
- **Arguments:**
  - `api_key` (string, required)
  - `query` (string, required)
  - `limit` (integer, optional)
  - `include_domains` (array of strings, optional)
  - `exclude_domains` (array of strings, optional)
- **Example:**
```json
{
  "tool_name": "brave",
  "arguments": {
    "api_key": "...",
    "query": "python async tutorial"
  }
}
```

### 2. Tavily Search (`tavily`)
- **Description:** Web search with factual results and domain filtering.
- **Arguments:**
  - `api_key` (string, required)
  - `query` (string, required)
  - `limit` (integer, optional)
  - `include_domains` (array of strings, optional)
  - `exclude_domains` (array of strings, optional)
- **Example:**
```json
{
  "tool_name": "tavily",
  "arguments": {
    "api_key": "...",
    "query": "latest AI research papers"
  }
}
```

### 3. Jina Reader (`jina_reader`)
- **Description:** Converts any URL to clean, LLM-friendly text using Jina Reader API.
- **Arguments:**
  - `api_key` (string, required)
  - `url` (string, required)
- **Example:**
```json
{
  "tool_name": "jina_reader",
  "arguments": {
    "api_key": "...",
    "url": "https://example.com"
  }
}
```

### 4. Jina Grounding (`jina_grounding`)
- **Description:** Content enrichment and grounding using Jina AI.
- **Arguments:**
  - `api_key` (string, required)
  - `content` (string, required)
- **Example:**
```json
{
  "tool_name": "jina_grounding",
  "arguments": {
    "api_key": "...",
    "content": "The James Webb Space Telescope is the most powerful..."
  }
}
```

### 5. Firecrawl Actions (`firecrawl_actions`)
- **Description:** Page interactions and extraction for dynamic content.
- **Arguments:**
  - `api_key` (string, required)
  - `url` (string, required)
  - `extract_depth` (string, optional: "basic" or "advanced")
- **Example:**
```json
{
  "tool_name": "firecrawl_actions",
  "arguments": {
    "api_key": "...",
    "url": "https://example.com",
    "extract_depth": "advanced"
  }
}
```

### 6. Firecrawl Crawl (`firecrawl_crawl`)
- **Description:** Multi-page crawl and extraction.
- **Arguments:**
  - `api_key` (string, required)
  - `url` (string, required)
  - `extract_depth` (string, optional)
- **Example:**
```json
{
  "tool_name": "firecrawl_crawl",
  "arguments": {
    "api_key": "...",
    "url": "https://docs.crewai.com/"
  }
}
```

### 7. Firecrawl Extract (`firecrawl_extract`)
- **Description:** Extracts main content, title, and author from a page.
- **Arguments:**
  - `api_key` (string, required)
  - `url` (string, required)
  - `extract_depth` (string, optional)
- **Example:**
```json
{
  "tool_name": "firecrawl_extract",
  "arguments": {
    "api_key": "...",
    "url": "https://example.com"
  }
}
```

### 8. Firecrawl Scrape (`firecrawl_scrape`)
- **Description:** Scrapes a single page for content.
- **Arguments:**
  - `api_key` (string, required)
  - `url` (string, required)
  - `extract_depth` (string, optional)
- **Example:**
```json
{
  "tool_name": "firecrawl_scrape",
  "arguments": {
    "api_key": "...",
    "url": "https://example.com"
  }
}
```

### 9. Perplexity (`perplexity`)
- **Description:** AI-powered response generation with real-time web search.
- **Arguments:**
  - `api_key` (string, required)
  - `query` (string, required)
  - `limit` (integer, optional)
- **Example:**
```json
{
  "tool_name": "perplexity",
  "arguments": {
    "api_key": "...",
    "query": "What are the latest breakthroughs in quantum computing?"
  }
}
``` 