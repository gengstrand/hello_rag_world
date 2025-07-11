import unittest
import logging
from unittest.mock import MagicMock
from client import HelloRagClient, DynamicFacade

logger = logging.Logger('test')
logger.info = MagicMock()

class TestClient(unittest.TestCase):

    def test_pdf_run(self):
        indexer = DynamicFacade('indexer.pdf_indexer', 'PDFIndexer', logger).create("test.pdf")
        t = HelloRagClient(
            DynamicFacade('txtai_facade', 'TxtAiFacade', logger).create(indexer),
            DynamicFacade('llm.mocked_llm', 'MockedLargeLanguageModel', logger).create(),
            logger
        ).run(True)
        self.assertTrue(t)

    def test_folder_run(self):
        indexer = DynamicFacade('indexer.folder_indexer', 'FolderIndexer', logger).create("test")
        t = HelloRagClient(
            DynamicFacade('txtai_facade', 'TxtAiFacade', logger).create(indexer),
            DynamicFacade('llm.mocked_llm', 'MockedLargeLanguageModel', logger).create(),
            logger
        ).run(True)
        self.assertTrue(t)

if __name__ == '__main__':
    unittest.main()