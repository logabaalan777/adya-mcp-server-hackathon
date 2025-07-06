import requests

# Endpoints
TAVILY_BASE_URL = "https://api.tavily.com"
BRAVE_BASE_URL = "https://api.search.brave.com/res/v1"
PERPLEXITY_BASE_URL = "https://api.perplexity.ai"
JINA_GROUNDING_URL = "https://g.jina.ai"
JINA_READER_URL = "https://r.jina.ai/"
FIRECRAWL_SCRAPE_URL = "https://api.firecrawl.dev/v1/scrape"
FIRECRAWL_CRAWL_URL = "https://api.firecrawl.dev/v1/crawl"
FIRECRAWL_EXTRACT_URL = "https://api.firecrawl.dev/v1/extract"
FIRECRAWL_MAP_URL = "https://api.firecrawl.dev/v1/map"

class OmnisearchClient:
    def __init__(self, api_key):
        self.api_key = api_key

    # --- SEARCH PROVIDERS ---
    def search_brave(self, query, limit=3, include_domains=None, exclude_domains=None):
        url = f"{BRAVE_BASE_URL}/web/search"
        params = {
            "q": query,
            "count": limit
        }
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results = []
        web = data.get("web", {})
        # If 'web' is a list, iterate directly; if dict, get 'results'
        if isinstance(web, list):
            for r in web:
                results.append({
                    "title": r.get("title"),
                    "url": r.get("url"),
                    "snippet": r.get("description"),
                    "source_provider": "brave"
                })
        elif isinstance(web, dict):
            for r in web.get("results", []):
                results.append({
                    "title": r.get("title"),
                    "url": r.get("url"),
                    "snippet": r.get("description"),
                    "source_provider": "brave"
                })
        return results

    def search_tavily(self, query, limit=3, include_domains=None, exclude_domains=None):
        url = f"{TAVILY_BASE_URL}/search"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "query": query,
            "max_results": limit,
            "include_domains": include_domains or [],
            "exclude_domains": exclude_domains or [],
            "search_depth": "basic",
            "topic": "general"
        }
        resp = requests.post(url, json=body, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for r in data.get("results", []):
            results.append({
                "title": r.get("title"),
                "url": r.get("url"),
                "snippet": r.get("content"),
                "score": r.get("score"),
                "source_provider": "tavily"
            })
        return results

    # --- AI RESPONSE PROVIDER ---
    def search_perplexity(self, query, limit=2):
        url = f"{PERPLEXITY_BASE_URL}/chat/completions"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        body = {
            "model": "sonar-pro",
            "messages": [{"role": "user", "content": query}],
            "temperature": 0.2,
            "max_tokens": 1024
        }
        resp = requests.post(url, json=body, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        results = [{
            "title": "Perplexity AI",
            "url": "https://perplexity.ai",
            "snippet": answer,
            "source_provider": "perplexity"
        }]
        return results
        
    # --- FIRECRAWL PROVIDERS ---
    def firecrawl_actions(self, url, extract_depth="basic"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "url": url,
            "formats": ["markdown", "screenshot"],
            "actions": [
                {"type": "wait", "milliseconds": 2000},
                {"type": "scroll", "duration": 1000}
            ]
        }
        resp = requests.post(FIRECRAWL_SCRAPE_URL, json=body, headers=headers, timeout=90)
        resp.raise_for_status()
        data = resp.json()
        return data

    def firecrawl_crawl(self, url, extract_depth="basic"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "url": url,
            "scrapeOptions": {"formats": ["markdown"], "onlyMainContent": True},
            "maxDepth": 3 if extract_depth == "advanced" else 1,
            "limit": 50 if extract_depth == "advanced" else 20
        }
        resp = requests.post(FIRECRAWL_CRAWL_URL, json=body, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data


    def firecrawl_extract(self, url, extract_depth="basic"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "urls": [url],
            "prompt": "Extract the main content, title, and author from this page. Summarize the key information." if extract_depth == "basic" else "Extract all relevant information from this page including: title, author, date published, main content, categories or tags, related links, and any structured data like product information, pricing, or specifications. Format the data in a well-structured way.",
            "showSources": True,
            "scrapeOptions": {"formats": ["markdown"], "onlyMainContent": True, "waitFor": 2000 if extract_depth == "basic" else 5000}
        }
        resp = requests.post(FIRECRAWL_EXTRACT_URL, json=body, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data

    def firecrawl_scrape(self, url, extract_depth="basic"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "url": url,
            "formats": ["markdown"],
            "onlyMainContent": True,
            "waitFor": 2000 if extract_depth == "basic" else 5000
        }
        resp = requests.post(FIRECRAWL_SCRAPE_URL, json=body, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data

    # --- TAVILY EXTRACT ---
    def tavily_extract(self, url, extract_depth="basic"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "query": url,
            "max_results": 1,
            "search_depth": extract_depth
        }
        resp = requests.post(f"{TAVILY_BASE_URL}/search", json=body, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data

    # --- JINA GROUNDING ---
    def jina_grounding(self, content):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "statement": content
        }
        resp = requests.post(JINA_GROUNDING_URL, json=body, headers=headers, timeout=90)
        resp.raise_for_status()
        data = resp.json()
        return data

    # --- FIRECRAWL MAP ---
    def firecrawl_map(self, url, extract_depth="basic"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "url": url,
            "limit": 200 if extract_depth == "advanced" else 50,
            "ignoreSitemap": False,
            "includeSubdomains": False
        }
        resp = requests.post(FIRECRAWL_MAP_URL, json=body, headers=headers, timeout=90)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("success") or data.get("error"):
            raise Exception(f"Error mapping website: {data.get('error', 'Unknown error')}")
        links = data.get("links", [])
        if not links:
            raise Exception("No URLs discovered during mapping")
        formatted_content = f"# Site Map for {url}\n\nFound {len(links)} URLs:\n\n" + "\n".join(f"- {u}" for u in links)
        return {
            "content": formatted_content,
            "links": links,
            "metadata": {
                "title": f"Site Map for {url}",
                "word_count": len(links),
                "urls_processed": 1,
                "successful_extractions": 1,
                "extract_depth": extract_depth
            }
        }

    # --- JINA READER ---
    def jina_reader(self, url):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        body = {"url": url}
        resp = requests.post(JINA_READER_URL, json=body, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("data"):
            raise Exception("Invalid response format from Jina Reader")
        return {
            "content": data["data"].get("content", ""),
            "metadata": {
                "title": data["data"].get("title", ""),
                "date": data["data"].get("timestamp", ""),
                "word_count": len(data["data"].get("content", "").split()),
            }
        }
