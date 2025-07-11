import os
import sys
import logging
import importlib
import importlib.util
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))
from search_facade import SearchFacade
from llm.llm_facade import LargeLanguageModelFacade

def import_from_path(module_name, file_path):
    """Import a module given its name and file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

class DynamicFacade:
    def __init__(self, facade_module: str, facade_class: str, logger: logging.Logger):
        self.facade_module = facade_module
        self.facade_class = facade_class
        self.logger = logger

    def create(self, ctor_arg = None):
        if '.' in self.facade_module:
            m = import_from_path(self.facade_module, f"../{self.facade_module.replace('.', '/')}.py")
        else:
            m = importlib.import_module(self.facade_module)
        c = getattr(m, self.facade_class)
        if ctor_arg is None:
            rv = c(self.logger)
        else:
            rv = c(self.logger, ctor_arg)
        return rv

class HelloRagClient:
    def __init__(self, search: SearchFacade, llm: LargeLanguageModelFacade, logger: logging.Logger, max_results: int = 10):
        self._search = search
        self._llm = llm
        self._logger = logger
        self._max_results = max_results

    def run(self, test_mode: bool = False) -> bool:
        title = self._search.add_pages()
        if test_mode:
            results = self._search.search("test", 2 * self._max_results, 0.1)
            return len(results) > 0
        else:
            question = input(f"What do you want to know about {title}? ")
            while len(question) > 0:
                results = self._search.search(question, 2 * self._max_results, 0.1)
                ranked_results = []
                for result in results:
                    ranked_results.append(
                        {
                            "relevance": llm.relevance(question, result),
                            "result": result
                        }
                    )
                ranked_results.sort(key=lambda result: result["relevance"], reverse=True)
                rr = ranked_results if len(ranked_results) <= self._max_results else ranked_results[:self._max_results]
                self._logger.info(f"Results for question '{question}': {rr}")
                answer = self._llm.ask(question, [ r["result"] for r in rr ])
                self._logger.info(f"Answer for question '{question}': {answer}")
                print(answer)
                question = input("Do you have another question to ask? ")
            return True

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python client.py source module_name class_name [ log_file [max_results]]")
        sys.exit(-1)
    source = sys.argv[1]
    module_name = sys.argv[2]
    class_name = sys.argv[3]
    log_file = sys.argv[4] if len(sys.argv) > 4 else None
    max_results = int(sys.argv[5]) if len(sys.argv) > 5 else 10

    if log_file:
        logging.basicConfig(filename=log_file, level=logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('hello_rag_world')

    if not module_name or not class_name:
        print("Module name and class name must be provided.")
        sys.exit(-1)
    if not os.path.exists(source):
        if module_name == "milvus_facade" and class_name == "MilvusFacade":
            index = DynamicFacade('indexer.empty_indexer', 'EmptyIndexer', logger).create(source)
        else:
            print("Source file or folder does not exist.")
            sys.exit(-1)
    elif os.path.isfile(source) and source.endswith('.pdf'):
        index = DynamicFacade('indexer.pdf_indexer', 'PDFIndexer', logger).create(source)
    elif os.path.isdir(source):
        index = DynamicFacade('indexer.folder_indexer', 'FolderIndexer', logger).create(source)
    else:
        print("Source must be a PDF file or a folder containing text files.")
        sys.exit(-1)
    search = DynamicFacade(module_name, class_name, logger).create(index)
    llm = DynamicFacade('llm.ollama_facade', 'OllamaFacade', logger).create("llama3.3")
    HelloRagClient(search, llm, logger, max_results).run()
