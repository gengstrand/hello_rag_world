# hello_rag_world
the hello world of RAG pipelines


```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.3
git clone https://github.com/gengstrand/hello_rag_world.git
cd hello_rag_world
curl --output csharp-vs-kotlin.pdf https://glennengstrand.info/assets/media/csharp-vs-kotlin.pdf
cd w_mcp
pip install -r requirements.txt
python client.py ../csharp-vs-kotlin.pdf milvus_server
# ask questions about the PDF. Hit enter by itself to exit the question loop.
cd ../wo_mcp
python client.py ../csharp-vs-kotlin.pdf milvus_facade MilvusFacade
```