import os
import chromadb
from chromadb.utils import embedding_functions
from app.schemas.bco import BCO
from typing import List

class VectorStore:
    def __init__(self):
        # In a real local deployment, this would persist to disk
        self.client = chromadb.Client()
        self.openai_ef = None
        if os.getenv("OPENAI_API_KEY"):
            self.openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-3-small"
            )

        self.collection = self.client.get_or_create_collection(
            name="cortex_bcos",
            embedding_function=self.openai_ef
        )

    def add_bco(self, bco: BCO):
        content = f"{bco.label} {bco.type} {' '.join(bco.evidence)}"
        self.collection.add(
            documents=[content],
            metadatas=[{
                "bco_id": bco.bco_id,
                "scope": bco.scope,
                "type": bco.type
            }],
            ids=[bco.bco_id]
        )

    def search_bcos(self, query: str, n_results: int = 5) -> List[str]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return [meta["bco_id"] for meta in results["metadatas"][0]]
