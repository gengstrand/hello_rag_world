import sys
from typing import cast
from search_facade import SearchFacade

def run(pdf_file: str, search_facade_module: str, facade_class_name: str):
    m = __import__(search_facade_module)
    c = getattr(m, facade_class_name)
    o = c()
    f = cast(SearchFacade, o)
    title = f.add_pages(pdf_file)
    question = input(f"What do you want to know about {title}? ")
    while len(question) > 0:
        results = f.search(question, 10, 0.1)
        for result in results:
            print(result + '\n\n')
        question = input(f"Do you have another question to ask? ")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python client.py pdf_file module_name class_name")
        sys.exit(-1)
    run(sys.argv[1], sys.argv[2], sys.argv[3])
