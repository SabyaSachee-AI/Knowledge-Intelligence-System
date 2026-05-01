import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbedding
from app.config import config


class VectorStore:
    def __init__(self, path):
        self.embeddings = OpenAIEmbedding(openai_api_key=config.OPENAI_API_KEY)
        self.vector_store = Chroma(
            persist_directory=path,
            embedding_function=self.embeddings
        )

    def add_documents(self, documents):
        """Add documents to vector store"""
        return self.vector_store.add_documents(documents)

    def similarity_search(self, query, k=4):
        """Search for similar documents"""
        return self.vector_store.similarity_search(query, k=k)

