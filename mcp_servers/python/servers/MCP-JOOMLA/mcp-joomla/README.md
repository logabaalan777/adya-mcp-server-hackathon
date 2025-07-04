# Joomla MCP Server

A Model Context Protocol (MCP) server for managing Joomla content management system articles and categories through a modular, credential-based architecture.

## Features

- **Dynamic Credential Management**: Credentials are passed with each request instead of environment variables
- **Modular Architecture**: Separate tool handlers for different functionalities
- **Article Management**: Create, read, update, and manage article states
- **Category Management**: Retrieve and work with Joomla categories
- **Safe Operations**: Trash articles instead of permanent deletion for recovery

## Architecture

The server follows a modular pattern similar to other MCP servers:

```
src/mcp_joomla/
├── toolhandler.py          # Base ToolHandler class
├── joomla_client.py        # Joomla API client with credential management
├── tools_articles.py       # Article-related tools (get, create)
├── tools_categories.py     # Category-related tools
├── tools_management.py     # Article management tools (update, state, trash)
└── server.py              # Main server with tool registration
```

## Tools

### 1. Get Joomla Articles
Retrieve all articles from the Joomla website.

**JSON Request:**
```json
{
  "name": "get_joomla_articles",
  "arguments": {
    "base_url": "https://your-joomla-site.com",
    "bearer_token": "your-bearer-token"
  }
}
```

### 2. Get Joomla Categories
Retrieve all categories from the Joomla website.

**JSON Request:**
```json
{
  "name": "get_joomla_categories",
  "arguments": {
    "base_url": "https://your-joomla-site.com",
    "bearer_token": "your-bearer-token"
  }
}
```

### 3. Create Article
Create a new article on the Joomla website.

**JSON Request:**
```json
{
  "name": "create_article",
  "arguments": {
    "base_url": "https://your-joomla-site.com",
    "bearer_token": "your-bearer-token",
    "article_text": "This is the content of my article. It can be plain text or HTML.",
    "title": "My Article Title",
    "category_id": 2,
    "convert_plain_text": true,
    "published": true
  }
}
```

### 4. Update Article
Update an existing article on the Joomla website.

**JSON Request:**
```json
{
  "name": "update_article",
  "arguments": {
    "base_url": "https://your-joomla-site.com",
    "bearer_token": "your-bearer-token",
    "article_id": 123,
    "title": "Updated Article Title",
    "fulltext": "Updated article content goes here.",
    "metadesc": "Updated meta description",
    "convert_plain_text": true
  }
}
```

### 5. Manage Article State
Change the publication state of an article.

**JSON Request:**
```json
{
  "name": "manage_article_state",
  "arguments": {
    "base_url": "https://your-joomla-site.com",
    "bearer_token": "your-bearer-token",
    "article_id": 123,
    "target_state": 1
  }
}
```

**State Values:**
- `1`: Published
- `0`: Unpublished
- `2`: Archived
- `-2`: Trashed

### 6. Move Article to Trash
Safely delete an article by moving it to trash (recoverable).

**JSON Request:**
```json
{
  "name": "move_article_to_trash",
  "arguments": {
    "base_url": "https://your-joomla-site.com",
    "bearer_token": "your-bearer-token",
    "article_id": 123,
    "expected_title": "Article Title"
  }
}
```

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Joomla API Setup:**
   - Ensure your Joomla site has the API enabled
   - Generate a bearer token with appropriate permissions
   - Note your Joomla site's base URL

3. **Run the Server:**
   ```bash
   python -m src.mcp_joomla.server
   ```

## Credential Management

Unlike the previous version that used environment variables, this server requires credentials to be passed with each request:

- `base_url`: Your Joomla website URL (e.g., "https://example.com")
- `bearer_token`: Your Joomla API bearer token

This approach provides:
- **Flexibility**: Use different credentials for different operations
- **Security**: No need to store credentials in environment variables
- **Multi-tenant Support**: Work with multiple Joomla sites from the same server

## Error Handling

The server provides comprehensive error handling:
- Invalid credentials
- Network connectivity issues
- Invalid article/category IDs
- Permission errors
- JSON parsing errors

All errors are returned as human-readable messages in the response.

## Content Processing

The server automatically handles:
- **Text to HTML Conversion**: Converts plain text to sanitized HTML using Markdown
- **Alias Generation**: Creates URL-friendly aliases from article titles
- **Content Sanitization**: Removes potentially harmful HTML tags
- **Meta Description**: Handles SEO meta descriptions

## Example Workflow

1. **Get Categories:**
   ```json
   {
     "name": "get_joomla_categories",
     "arguments": {
       "base_url": "https://myjoomla.com",
       "bearer_token": "abc123..."
     }
   }
   ```

2. **Create Article:**
   ```json
   {
     "name": "create_article",
     "arguments": {
       "base_url": "https://myjoomla.com",
       "bearer_token": "abc123...",
       "article_text": "Welcome to our new blog post!",
       "title": "Welcome Post",
       "category_id": 1,
       "published": true
     }
   }
   ```

3. **Update Article:**
   ```json
   {
     "name": "update_article",
     "arguments": {
       "base_url": "https://myjoomla.com",
       "bearer_token": "abc123...",
       "article_id": 456,
       "title": "Updated Welcome Post",
       "fulltext": "Updated content with more information."
     }
   }
   ```

## Security Notes

- Bearer tokens should be kept secure and not shared
- The server sanitizes HTML content to prevent XSS attacks
- Articles are moved to trash instead of permanent deletion
- All API requests use HTTPS when available

## Troubleshooting

**Common Issues:**
1. **401 Unauthorized**: Check your bearer token
2. **404 Not Found**: Verify the base URL and API endpoint
3. **403 Forbidden**: Ensure your token has the required permissions
4. **Invalid Category ID**: Use `get_joomla_categories` to find valid IDs

**Debug Mode:**
Enable logging by setting the appropriate log level in your MCP client configuration.

