import google.generativeai as genai
import logging
import os

logger = logging.getLogger(__name__)

# Configure API Key (In prod, use env var. Here using hardcoded for demo as requested)
GEMINI_API_KEY = "enter your API key"
genai.configure(api_key=GEMINI_API_KEY)

class GeminiService:
    def __init__(self):
        # Using the latest stable model
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def explain_paper(self, title: str, abstract: str) -> str:
        """
        Generates a simplified explanation of the paper.
        """
        prompt = f"""
        You are an expert research assistant. 
        Read the following paper abstract and explain it to a software engineer who is not an expert in this specific field.
        
        Title: {title}
        Abstract: {abstract}
        
        Task:
        1. Summarize the core problem they are solving in 1 sentence.
        2. Explain their solution/method in 1-2 simple sentences.
        3. Mention the key result/improvement if any.
        
        Format: Return HTML with <p> tags. Keep it short (max 100 words).
        """
        try:
            logger.info(f"Sending prompt to Gemini for paper: {title[:30]}...")
            response = await self.model.generate_content_async(prompt)
            logger.info("Gemini response received.")
            return response.text
        except Exception as e:
            logger.error(f"Gemini Error details: {e}")
            return f"<p style='color:red'>Error: {e}. Check server logs.</p>"

_gemini_instance = None

def get_gemini_service():
    global _gemini_instance
    if _gemini_instance is None:
        _gemini_instance = GeminiService()
    return _gemini_instance
