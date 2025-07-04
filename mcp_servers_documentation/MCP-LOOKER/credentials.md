# Looker MCP Server Credentials

## Overview
This document provides instructions on structuring the credentials needed to connect the Looker MCP Server in the Vanij Platform.

---

## Credential Format
```json
{
  "LOOKER": {
    "base_url": "https://your-looker-instance.com",
    "client_id": "your-looker-client-id",
    "client_secret": "your-looker-client-secret"
  }
}
```

- The `base_url` should point to your Looker instance (e.g., https://company.looker.com).
- The `client_id` and `client_secret` are required for API authentication.
- You can generate API credentials in the Looker Admin panel under Users > Edit > API Keys.
