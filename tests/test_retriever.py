# tests/test_retriever.py
import pytest
from src.retriever import HybridRetriever
from src.Data_preprocessing import KnowledgeBase

@pytest.fixture
def setup():
    kb = KnowledgeBase('data/Assignment_Data_Base.xlsx')
    kb.create_embeddings()
    return HybridRetriever(kb)

def test_local_retrieve(setup):
    retriever = setup
    results = retriever.local_retrieve("hypoglycemia symptoms")
    assert len(results) == 3
    assert any("Hypoglycaemia" in result for result in results)

def test_hybrid_search(setup):
    retriever = setup
    results = retriever.hybrid_search("heart attack symptoms")
    assert 'local' in results
    assert 'web' in results
    assert len(results['local']) == 3