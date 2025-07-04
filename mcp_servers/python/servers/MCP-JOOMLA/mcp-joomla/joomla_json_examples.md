# Joomla MCP Client JSON Request Examples

## Basic Structure

All Joomla MCP requests follow this pattern:

```json
{
  "selected_server_credentials": {
    "MCP-JOOMLA": {
      "base_url": "https://your-joomla-site.com",
      "bearer_token": "your-joomla-bearer-token"
    }
  },
  "client_details": {
    "tool_name": "tool_name_here",
    "arguments": {
      // Tool-specific arguments
    }
  },
  "selected_client": "MCP_CLIENT_JOOMLA",
  "selected_servers": [
    "MCP-JOOMLA"
  ]
}
```

## 1. Get Joomla Articles

```json
{
  "selected_server_credentials": {
    "MCP-JOOMLA": {
      "base_url": "https://your-joomla-site.com",
      "bearer_token": "your-joomla-bearer-token"
    }
  },
  "client_details": {
    "tool_name": "get_joomla_articles",
    "arguments": {
      "base_url": "https://your-joomla-site.com",
      "bearer_token": "your-joomla-bearer-token"
    }
  },
  "selected_client": "MCP_CLIENT_JOOMLA",
  "selected_servers": [
    "MCP-JOOMLA"
  ]
}
```

## 2. Get Joomla Categories

```json
{
  "selected_server_credentials": {
    "MCP-JOOMLA": {
      "base_url": "https://your-joomla-site.com",
      "bearer_token": "your-joomla-bearer-token"
    }
  },
  "client_details": {
    "tool_name": "get_joomla_categories",
    "arguments": {
      "base_url": "https://your-joomla-site.com",
      "bearer_token": "your-joomla-bearer-token"
    }
  },
  "selected_client": "MCP_CLIENT_JOOMLA",
  "selected_servers": [
    "MCP-JOOMLA"
  ]
}
```

## 3. Create Article

```json
{
  "selected_server_credentials": {
    "MCP-JOOMLA": {
      "base_url": "https://your-joomla-site.com",
      "bearer_token": "your-joomla-bearer-token"
    }
  },
  "client_details": {
    "tool_name": "create_article",
    "arguments": {
      "base_url": "https://your-joomla-site.com",
      "bearer_token": "your-joomla-bearer-token",
      "article_text": "This is the content of my new article. It can be plain text or HTML.",
      "title": "My New Article",
      "category_id": 2,
      "convert_plain_text": true,
      "published": true
    }
  },
  "selected_client": "MCP_CLIENT_JOOMLA",
  "selected_servers": [
    "MCP-JOOMLA"
  ]
}
```

## 4. Update Article

```json
{
  "selected_server_credentials": {
    "MCP-JOOMLA": {
      "base_url": "https://your-joomla-site.com",
      "bearer_token": "your-joomla-bearer-token"
    }
  },
  "client_details": {
    "tool_name": "update_article",
    "arguments": {
      "base_url": "https://your-joomla-site.com",
      "bearer_token": "your-joomla-bearer-token",
      "article_id": 123,
      "title": "Updated Article Title",
      "fulltext": "This is the updated content of the article.",
      "metadesc": "Updated meta description for SEO",
      "convert_plain_text": true
    }
  },
  "selected_client": "MCP_CLIENT_JOOMLA",
  "selected_servers": [
    "MCP-JOOMLA"
  ]
}
```

## 5. Manage Article State

```json
{
  "selected_server_credentials": {
    "MCP-JOOMLA": {
      "base_url": "https://your-joomla-site.com",
      "bearer_token": "your-joomla-bearer-token"
    }
  },
  "client_details": {
    "tool_name": "manage_article_state",
    "arguments": {
      "base_url": "https://your-joomla-site.com",
      "bearer_token": "your-joomla-bearer-token",
      "article_id": 123,
      "target_state": 1
    }
  },
  "selected_client": "MCP_CLIENT_JOOMLA",
  "selected_servers": [
    "MCP-JOOMLA"
  ]
}
```

**State Values:**
- `1`: Published
- `0`: Unpublished  
- `2`: Archived
- `-2`: Trashed

## 6. Move Article to Trash

```json
{
  "selected_server_credentials": {
    "MCP-JOOMLA": {
      "base_url": "https://your-joomla-site.com",
      "bearer_token": "your-joomla-bearer-token"
    }
  },
  "client_details": {
    "tool_name": "move_article_to_trash",
    "arguments": {
      "base_url": "https://your-joomla-site.com",
      "bearer_token": "your-joomla-bearer-token",
      "article_id": 123,
      "expected_title": "Article Title to Verify"
    }
  },
  "selected_client": "MCP_CLIENT_JOOMLA",
  "selected_servers": [
    "MCP-JOOMLA"
  ]
}
```

## Complete Workflow Example

### Step 1: Get Categories
```json
{
  "selected_server_credentials": {
    "MCP-JOOMLA": {
      "base_url": "https://myjoomla.com",
      "bearer_token": "abc123def456"
    }
  },
  "client_details": {
    "tool_name": "get_joomla_categories",
    "arguments": {
      "base_url": "https://myjoomla.com",
      "bearer_token": "abc123def456"
    }
  },
  "selected_client": "MCP_CLIENT_JOOMLA",
  "selected_servers": [
    "MCP-JOOMLA"
  ]
}
```

### Step 2: Create Article
```json
{
  "selected_server_credentials": {
    "MCP-JOOMLA": {
      "base_url": "https://myjoomla.com",
      "bearer_token": "abc123def456"
    }
  },
  "client_details": {
    "tool_name": "create_article",
    "arguments": {
      "base_url": "https://myjoomla.com",
      "bearer_token": "abc123def456",
      "article_text": "Welcome to our new blog! This is our first post.",
      "title": "Welcome to Our Blog",
      "category_id": 1,
      "published": true
    }
  },
  "selected_client": "MCP_CLIENT_JOOMLA",
  "selected_servers": [
    "MCP-JOOMLA"
  ]
}
```

### Step 3: Update Article
```json
{
  "selected_server_credentials": {
    "MCP-JOOMLA": {
      "base_url": "https://myjoomla.com",
      "bearer_token": "abc123def456"
    }
  },
  "client_details": {
    "tool_name": "update_article",
    "arguments": {
      "base_url": "https://myjoomla.com",
      "bearer_token": "abc123def456",
      "article_id": 456,
      "title": "Updated Welcome to Our Blog",
      "fulltext": "Welcome to our new blog! This is our first post with updated content.",
      "metadesc": "Welcome post for our new blog"
    }
  },
  "selected_client": "MCP_CLIENT_JOOMLA",
  "selected_servers": [
    "MCP-JOOMLA"
  ]
}
```

## Notes

- Replace `"https://your-joomla-site.com"` with your actual Joomla site URL
- Replace `"your-joomla-bearer-token"` with your actual Joomla API bearer token
- The `article_id` should be a valid integer from your Joomla site
- The `category_id` should be a valid category ID from your Joomla site
- All requests require both `base_url` and `bearer_token` in the arguments 