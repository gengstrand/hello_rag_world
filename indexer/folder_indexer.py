import os
from typing import Generator
from indexer.indexer_facade import IndexerFacade

class FolderIndexer(IndexerFacade):
    def __init__(self, source: str):
        self._source = source
        self._title = os.path.basename(source)

    def documents(self) -> Generator[str, None, None]:
        for root, _, files in os.walk(self._source):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    yield f.read().replace('\n', ' ')

    def title(self) -> str:
        return self._title