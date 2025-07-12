# src/retriever.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class HybridRetriever:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.serper_api_key = os.getenv('SERPER_API_KEY')
        
    def local_retrieve(self, query, k=3):
        return self.kb.semantic_search(query, k)
    
    def web_retrieve(self, query, num_results=3):
        url = "https://google.serper.dev/search"
        payload = {
            "q": query,
            "num": num_results
        }
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return [item['snippet'] for item in response.json().get('organic', [])]
        return []
    
    def hybrid_search(self, query):
        local_results = self.local_retrieve(query)
        web_results = self.web_retrieve(query)
        return {
            "local": local_results,
            "web": web_results
        }