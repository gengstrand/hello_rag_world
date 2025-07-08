import sys
from txtai import Embeddings
from mcp.server.fastmcp import FastMCP
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))
from indexer.pdf_indexer import PDFIndexer

mcp = FastMCP("pdf_search_txtai")
embeddings = Embeddings(hybrid=True, path="sentence-transformers/nli-mpnet-base-v2")
data = []

@mcp.tool()
def add_pages(pdf_file: str) -> str:
    global embeddings, data
    indexer = PDFIndexer(pdf_file)
    data = [ doc for doc in indexer.documents ]
    embeddings.index(data)
    return indexer.title

@mcp.tool()
def search(query: str, top_results: int, simularity: float) -> list[str]:
    global embeddings, data
    return [ data[index] for (index, score) in embeddings.search(query, top_results) if score > simularity ]

if __name__ == "__main__":
    mcp.run()
