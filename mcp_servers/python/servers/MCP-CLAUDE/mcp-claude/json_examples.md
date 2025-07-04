# JSON Examples for MCP-CLAUDE Tools

## 1. Chat Completion (`chat_completion`)
```json
{
  "client_details": {
    "tool_name": "chat_completion",
    "arguments": {
      "messages": [
        {"role": "user", "content": "Hello, who are you?"}
      ],
      "conversation_id": "my-convo-1",
      "system_prompt": "You are a helpful assistant.",
      "temperature": 0.7,
      "max_tokens": 256,
      "api_key": "YOUR_GEMINI_API_KEY"
    }
  }
}
```

## 2. Clear Conversation (`clear_conversation`)
```json
{
  "client_details": {
    "tool_name": "clear_conversation",
    "arguments": {
      "conversation_id": "my-convo-1"
    }
  }
}
```

## 3. Get Conversation History (`get_conversation_history`)
```json
{
  "client_details": {
    "tool_name": "get_conversation_history",
    "arguments": {
      "conversation_id": "my-convo-1",
      "include_metadata": true
    }
  }
}
```

## 4. Get Model Info (`get_model_info`)
```json
{
  "client_details": {
    "tool_name": "get_model_info",
    "arguments": {}
  }
}
```

## 5. Summarize Text (`summarize_text`)
```json
{
  "client_details": {
    "tool_name": "summarize_text",
    "arguments": {
      "text": "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of intelligent agents: any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.",
      "api_key": "YOUR_GEMINI_API_KEY"
    }
  }
}
```

## 6. Translate Text (`translate_text`)
```json
{
  "client_details": {
    "tool_name": "translate_text",
    "arguments": {
      "text": "Hello, how are you today?",
      "source_lang": "en",
      "target_lang": "fr",
      "api_key": "YOUR_GEMINI_API_KEY"
    }
  }
}
```

## 7. Sentiment Analysis (`sentiment_analysis`)
```json
{
  "client_details": {
    "tool_name": "sentiment_analysis",
    "arguments": {
      "text": "I absolutely love this product! It has exceeded all my expectations and I would highly recommend it to everyone.",
      "api_key": "YOUR_GEMINI_API_KEY"
    }
  }
}
```

## 8. Extract Keywords (`extract_keywords`)
```json
{
  "client_details": {
    "tool_name": "extract_keywords",
    "arguments": {
      "text": "Artificial intelligence and machine learning are transforming industries by enabling computers to learn from data and make decisions.",
      "api_key": "YOUR_GEMINI_API_KEY"
    }
  }
}
``` 