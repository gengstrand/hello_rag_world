import logging

from txtai import Embeddings
from search_facade import SearchFacade
from indexer.indexer_facade import IndexerFacade

class TxtAiFacade(SearchFacade):
    def __init__(self, logger: logging.Logger, indexer: IndexerFacade):
        self.embeddings = Embeddings(hybrid=True, path="sentence-transformers/nli-mpnet-base-v2")
        self.indexer = indexer
        self.data = []
        self.logger = logger

    def add_pages(self) -> str:
        for doc in self.indexer.documents():
            self.data.append(doc)
        self.embeddings.index(self.data)
        return self.indexer.title()

    def search(self, query: str, top_results: int, simularity: float) -> list[str]:
        return [ self.data[index] for (index, score) in self.embeddings.search(query, top_results) if score > simularity ]
