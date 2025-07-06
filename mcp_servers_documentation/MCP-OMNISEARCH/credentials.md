# MCP-OMNISEARCH Credentials

This server requires API keys for various search and enrichment providers. You must obtain and set these credentials to use the corresponding tools.

## Required API Keys

- **Brave API Key**
  - Get from: https://search.brave.com/api
  - Set as: `BRAVE_API_KEY`

- **Tavily API Key**
  - Get from: https://app.tavily.com/
  - Set as: `TAVILY_API_KEY`

- **Jina API Key**
  - Get from: https://jina.ai/reader
  - Set as: `JINA_API_KEY`

- **Firecrawl API Key**
  - Get from: https://firecrawl.dev/
  - Set as: `FIRECRAWL_API_KEY`

- **Perplexity API Key**
  - Get from: https://platform.perplexity.ai/
  - Set as: `PERPLEXITY_API_KEY`

## How to Set Credentials

You can provide these keys in your POST requests under `selected_server_credentials`, or set them as environment variables for local development.

Example POST request snippet:
```json
{
  "selected_server_credentials": {
    "MCP-OMNISEARCH": {
      "BRAVE_API_KEY": "...",
      "TAVILY_API_KEY": "...",
      "JINA_API_KEY": "...",
      "FIRECRAWL_API_KEY": "...",
      "PERPLEXITY_API_KEY": "..."
    }
  }
}
``` 