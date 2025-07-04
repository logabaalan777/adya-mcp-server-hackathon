# Looker MCP Client JSON Request Examples

## Basic Structure

All Looker MCP requests follow this pattern:

```json
{
  "selected_server_credentials": {
    "MCP-LOOKER": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret"
    }
  },
  "client_details": {
    "tool_name": "tool_name_here",
    "arguments": {
      // Tool-specific arguments
    }
  },
  "selected_client": "MCP_CLIENT_LOOKER",
  "selected_servers": [
    "MCP-LOOKER"
  ]
}
```

## 1. Get Looker Dashboards

```json
{
  "selected_server_credentials": {
    "MCP-LOOKER": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret"
    }
  },
  "client_details": {
    "tool_name": "get_looker_dashboards",
    "arguments": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret"
    }
  },
  "selected_client": "MCP_CLIENT_LOOKER",
  "selected_servers": [
    "MCP-LOOKER"
  ]
}
```

## 2. Get Dashboard Details

```json
{
  "selected_server_credentials": {
    "MCP-LOOKER": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret"
    }
  },
  "client_details": {
    "tool_name": "get_dashboard_details",
    "arguments": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret",
      "dashboard_id": "123"
    }
  },
  "selected_client": "MCP_CLIENT_LOOKER",
  "selected_servers": [
    "MCP-LOOKER"
  ]
}
```

## 3. Get Looker Models

```json
{
  "selected_server_credentials": {
    "MCP-LOOKER": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret"
    }
  },
  "client_details": {
    "tool_name": "get_looker_models",
    "arguments": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret"
    }
  },
  "selected_client": "MCP_CLIENT_LOOKER",
  "selected_servers": [
    "MCP-LOOKER"
  ]
}
```

## 4. Get Looker Explores

```json
{
  "selected_server_credentials": {
    "MCP-LOOKER": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret"
    }
  },
  "client_details": {
    "tool_name": "get_looker_explores",
    "arguments": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret",
      "model_name": "sales_model"
    }
  },
  "selected_client": "MCP_CLIENT_LOOKER",
  "selected_servers": [
    "MCP-LOOKER"
  ]
}
```

## 5. Run Looker Query

```json
{
  "selected_server_credentials": {
    "MCP-LOOKER": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret"
    }
  },
  "client_details": {
    "tool_name": "run_looker_query",
    "arguments": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret",
      "model": "sales_model",
      "explore": "orders",
      "fields": ["orders.order_date", "orders.total_amount", "customers.customer_name"],
      "filters": {"orders.status": "completed"},
      "sorts": ["orders.order_date desc"],
      "limit": 100
    }
  },
  "selected_client": "MCP_CLIENT_LOOKER",
  "selected_servers": [
    "MCP-LOOKER"
  ]
}
```

## 6. Get Looker Looks

```json
{
  "selected_server_credentials": {
    "MCP-LOOKER": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret"
    }
  },
  "client_details": {
    "tool_name": "get_looker_looks",
    "arguments": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret"
    }
  },
  "selected_client": "MCP_CLIENT_LOOKER",
  "selected_servers": [
    "MCP-LOOKER"
  ]
}
```

## 7. Create Looker Look

```json
{
  "selected_server_credentials": {
    "MCP-LOOKER": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret"
    }
  },
  "client_details": {
    "tool_name": "create_looker_look",
    "arguments": {
      "base_url": "https://your-company.looker.com",
      "client_id": "your-client-id",
      "client_secret": "your-client-secret",
      "title": "Monthly Sales Report",
      "description": "Monthly sales data by region",
      "model": "sales_model",
      "explore": "orders",
      "fields": ["orders.order_date", "orders.total_amount", "customers.region"],
      "filters": {"orders.status": "completed"},
      "sorts": ["orders.order_date desc"],
      "limit": 1000
    }
  },
  "selected_client": "MCP_CLIENT_LOOKER",
  "selected_servers": [
    "MCP-LOOKER"
  ]
}
```

## Complete Workflow Example

