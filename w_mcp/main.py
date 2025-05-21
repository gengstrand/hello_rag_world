from pypdf import PdfReader
from txtai import Embeddings
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pdf_search")
embeddings = Embeddings(hybrid=True, path="sentence-transformers/nli-mpnet-base-v2")
data = []

@mcp.tool()
def add_pages(pdf_file: str) -> str:
    global embeddings, data
    reader = PdfReader(pdf_file)
    metadata = reader.metadata
    rv = pdf_file
    if metadata and '/Title' in metadata:
        rv = metadata['/Title']
    data = [ page.extract_text().replace('\n', ' ') for page in reader.pages ]
    embeddings.index(data)
    return rv

@mcp.tool()
def search(query: str, top_results: int, simularity: float) -> list[str]:
    global embeddings, data
    return [ data[index] for (index, score) in embeddings.search(query, top_results) if score > simularity ]

if __name__ == "__main__":
    mcp.run()
