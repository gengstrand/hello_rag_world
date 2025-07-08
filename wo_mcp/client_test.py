import unittest
from client import HelloRagClient, DynamicFacade

class TestClient(unittest.TestCase):
    def test_pdf_run(self):
        indexer = DynamicFacade('indexer.pdf_indexer', 'PDFIndexer').create("test.pdf")
        t = HelloRagClient(
            DynamicFacade('txtai_facade', 'TxtAiFacade').create(indexer),
            DynamicFacade('llm.mocked_llm', 'MockedLargeLanguageModel').create()
        ).run(True)
        self.assertTrue(t)

    def test_folder_run(self):
        indexer = DynamicFacade('indexer.folder_indexer', 'FolderIndexer').create("test")
        t = HelloRagClient(
            DynamicFacade('txtai_facade', 'TxtAiFacade').create(indexer),
            DynamicFacade('llm.mocked_llm', 'MockedLargeLanguageModel').create()
        ).run(True)
        self.assertTrue(t)

if __name__ == '__main__':
    unittest.main()