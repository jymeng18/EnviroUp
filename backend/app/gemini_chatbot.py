# app/gemini_chatbot.py
import os
import google.generativeai as genai
from typing import Optional

class FirePreventionChatbot:
    def __init__(self):
        # Initialize Gemini API
        api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # System prompt for fire prevention expertise
        self.system_prompt = """You are a knowledgeable fire prevention and wildfire safety expert. Your role is to provide helpful, accurate, and practical advice about:

1. Wildfire prevention techniques
2. Home and property protection strategies
3. Emergency preparedness for wildfires
4. Fire safety best practices
5. Evacuation planning
6. Fire-resistant landscaping
7. Community fire safety
8. Understanding fire danger ratings
9. Creating defensible space around homes
10. Fire-safe building materials and construction
11. Limit your response to max 40 words

Always provide practical, actionable advice. If asked about something outside fire prevention, politely redirect to fire safety topics. Be encouraging and supportive while emphasizing the importance of preparedness.

Keep responses concise but informative, and always prioritize safety."""
    
    def chat(self, user_message: str, conversation_history: Optional[list] = None) -> dict:
        """
        Process a user message and return a response from the fire prevention chatbot
        
        Args:
            user_message: The user's question or message
            conversation_history: Optional list of previous messages for context
            
        Returns:
            dict: Response containing the chatbot's reply and metadata
        """
        try:
            # Prepare the conversation context
            if conversation_history:
                # Format conversation history for Gemini
                context = self.system_prompt + "\n\nPrevious conversation:\n"
                for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                    role = "User" if msg.get('role') == 'user' else "Assistant"
                    context += f"{role}: {msg.get('content', '')}\n"
                context += f"\nUser: {user_message}"
            else:
                context = f"{self.system_prompt}\n\nUser: {user_message}"
            
            # Generate response
            response = self.model.generate_content(context)
            
            return {
                'success': True,
                'message': response.text,
                'timestamp': self._get_timestamp(),
                'model': 'gemini-2.0-flash'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Chatbot error: {str(e)}",
                'timestamp': self._get_timestamp()
            }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as string"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_welcome_message(self) -> dict:
        """Get a welcome message for new users"""
        welcome_msg = """🔥 Yo what's up, I am Henry, your 'fire' safety assistant! 

I'm here to help you with wildfire safety and prevention. I can assist you with:\n

 Creating defensible space around your home,\n
 Fire-resistant landscaping tips,\n
 Emergency evacuation planning,\n
 Understanding fire danger ratings,\n
 Home protection strategies,\n
 Community fire safety.

What would you like to know about fire prevention?"""
        
        return {
            'success': True,
            'message': welcome_msg,
            'timestamp': self._get_timestamp(),
            'is_welcome': True
        }
