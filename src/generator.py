# src/generator.py
from openai import OpenAI
from dotenv import load_dotenv
import os
import re

load_dotenv()

class ResponseGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def generate_response(self, query, retrieved_info):
        disclaimer = "This information is for educational purposes only and is not a substitute for professional medical advice."
        
        prompt = f"""You are a medical first-aid assistant. Provide concise guidance (≤250 words) for the following query:
        
        Query: {query}
        
        Retrieved Information:
        - Local Knowledge: {retrieved_info['local']}
        - Web Results: {retrieved_info['web']}
        
        Structure your response with:
        1. Likely condition(s)
        2. Immediate first-aid steps
        3. Key medications (if applicable)
        4. When to seek emergency care
        5. Sources (cite as 'Local Knowledge #X' or 'Web Result #X')
        
        Always begin with the disclaimer: {disclaimer}"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        
        return response.choices[0].message.content