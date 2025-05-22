import sys
from typing import cast
from search_facade import SearchFacade
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))
from llm.ollama_facade import OllamaFacade

def run(pdf_file: str, search_facade_module: str, facade_class_name: str):
    m = __import__(search_facade_module)
    c = getattr(m, facade_class_name)
    o = c()
    f = cast(SearchFacade, o)
    llm = OllamaFacade("llama:3.3")
    title = f.add_pages(pdf_file)
    question = input(f"What do you want to know about {title}? ")
    while len(question) > 0:
        results = f.search(question, 10, 0.1)
        ranked_results = []
        for result in results:
            ranked_results.append(
                {
                    "relevance": llm.relevance(question, result),
                    "result": result
                }
            )
        ranked_results.sort(key=lambda result: result["relevance"], reverse=True)
        rr = ranked_results if len(ranked_results) <= 6 else ranked_results[:5]
        print(llm.ask(question, [ r["result"] for r in rr ]))
        question = input(f"Do you have another question to ask? ")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python client.py pdf_file module_name class_name")
        sys.exit(-1)
    run(sys.argv[1], sys.argv[2], sys.argv[3])
