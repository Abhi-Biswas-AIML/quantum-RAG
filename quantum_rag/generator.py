import google.generativeai as genai
import os

class GeminiGenerator:
    def __init__(self, api_key: str = None):
        """
        Initialize Gemini Generator.
        If api_key is not provided, looks for GOOGLE_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API Key is required for generation. Please provide it or set GOOGLE_API_KEY environment variable.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate(self, prompt: str) -> str:
        """
        Generate a response using Gemini.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
