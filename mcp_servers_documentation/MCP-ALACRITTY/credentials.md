# Alacritty MCP Server Credentials

## Overview
This document provides instructions on structuring the credentials needed to connect the Alacritty MCP Server in the Vanij Platform.

---

## Credential Format
```json
{
  "ALACRITTY": {
    "config_path": "/path/to/alacritty.yml"
  }
}
```

- The `config_path` should point to your Alacritty configuration file (YAML or TOML format).
- Supported formats: `.yml`, `.yaml`, `.toml`
- No API keys or secrets are required; only the config file path is needed for all operations.
