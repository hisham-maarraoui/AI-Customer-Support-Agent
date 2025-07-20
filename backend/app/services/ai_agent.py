import google.generativeai as genai
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.services.vector_store import vector_store
from app.services.guardrails import GuardrailsService
import json
import logging
import time

logger = logging.getLogger(__name__)

class AIAgentService:
    def __init__(self):
        # Configure Google Gemini
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
        self.guardrails = GuardrailsService()
        
        # System prompt for the AI agent
        self.system_prompt = """You are an Apple Support AI Agent, designed to help users with questions about Apple products and services. 

Your role is to:
1. Provide accurate, helpful information about Apple products, services, and troubleshooting
2. Be friendly, professional, and empathetic
3. Always cite your sources when providing information
4. Redirect users to official Apple support channels when appropriate
5. Never provide personal, legal, or financial advice
6. Detect and handle sensitive queries appropriately

When responding:
- Use the provided context from Apple's official support documentation
- If you don't have enough information, suggest contacting Apple Support directly
- Be concise but thorough
- Use a helpful, conversational tone
- Always mention the source of your information

Available tools:
- schedule_meeting: Can schedule a meeting with Apple Support if the user requests it

Remember: You are not a replacement for official Apple Support, but a helpful assistant to guide users to the right information."""
    
    def generate_response(self, user_message: str, conversation_history: List[Dict] = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate a response using RAG"""
        try:
            # Check guardrails first
            guardrail_check = self.guardrails.check_message(user_message)
            if guardrail_check['flagged']:
                return {
                    'message': guardrail_check['response'],
                    'sources': [],
                    'confidence': 0.0,
                    'guardrail_triggered': True,
                    'guardrail_type': guardrail_check['type']
                }
            
            # Search for relevant information
            try:
                search_results = vector_store.search(user_message, k=5)
                # Prepare context from search results
                context_text = self._prepare_context(search_results)
            except Exception as search_error:
                logger.warning(f"Vector search failed: {search_error}")
                search_results = []
                context_text = "No specific information found in the knowledge base."
            
            # Prepare conversation history
            messages = self._prepare_messages(user_message, conversation_history, context_text)
            
            # Generate response using Gemini with better error handling
            try:
                response = self.model.generate_content(
                    messages,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=1000,
                    )
                )
                
                # Process response
                assistant_message = response.text
                
            except Exception as gemini_error:
                error_str = str(gemini_error)
                logger.error(f"Gemini API error: {error_str}")
                
                # Handle quota exceeded error
                if "429" in error_str or "quota" in error_str.lower():
                    return {
                        'message': "I'm currently experiencing high demand. Please try again in a few minutes, or contact Apple Support directly for immediate assistance.",
                        'sources': self._format_sources(search_results),
                        'confidence': 0.3,
                        'error': 'quota_exceeded',
                        'fallback_response': True
                    }
                else:
                    # For other Gemini errors, provide a helpful fallback
                    return {
                        'message': "I'm having trouble processing your request right now. Here's what I found in our knowledge base that might help:",
                        'sources': self._format_sources(search_results),
                        'confidence': 0.2,
                        'error': 'gemini_error',
                        'fallback_response': True
                    }
            
            # Check if response contains tool usage (simplified for Gemini)
            if self._should_use_tools(user_message):
                tool_response = self._handle_tool_usage(assistant_message, user_message, conversation_history)
                if tool_response:
                    return tool_response
            
            # Format sources
            sources = self._format_sources(search_results)
            
            # Calculate confidence based on search results
            confidence = self._calculate_confidence(search_results)
            
            return {
                'message': assistant_message,
                'sources': sources,
                'confidence': confidence,
                'guardrail_triggered': False
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                'message': "I apologize, but I'm experiencing technical difficulties. Please try again or contact Apple Support directly for assistance.",
                'sources': [],
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _prepare_context(self, search_results: List[Dict[str, Any]]) -> str:
        """Prepare context from search results"""
        if not search_results:
            return "No specific information found in the knowledge base."
        
        context_parts = []
        for i, result in enumerate(search_results[:3]):  # Use top 3 results
            content = result['content']
            metadata = result['metadata']
            
            source_info = f"Source {i+1}: {metadata.get('title', 'Unknown')} ({metadata.get('url', 'No URL')})"
            context_parts.append(f"{source_info}\n{content}\n")
        
        return "\n".join(context_parts)
    
    def _prepare_messages(self, user_message: str, conversation_history: List[Dict] = None, context: str = None) -> List[str]:
        """Prepare messages for Gemini API"""
        messages = []
        
        # Add system prompt
        system_content = self.system_prompt
        
        # Add context if available
        if context:
            system_content += f"\n\nHere is relevant information from Apple's support documentation:\n\n{context}\n\nUse this information to answer the user's question. Always cite the sources when providing information."
        
        messages.append(system_content)
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-10:]:  # Limit to last 10 messages
                if msg['role'] == 'user':
                    messages.append(f"User: {msg['content']}")
                elif msg['role'] == 'assistant':
                    messages.append(f"Assistant: {msg['content']}")
        
        # Add current user message
        messages.append(f"User: {user_message}")
        messages.append("Assistant:")
        
        return messages
    
    def _format_sources(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Format search results as sources"""
        sources = []
        seen_urls = set()
        
        for result in search_results:
            metadata = result['metadata']
            url = metadata.get('url', '')
            
            # Avoid duplicate sources
            if url and url not in seen_urls:
                seen_urls.add(url)
                sources.append({
                    'title': metadata.get('title', 'Apple Support'),
                    'url': url,
                    'product': metadata.get('product', ''),
                    'content_type': metadata.get('content_type', ''),
                    'relevance_score': result.get('score', 0.0)
                })
        
        return sources[:3]  # Limit to top 3 sources
    
    def _calculate_confidence(self, search_results: List[Dict[str, Any]]) -> float:
        """Calculate confidence based on search results"""
        if not search_results:
            return 0.0
        
        # Calculate average score of top results
        scores = [result.get('score', 0.0) for result in search_results[:3]]
        avg_score = sum(scores) / len(scores)
        
        # Convert similarity score to confidence (0-1)
        # Higher similarity scores indicate better matches
        confidence = min(avg_score * 2, 1.0)  # Scale and cap at 1.0
        
        return round(confidence, 2)
    
    def _should_use_tools(self, user_message: str) -> bool:
        """Determine if tools should be used based on user message"""
        tool_keywords = [
            'schedule', 'appointment', 'meeting', 'call', 'speak', 'talk',
            'book', 'reserve', 'set up', 'arrange'
        ]
        
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in tool_keywords)
    
    def _handle_tool_usage(self, assistant_message: str, user_message: str, conversation_history: List[Dict] = None) -> Optional[Dict[str, Any]]:
        """Handle tool usage from the AI agent (simplified for Gemini)"""
        try:
            # Check if the message contains scheduling-related content
            if any(keyword in assistant_message.lower() for keyword in ['schedule', 'appointment', 'meeting']):
                # Simulate scheduling a meeting
                meeting_id = f"meeting_{int(time.time())}"
                
                # Create a response with meeting details
                meeting_response = f"""I'd be happy to help you schedule a meeting with Apple Support!

Meeting ID: {meeting_id}
Status: Pending confirmation

To complete the scheduling, please provide:
- Your name
- Email address
- Phone number (optional)
- Preferred date and time
- Brief description of what you need help with

You can also call Apple Support directly at 1-800-275-2273 for immediate assistance."""
                
                return {
                    'message': meeting_response,
                    'sources': [],
                    'confidence': 0.8,
                    'guardrail_triggered': False,
                    'tool_used': 'schedule_meeting',
                    'meeting_id': meeting_id
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error handling tool usage: {e}")
            return None
    
    def get_product_specific_response(self, user_message: str, product: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Generate a product-specific response"""
        try:
            # Add product context to the search
            product_query = f"{product} {user_message}"
            search_results = vector_store.search(product_query, k=5)
            
            # Filter results for the specific product
            product_results = [
                result for result in search_results 
                if product.lower() in result['metadata'].get('product', '').lower()
            ]
            
            if not product_results:
                product_results = search_results  # Fallback to general results
            
            context_text = self._prepare_context(product_results)
            
            # Prepare messages with product context
            system_content = f"{self.system_prompt}\n\nFocus on {product} specifically. Use the provided context to give accurate information about {product}."
            
            if context_text:
                system_content += f"\n\nHere is relevant information about {product}:\n\n{context_text}"
            
            messages = [system_content, f"User: {user_message}", "Assistant:"]
            
            # Generate response
            response = self.model.generate_content(
                messages,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1000,
                )
            )
            
            # Format sources
            sources = self._format_sources(product_results)
            confidence = self._calculate_confidence(product_results)
            
            return {
                'message': response.text,
                'sources': sources,
                'confidence': confidence,
                'product': product,
                'guardrail_triggered': False
            }
            
        except Exception as e:
            logger.error(f"Error generating product-specific response: {e}")
            return {
                'message': f"I apologize, but I'm having trouble finding specific information about {product}. Please try rephrasing your question or contact Apple Support directly.",
                'sources': [],
                'confidence': 0.0,
                'product': product,
                'error': str(e)
            }
    
    def get_voice_response(self, user_message: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Generate a response optimized for voice interaction"""
        try:
            # Check guardrails
            guardrail_check = self.guardrails.check_message(user_message)
            if guardrail_check['flagged']:
                return {
                    'message': guardrail_check['response'],
                    'sources': [],
                    'confidence': 0.0,
                    'guardrail_triggered': True,
                    'guardrail_type': guardrail_check['type']
                }
            
            # Search for relevant information
            search_results = vector_store.search(user_message, k=3)  # Fewer results for voice
            context_text = self._prepare_context(search_results)
            
            # Prepare voice-optimized system prompt
            voice_system_prompt = f"""{self.system_prompt}

For voice interactions:
- Keep responses concise and conversational
- Use simple, clear language
- Avoid complex technical jargon
- Be more direct and actionable
- Focus on the most important information first

{context_text if context_text else 'No specific information found in the knowledge base.'}"""
            
            messages = [voice_system_prompt, f"User: {user_message}", "Assistant:"]
            
            # Generate response
            response = self.model.generate_content(
                messages,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=500,  # Shorter for voice
                )
            )
            
            sources = self._format_sources(search_results)
            confidence = self._calculate_confidence(search_results)
            
            return {
                'message': response.text,
                'sources': sources,
                'confidence': confidence,
                'guardrail_triggered': False,
                'voice_optimized': True
            }
            
        except Exception as e:
            logger.error(f"Error generating voice response: {e}")
            return {
                'message': "I apologize, but I'm experiencing technical difficulties. Please try again or contact Apple Support directly.",
                'sources': [],
                'confidence': 0.0,
                'error': str(e)
            } 

# Global instance
ai_agent = AIAgentService() 