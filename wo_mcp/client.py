import os
import sys
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
    def __init__(self, facade_module: str, facade_class: str):
        self.facade_module = facade_module
        self.facade_class = facade_class

    def create(self, ctor_arg = None):
        if '.' in self.facade_module:
            m = import_from_path(self.facade_module, f"../{self.facade_module.replace('.', '/')}.py")
        else:
            m = importlib.import_module(self.facade_module)
        c = getattr(m, self.facade_class)
        if ctor_arg is None:
            rv = c()
        else:
            rv = c(ctor_arg)
        return rv

class HelloRagClient:
    def __init__(self, search: SearchFacade, llm: LargeLanguageModelFacade, max_results: int = 10):
        self._search = search
        self._llm = llm
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
                print(self._llm.ask(question, [ r["result"] for r in rr ]))
                question = input(f"Do you have another question to ask? ")
            return True

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python client.py source module_name class_name [max_results]")
        sys.exit(-1)
    source = sys.argv[1]
    module_name = sys.argv[2]
    class_name = sys.argv[3]
    max_results = int(sys.argv[4]) if len(sys.argv) > 4 else 10

    if not module_name or not class_name:
        print("Module name and class name must be provided.")
        sys.exit(-1)
    if not os.path.exists(source):
        if module_name == "milvus_facade" and class_name == "MilvusFacade":
            index = DynamicFacade('empty_indexer', 'EmptyIndexer').create(source)
        else:
            print("Source file or folder does not exist.")
            sys.exit(-1)
    elif os.path.isfile(source) and source.endswith('.pdf'):
        index = DynamicFacade('indexer.pdf_indexer', 'PDFIndexer').create(source)
    elif os.path.isdir(source):
        index = DynamicFacade('indexer.folder_indexer', 'FolderIndexer').create(source)
    else:
        print("Source must be a PDF file or a folder containing text files.")
        sys.exit(-1)
    search = DynamicFacade(module_name, class_name).create(index)
    llm = DynamicFacade('llm.ollama_facade', 'OllamaFacade').create("llama3.3")
    HelloRagClient(search, llm, max_results).run()
