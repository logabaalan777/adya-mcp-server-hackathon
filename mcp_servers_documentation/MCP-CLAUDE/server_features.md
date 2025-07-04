
---

###   *About MCP Server, Features, and Capabilities*
```markdown
# Claude MCP Server Overview

## What is the Claude MCP Server?
The Claude MCP Server is a connector within the Vanij Platform that enables seamless interaction with Google Gemini (Claude) models using the Gemini API.

---

## Key Features
- ✅ Generate chat completions using Gemini models
- ✅ Maintain and manage multi-turn conversation history
- ✅ Clear conversation history for any session
- ✅ Retrieve conversation history and metadata
- ✅ Get current model information and server status
- ✅ Summarize text
- ✅ Translate text between languages
- ✅ Analyze sentiment of text
- ✅ Extract keywords from text

---

## Capabilities
| Capability                | Description                                         |
|---------------------------|-----------------------------------------------------|
| Chat Completion           | Generate responses to user prompts using Gemini     |
| Conversation Management   | Track, retrieve, and clear conversation history     |
| Model Info                | Get current model, config, and server status        |
| Summarization             | Summarize long or complex text                      |
| Translation               | Translate text between languages                    |
| Sentiment Analysis        | Detect sentiment (positive, negative, neutral)      |
| Keyword Extraction        | Extract main keywords from text                     |

---

## Supported Gemini Models
- gemini-1.5-flash (default)
- Other Gemini models supported by the API

---

## Security Notes
- Authenticated via **Gemini API key** (passed per request)
- No credentials stored on server; all requests must include API key
- All communications must be secured over HTTPS

---

## Integration Use Cases
- AI-powered chatbots and assistants
- Automated content generation
- Conversation analytics and logging
- Text summarization and translation
- Sentiment and keyword analysis for feedback or reviews

```
