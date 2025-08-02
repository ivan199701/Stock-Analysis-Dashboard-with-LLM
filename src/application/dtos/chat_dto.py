from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ChatRequest:
    """
    Data transfer object for a chat request.
    """
    stock_analysis: Dict[str, Any]
    chat_history: List[Dict[str, str]]
    user_question: str

@dataclass
class ChatResponse:
    """
    Data transfer object for a chat response.
    """
    assistant_response: str
