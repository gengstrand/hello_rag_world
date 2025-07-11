import os
import logging
from pypdf import PdfReader
from typing import Generator
from indexer.indexer_facade import IndexerFacade

class PDFIndexer(IndexerFacade):
    def __init__(self, logger: logging.Logger, source: str):
        self._source = source
        self._title = source
        self._collection_name = os.path.basename(source).replace(" ", "_").lower() + "_collection"
        self._logger = logger

    def documents(self) -> Generator[str, None, None]:
        reader = PdfReader(self._source)
        metadata = reader.metadata
        if metadata and '/Title' in metadata:
            self._title = metadata['/Title']

        for page in reader.pages:
            yield page.extract_text().replace('\n', ' ')

    def title(self) -> str:
        return self._title
    
    def collection_name(self) -> str:
        return self._collection_name
    
    def is_empty(self) -> bool:
        return not os.path.exists(self._source) or os.path.getsize(self._source) == 0