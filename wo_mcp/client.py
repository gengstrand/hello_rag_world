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
    def __init__(self, search: SearchFacade, llm: LargeLanguageModelFacade):
        self._search = search
        self._llm = llm

    def run(self, test_mode: bool = False) -> bool:
        title = self._search.add_pages()
        if test_mode:
            results = self._search.search("test", 10, 0.1)
            return len(results) > 0
        else:
            question = input(f"What do you want to know about {title}? ")
            while len(question) > 0:
                results = self._search.search(question, 10, 0.1)
                ranked_results = []
                for result in results:
                    ranked_results.append(
                        {
                            "relevance": llm.relevance(question, result),
                            "result": result
                        }
                    )
                ranked_results.sort(key=lambda result: result["relevance"], reverse=True)
                rr = ranked_results if len(ranked_results) <= 5 else ranked_results[:5]
                print(self._llm.ask(question, [ r["result"] for r in rr ]))
                question = input(f"Do you have another question to ask? ")
            return True

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python client.py pdf_file module_name class_name")
        sys.exit(-1)
    pdf_file = sys.argv[1]
    index = DynamicFacade('indexer.pdf_indexer', 'PDFIndexer').create(pdf_file)
    search = DynamicFacade(sys.argv[2], sys.argv[3]).create(index)
    llm = DynamicFacade('llm.ollama_facade', 'OllamaFacade').create("llama3.3")
    HelloRagClient(search, llm).run()
