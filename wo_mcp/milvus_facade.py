from pymilvus import MilvusClient
from search_facade import SearchFacade
from indexer.indexer_facade import IndexerFacade
from sentence_transformers import SentenceTransformer

class MilvusFacade(SearchFacade):
    def __init__(self, indexer: IndexerFacade):
        self.indexer = indexer
        db_name = "./milvus_pdf.db"
        self.collection_name = "doc_pages"
        self.client = MilvusClient(db_name)
        if self.client.has_collection(self.collection_name):
            self.client.drop_collection(self.collection_name)
        self.client.create_collection(
            collection_name=self.collection_name,
            dimension=768,
            metric_type="IP",
            consistency_level="Strong"
        )
        model_id = "sentence-transformers/all-distilroberta-v1"
        self.model = SentenceTransformer(model_id)

    def add_pages(self) -> str:
        data = []
        pn = 1
        for doc in self.indexer.documents():
            data.append({"id": pn, "vector": self.model.encode(doc), "text": doc})
            pn += 1
        self.client.insert(collection_name=self.collection_name, data=data)
        return self.indexer.title()

    def search(self, query: str, top_results: int, simularity: float) -> list[str]:
        results = self.client.search(
            collection_name=self.collection_name,
            data=[self.model.encode(query)],
            limit=top_results,
            search_params={"metric_type": "IP", "params": {}},
            output_fields=["text"]
        )
        return [ res["entity"]["text"] for res in results[0] if res["distance"] > simularity ]
