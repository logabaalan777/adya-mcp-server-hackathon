# OpenStreetMap MCP Server Credentials

## Overview
This document provides instructions on structuring the credentials needed to connect the OpenStreetMap MCP Server in the Vanij Platform.

---

## Credential Format
```json
{
  "OPENSTREETMAP": {
    "api_url": "https://api.openstreetmap.org" 
  }
}
```

- The `api_url` is optional and defaults to the public OpenStreetMap API if not provided.
- No authentication or API key is required for standard usage.
- For advanced or private OSM deployments, specify the custom API URL as needed.
