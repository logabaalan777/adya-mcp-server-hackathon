# Joomla MCP Server Credentials

## Overview
This document provides instructions on structuring the credentials needed to connect the Joomla MCP Server in the Vanij Platform.

---

## Credential Format
```json
{
  "JOOMLA": {
    "site_url": "https://your-joomla-site.com",
    "username": "your-joomla-username",
    "password": "your-joomla-password-or-app-password"
  }
}
```

- The `site_url` should point to your Joomla website.
- The `username` and `password` are required for authentication.
- Use an application password if your Joomla site supports it for better security.
