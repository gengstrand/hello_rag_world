import os
import logging
from typing import Generator
from indexer.indexer_facade import IndexerFacade

class FolderIndexer(IndexerFacade):
    def __init__(self, logger: logging.Logger, source: str):
        self._source = source
        self._title = os.path.basename(source)
        self._collection_name = self._title.replace(" ", "_").lower() + "_collection"
        self._logger = logger

    def documents(self) -> Generator[str, None, None]:
        for root, _, files in os.walk(self._source):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    yield f.read().replace('\n', ' ')

    def title(self) -> str:
        return self._title
    
    def collection_name(self) -> str:
        return self._collection_name
    
    def is_empty(self) -> bool:
        return not any(os.scandir(self._source))