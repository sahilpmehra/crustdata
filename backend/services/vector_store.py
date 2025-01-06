from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List
import os
from config_prod import VECTOR_STORE_PATH

class VectorStoreService:
    def __init__(self, openai_api_key: str):
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.persist_directory = VECTOR_STORE_PATH
        
        # Load existing vector store if it exists
        if os.path.exists(self.persist_directory):
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        else:
            os.makedirs(self.persist_directory, exist_ok=True)
            self.vector_store = None

    def create_embeddings(self, texts: List[str], metadatas: List[dict]):
        self.vector_store = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
            persist_directory=self.persist_directory
        )
        self.vector_store.persist()

    async def search(self, query: str, k: int = 3):
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Please run initialize_vectors.py first.")
        
        results = self.vector_store.similarity_search(query, k=k)
        return [{
            'content': doc.page_content,
            'metadata': doc.metadata
        } for doc in results]