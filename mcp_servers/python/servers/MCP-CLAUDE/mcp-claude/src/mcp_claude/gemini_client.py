import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import google.generativeai as genai
except ImportError as e:
    print(f"Missing required packages: {e}")
    print("Install with: pip install google-generativeai")
    raise

logger = logging.getLogger(__name__)

@dataclass
class Message:
    """Message data structure"""
    role: str
    content: str
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class ConversationManager:
    """Manages conversation history and state"""

    def __init__(self):
        self.conversations: Dict[str, List[Message]] = {}
        self.system_prompts: Dict[str, str] = {}
        self.conversation_metadata: Dict[str, Dict] = {}

    def add_message(self, conversation_id: str, role: str, content: str, metadata: Dict = None) -> None:
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
            self.conversation_metadata[conversation_id] = {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "message_count": 0
            }
        message = Message(role=role, content=content)
        self.conversations[conversation_id].append(message)
        self.conversation_metadata[conversation_id]["last_updated"] = datetime.now().isoformat()
        self.conversation_metadata[conversation_id]["message_count"] += 1
        logger.info(f"Added {role} message to conversation {conversation_id}")

    def get_conversation(self, conversation_id: str) -> List[Dict]:
        messages = self.conversations.get(conversation_id, [])
        return [asdict(msg) for msg in messages]

    def get_conversation_summary(self, conversation_id: str) -> Dict:
        messages = self.get_conversation(conversation_id)
        metadata = self.conversation_metadata.get(conversation_id, {})
        return {
            "conversation_id": conversation_id,
            "messages": messages,
            "metadata": metadata,
            "system_prompt": self.system_prompts.get(conversation_id)
        }

    def clear_conversation(self, conversation_id: str) -> bool:
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            if conversation_id in self.system_prompts:
                del self.system_prompts[conversation_id]
            if conversation_id in self.conversation_metadata:
                del self.conversation_metadata[conversation_id]
            logger.info(f"Cleared conversation {conversation_id}")
            return True
        return False

    def set_system_prompt(self, conversation_id: str, system_prompt: str) -> None:
        self.system_prompts[conversation_id] = system_prompt
        logger.info(f"Set system prompt for conversation {conversation_id}")

    def get_system_prompt(self, conversation_id: str) -> Optional[str]:
        return self.system_prompts.get(conversation_id)

class GeminiClient:
    """Gemini API client wrapper"""

    def __init__(self):
        self.client = None
        self.model_name = "gemini-1.5-flash"
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 4096,
        }

    def initialize(self, api_key: str, model_name: str = None) -> bool:
        try:
            genai.configure(api_key=api_key)
            self.model_name = model_name or self.model_name
            self.client = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config
            )
            test_response = self.client.generate_content("Hello")
            if test_response.text:
                logger.info(f"Gemini client initialized successfully with model {self.model_name}")
                return True
            else:
                logger.error("Gemini client test failed - no response")
                return False
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            self.client = None
            return False

    def generate_response(self, messages: List[Dict], system_prompt: Optional[str] = None, **kwargs) -> str:
        if not self.client:
            raise Exception("Gemini client not initialized. Please call initialize_client first.")
        try:
            formatted_prompt = self._format_messages(messages, system_prompt)
            gen_config = self.generation_config.copy()
            gen_config.update(kwargs)
            response = self.client.generate_content(
                formatted_prompt,
                generation_config=gen_config
            )
            if response.text:
                return response.text.strip()
            else:
                return "No response generated by the model"
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise Exception(f"API call failed: {str(e)}")

    def _format_messages(self, messages: List[Dict], system_prompt: Optional[str] = None) -> str:
        formatted = ""
        if system_prompt:
            formatted += f"System Instructions: {system_prompt}\n\n"
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role == 'user':
                formatted += f"Human: {content}\n"
            elif role == 'assistant':
                formatted += f"Assistant: {content}\n"
            else:
                formatted += f"{role.capitalize()}: {content}\n"
        formatted += "Assistant: "
        return formatted

    def get_model_info(self) -> Dict:
        return {
            "model_name": self.model_name,
            "generation_config": self.generation_config,
            "initialized": self.client is not None
        }

# Global instances for import in tool handlers
gemini_client = GeminiClient()
conversation_manager = ConversationManager()