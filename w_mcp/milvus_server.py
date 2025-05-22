from pypdf import PdfReader
from pymilvus import MilvusClient
from mcp.server.fastmcp import FastMCP
from sentence_transformers import SentenceTransformer

db_name = "./milvus_pdf.db"
collection_name = "doc_pages"
mcp = FastMCP("pdf_search_milvus")
client = MilvusClient(db_name)
if client.has_collection(collection_name):
    client.drop_collection(collection_name)
client.create_collection(
    collection_name=collection_name,
    dimension=768,
    metric_type="IP",
    consistency_level="Strong"
)
model_id = "sentence-transformers/all-distilroberta-v1"
model = SentenceTransformer(model_id)

@mcp.tool()
def add_pages(pdf_file: str) -> str:
    global client, collection_name, model
    reader = PdfReader(pdf_file)
    metadata = reader.metadata
    rv = pdf_file
    if metadata and '/Title' in metadata:
        rv = metadata['/Title']
    data = []
    pn = 1
    for page in reader.pages:
        p = page.extract_text().replace('\n', ' ')
        data.append({"id": pn, "vector": model.encode(p), "text": p})
        pn += 1
    client.insert(collection_name=collection_name, data=data)
    return rv

@mcp.tool()
def search(query: str, top_results: int, simularity: float) -> list[str]:
    global client, collection_name, model
    results = client.search(
        collection_name=collection_name,
        data=[model.encode(query)],
        limit=top_results,
        search_params={"metric_type": "IP", "params": {}},
        output_fields=["text"]
    )
    return [ res["entity"]["text"] for res in results[0] if res["distance"] > simularity ]

if __name__ == "__main__":
    mcp.run()
