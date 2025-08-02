from src.application.dtos.chat_dto import ChatRequest, ChatResponse
from src.application.interfaces.external.llm_service import LLMServiceInterface


class ChatService:
    """
    Service to handle chat interactions.
    """

    def __init__(self, llm_service: LLMServiceInterface):
        self.llm_service = llm_service

    async def get_response(self, request: ChatRequest) -> ChatResponse:
        """
        Generates a response to a user's question based on stock analysis and chat history.
        """
        prompt = self._build_prompt(request)
        llm_response_text = await self.llm_service.generate_text(prompt)
        return ChatResponse(assistant_response=llm_response_text)

    def _build_prompt(self, request: ChatRequest) -> str:
        """
        Constructs a comprehensive prompt for the LLM.
        """
        # System message to set the context for the LLM
        prompt = f"""You are a specialized financial analyst assistant. 
Your role is to answer questions about a stock analysis that has already been performed.
Do not provide new analysis, real-time data, or financial advice.
Base your answers *only* on the information provided in the 'Original Stock Analysis' and the 'Conversation History' below.
Keep your answers concise and directly related to the user's question.

---
**Original Stock Analysis:**
{request.stock_analysis}
---
"""

        # Add conversation history if it exists
        if request.chat_history:
            prompt += "**Conversation History:**\n"
            for message in request.chat_history:
                # Assuming message is a dict with 'role' and 'content' keys
                role = message.get('role', 'Unknown').capitalize()
                content = message.get('content', '')
                prompt += f"{role}: {content}\n"
            prompt += "---\n"

        # Add the new user question
        prompt += f"**New User Question:**\n{request.user_question}"

        return prompt
