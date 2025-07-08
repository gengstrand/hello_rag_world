from pypdf import PdfReader
from typing import Generator
from indexer.indexer_facade import IndexerFacade

class PDFIndexer(IndexerFacade):
    def __init__(self, source: str):
        self._source = source
        self._title = source

    def documents(self) -> Generator[str, None, None]:
        reader = PdfReader(self._source)
        metadata = reader.metadata
        if metadata and '/Title' in metadata:
            self._title = metadata['/Title']

        for page in reader.pages:
            yield page.extract_text().replace('\n', ' ')

    def title(self) -> str:
        return self._title