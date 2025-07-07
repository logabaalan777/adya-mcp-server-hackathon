# 🧩 Joomla MCP Server – Demos and Payload Examples

This section explains how to set up the Joomla MCP Server, gather required credentials (if needed), and interact with it using the correct JSON payload.

---

## 🎥 Demo Video

**Joomla MCP server setup + API execution + fetching content from Joomla CMS**  
📺 [Watch Here](#) *([Add your recorded video link](https://drive.google.com/file/d/1T4-CGetL0cXC0mkaBB0Unl-uiggTI7FH/view?usp=sharing))*

---

## 🎥 Credentials Gathering Video

**Setting up Joomla locally (Docker or manual) + login credentials (username/password) if using live instance**  
📺 [Watch Here](#) *(Add your recorded video link)*

---

## 🔐 Credential JSON Payload

> This is the format used to send credentials from the MCP Client to the Joomla MCP Server.

```json
{
  "JOOMLA": {
    "base_url": "http://your-joomla-site.com",
    "username": "your-admin-username",
    "password": "your-admin-password"
  }
}
