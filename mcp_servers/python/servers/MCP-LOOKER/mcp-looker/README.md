# MCP-LOOKER Server

A Model Context Protocol (MCP) server for Looker data analytics platform. Provides tools for querying data, managing dashboards, looks, and exploring data models.

## Features

- **Dynamic Credential Management**: Credentials are passed with each request instead of environment variables
- **Modular Architecture**: Separate tool handlers for different functionalities
- **Dashboard Management**: Retrieve and explore dashboards
- **Query Execution**: Run Looker queries with full parameter support
- **Data Model Exploration**: Discover models and explores
- **Look Management**: Create and retrieve looks
- **Formatted Results**: Query results are formatted as readable tables

## Architecture

The server follows a modular pattern similar to other MCP servers:

```
src/mcp_looker/
├── toolhandler.py          # Base ToolHandler class
├── looker_client.py        # Looker API client with credential management
├── tools_dashboards.py     # Dashboard-related tools
├── tools_queries.py        # Query and model-related tools
├── tools_looks.py          # Look-related tools
└── server.py              # Main server with tool registration
```

## Tools

### 1. Get Looker Dashboards
Retrieve all dashboards from the Looker instance.

**JSON Request:**
```json
{
  "name": "get_looker_dashboards",
  "arguments": {
    "base_url": "https://your-company.looker.com",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret"
  }
}
```

### 2. Get Dashboard Details
Get detailed information about a specific dashboard.

**JSON Request:**
```json
{
  "name": "get_dashboard_details",
  "arguments": {
    "base_url": "https://your-company.looker.com",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "dashboard_id": "123"
  }
}
```

### 3. Run Looker Query
Execute a Looker query and return formatted results.

**JSON Request:**
```json
{
  "name": "run_looker_query",
  "arguments": {
    "base_url": "https://your-company.looker.com",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "model": "my_model",
    "explore": "my_explore",
    "fields": ["table.field1", "table.field2"],
    "filters": {"table.field1": "value"},
    "sorts": ["field1 desc"],
    "limit": 1000
  }
}
```

### 4. Get Looker Models
Retrieve all available data models.

**JSON Request:**
```json
{
  "name": "get_looker_models",
  "arguments": {
    "base_url": "https://your-company.looker.com",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret"
  }
}
```

### 5. Get Looker Explores
Get explores for a specific model.

**JSON Request:**
```json
{
  "name": "get_looker_explores",
  "arguments": {
    "base_url": "https://your-company.looker.com",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "model_name": "my_model"
  }
}
```

### 6. Get Looker Looks
Retrieve all looks from the Looker instance.

**JSON Request:**
```json
{
  "name": "get_looker_looks",
  "arguments": {
    "base_url": "https://your-company.looker.com",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret"
  }
}
```

### 7. Create Looker Look
Create a new look with specified query parameters.

**JSON Request:**
```json
{
  "name": "create_looker_look",
  "arguments": {
    "base_url": "https://your-company.looker.com",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "title": "My New Look",
    "description": "Description of the look",
    "model": "my_model",
    "explore": "my_explore",
    "fields": ["table.field1", "table.field2"],
    "filters": {"table.field1": "value"},
    "sorts": ["field1 desc"],
    "limit": 1000
  }
}
```

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Looker API Setup:**
   - Ensure your Looker instance has API access enabled
   - Generate API credentials (client_id and client_secret)
   - Note your Looker instance URL

3. **Run the Server:**
   ```bash
   python -m src.mcp_looker.server
   ```

## Credential Management

Unlike environment variable-based authentication, this server requires credentials to be passed with each request:

- `base_url`: Your Looker instance URL (e.g., "https://your-company.looker.com")
- `client_id`: Your Looker API client ID
- `client_secret`: Your Looker API client secret

This approach provides:
- **Flexibility**: Use different credentials for different operations
- **Security**: No need to store credentials in environment variables
- **Multi-tenant Support**: Work with multiple Looker instances from the same server

## Query Structure

Looker queries follow this structure:
```json
{
  "model": "model_name",
  "view": "explore_name",
  "fields": ["table.field1", "table.field2"],
  "filters": {"table.field1": "value"},
  "sorts": ["field1 desc", "field2 asc"],
  "limit": 1000
}
```

## Example Workflow

1. **Get Models:**
   ```json
   {
     "name": "get_looker_models",
     "arguments": {
       "base_url": "https://mycompany.looker.com",
       "client_id": "abc123",
       "client_secret": "def456"
     }
   }
   ```

2. **Get Explores for a Model:**
   ```json
   {
     "name": "get_looker_explores",
     "arguments": {
       "base_url": "https://mycompany.looker.com",
       "client_id": "abc123",
       "client_secret": "def456",
       "model_name": "sales_model"
     }
   }
   ```

3. **Run a Query:**
   ```json
   {
     "name": "run_looker_query",
     "arguments": {
       "base_url": "https://mycompany.looker.com",
       "client_id": "abc123",
       "client_secret": "def456",
       "model": "sales_model",
       "explore": "orders",
       "fields": ["orders.order_date", "orders.total_amount"],
       "filters": {"orders.status": "completed"},
       "sorts": ["orders.order_date desc"],
       "limit": 100
     }
   }
   ```

## Error Handling

The server provides comprehensive error handling:
- Invalid credentials
- Network connectivity issues
- Invalid model/explore names
- Query syntax errors
- Permission errors

All errors are returned as human-readable messages in the response.

## Security Notes

- Client secrets should be kept secure and not shared
- All API requests use HTTPS
- Access tokens are managed automatically by the client
- Credentials are not stored between requests

## Troubleshooting

**Common Issues:**
1. **401 Unauthorized**: Check your client_id and client_secret
2. **404 Not Found**: Verify the base_url and API endpoint
3. **403 Forbidden**: Ensure your credentials have the required permissions
4. **Invalid Model**: Use `get_looker_models` to find valid model names
5. **Invalid Explore**: Use `get_looker_explores` to find valid explore names

**Debug Mode:**
Enable logging by setting the appropriate log level in your MCP client configuration.
