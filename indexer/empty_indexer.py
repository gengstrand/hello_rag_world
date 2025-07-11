import logging
from typing import Generator
from indexer.indexer_facade import IndexerFacade

class EmptyIndexer(IndexerFacade):
    def __init__(self, logger: logging.Logger, source: str = "empty"):
        self._logger = logger
        self._source = source
        self._source = source

    def documents(self) -> Generator[str, None, None]:
        yield from []

    def title(self) -> str:
        return self._source

    def collection_name(self) -> str:
        return self._source

    def is_empty(self) -> bool:
        return True