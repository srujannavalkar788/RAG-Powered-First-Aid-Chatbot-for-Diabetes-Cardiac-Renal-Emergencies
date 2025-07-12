# src/data_preprocessing.py
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class KnowledgeBase:
    excel_path = 'data/Assignment Data Base.xlsx'
    def __init__(self, excel_path):
        self.df = pd.read_excel(excel_path)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        
    def create_embeddings(self):
        sentences = self.df['Sentence'].tolist()
        embeddings = self.model.encode(sentences, convert_to_tensor=False)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        return embeddings
    
    def save_index(self, path):
        faiss.write_index(self.index, path)
        
    def semantic_search(self, query, k=5):
        query_embedding = self.model.encode(query, convert_to_tensor=False)
        D, I = self.index.search(np.array([query_embedding]), k)
        return [self.df.iloc[i]['Sentence'] for i in I[0]]