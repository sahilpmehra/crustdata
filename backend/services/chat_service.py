from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME, MAX_TOKENS
from .vector_store import VectorStoreService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.vector_store = VectorStoreService(OPENAI_API_KEY)

    async def get_chat_response(self, message: str) -> str:
        try:
            logger.info(f"Searching for relevant documentation for query: {message}")
            search_results = await self.vector_store.search(message, k=3)
            logger.info(f"Found {len(search_results)} relevant documents")
            
            context = self._format_context(search_results)
            logger.info("Created context from search results")
            
            # Create the system message with context
            system_message = f"""You are a helpful assistant that provides information about Crustdata APIs.
Base your responses on the following documentation context:

{context}

If the context doesn't contain relevant information, you can say so. Provide a curl command to get the information that you can use to answer the question based on the context. Always maintain a helpful and professional tone."""

            # Create the chat completion with context
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": message}
                ],
                max_tokens=MAX_TOKENS,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI Error: {str(e)}")  # Debug print
            return f"Error processing your request: {str(e)}"

    def _format_context(self, search_results: list) -> str:
        context_parts = []
        
        for result in search_results:
            content = result['content']
            metadata = result['metadata']
            
            context_part = f"""
Section: {metadata['section']}
Source: {metadata['url']}
Content: {content}
---"""
            context_parts.append(context_part)
            
        return "\n".join(context_parts)