### Step 1: Get Models
```json
{
  "selected_server_credentials": {
    "MCP-LOOKER": {
      "base_url": "https://mycompany.looker.com",
      "client_id": "abc123def456",
      "client_secret": "xyz789uvw012"
    }
  },
  "client_details": {
    "tool_name": "get_looker_models",
    "arguments": {
      "base_url": "https://mycompany.looker.com",
      "client_id": "abc123def456",
      "client_secret": "xyz789uvw012"
    }
  },
  "selected_client": "MCP_CLIENT_LOOKER",
  "selected_servers": [
    "MCP-LOOKER"
  ]
}
```

### Step 2: Get Explores for a Model
```json
{
  "selected_server_credentials": {
    "MCP-LOOKER": {
      "base_url": "https://mycompany.looker.com",
      "client_id": "abc123def456",
      "client_secret": "xyz789uvw012"
    }
  },
  "client_details": {
    "tool_name": "get_looker_explores",
    "arguments": {
      "base_url": "https://mycompany.looker.com",
      "client_id": "abc123def456",
      "client_secret": "xyz789uvw012",
      "model_name": "sales_model"
    }
  },
  "selected_client": "MCP_CLIENT_LOOKER",
  "selected_servers": [
    "MCP-LOOKER"
  ]
}
```

### Step 3: Run a Query
```json
{
  "selected_server_credentials": {
    "MCP-LOOKER": {
      "base_url": "https://mycompany.looker.com",
      "client_id": "abc123def456",
      "client_secret": "xyz789uvw012"
    }
  },
  "client_details": {
    "tool_name": "run_looker_query",
    "arguments": {
      "base_url": "https://mycompany.looker.com",
      "client_id": "abc123def456",
      "client_secret": "xyz789uvw012",
      "model": "sales_model",
      "explore": "orders",
      "fields": ["orders.order_date", "orders.total_amount", "customers.customer_name"],
      "filters": {"orders.status": "completed", "orders.order_date": "2024-01-01"},
      "sorts": ["orders.total_amount desc"],
      "limit": 50
    }
  },
  "selected_client": "MCP_CLIENT_LOOKER",
  "selected_servers": [
    "MCP-LOOKER"
  ]
}
```

### Step 4: Create a Look
```json
{
  "selected_server_credentials": {
    "MCP-LOOKER": {
      "base_url": "https://mycompany.looker.com",
      "client_id": "abc123def456",
      "client_secret": "xyz789uvw012"
    }
  },
  "client_details": {
    "tool_name": "create_looker_look",
    "arguments": {
      "base_url": "https://mycompany.looker.com",
      "client_id": "abc123def456",
      "client_secret": "xyz789uvw012",
      "title": "Top Customers by Revenue",
      "description": "Shows top customers ranked by total revenue",
      "model": "sales_model",
      "explore": "customers",
      "fields": ["customers.customer_name", "customers.total_revenue", "customers.order_count"],
      "filters": {"customers.status": "active"},
      "sorts": ["customers.total_revenue desc"],
      "limit": 100
    }
  },
  "selected_client": "MCP_CLIENT_LOOKER",
  "selected_servers": [
    "MCP-LOOKER"
  ]
}
```

## Query Parameters Reference

### Fields
- Format: `["table.field1", "table.field2"]`
- Examples: `["orders.order_date", "customers.customer_name", "products.product_name"]`

### Filters
- Format: `{"table.field": "value"}`
- Examples: 
  - `{"orders.status": "completed"}`
  - `{"orders.order_date": "2024-01-01"}`
  - `{"customers.region": "North America"}`

### Sorts
- Format: `["field1 desc", "field2 asc"]`
- Examples:
  - `["orders.order_date desc"]`
  - `["customers.total_revenue desc", "customers.customer_name asc"]`

### Limits
- Default: 1000
- Range: 1 to 5000 (depending on Looker instance settings)

## Notes

- Replace `"https://your-company.looker.com"` with your actual Looker instance URL
- Replace `"your-client-id"` and `"your-client-secret"` with your actual Looker API credentials
- The `model` and `explore` names should match those available in your Looker instance
- Field names should follow the format `table.field_name`
- All dates should be in ISO format (YYYY-MM-DD)
- The server will automatically handle authentication and token management 