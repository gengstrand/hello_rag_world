import itertools

from pymilvus import MilvusClient
from search_facade import SearchFacade
from indexer.indexer_facade import IndexerFacade
from sentence_transformers import SentenceTransformer

def batch_iterator(iterable, n):
    """
    Batches an iterable into chunks of size n.
    The last batch may be shorter if the iterable's length is not a multiple of n.
    """
    it = iter(iterable)
    while True:
        batch = tuple(itertools.islice(it, n))
        if not batch:
            return
        yield batch

class MilvusFacade(SearchFacade):
    def __init__(self, indexer: IndexerFacade):
        self.indexer = indexer
        db_name = "./milvus_docs.db"
        self.client = MilvusClient(db_name)
        if self.client.has_collection(self.indexer.collection_name()):
            if not self.indexer.is_empty():
                self.client.drop_collection(self.indexer.collection_name())
                self.client.create_collection(
                    collection_name=self.indexer.collection_name(),
                    dimension=768,
                    metric_type="IP",
                    consistency_level="Strong"
                )
        else:
            self.client.create_collection(
                collection_name=self.indexer.collection_name(),
                dimension=768,
                metric_type="IP",
                consistency_level="Strong"
            )
        model_id = "sentence-transformers/all-distilroberta-v1"
        self.model = SentenceTransformer(model_id)

    def add_pages(self) -> str:
        if not self.indexer.is_empty():
            pn = 1
            for batch in batch_iterator(self.indexer.documents(), 100):
                data = []
                for doc in batch:
                    data.append({"id": pn, "vector": self.model.encode(doc), "text": doc})
                    pn += 1
                self.client.insert(collection_name=self.indexer.collection_name(), data=data)
        return self.indexer.title()

    def search(self, query: str, top_results: int, simularity: float) -> list[str]:
        results = self.client.search(
            collection_name=self.indexer.collection_name(),
            data=[self.model.encode(query)],
            limit=top_results,
            search_params={"metric_type": "IP", "params": {}},
            output_fields=["text"]
        )
        return [ res["entity"]["text"] for res in results[0] if res["distance"] > simularity ]
