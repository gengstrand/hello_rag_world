# hello_rag_world

the hello world of RAG pipelines

I did this as an exploration into what impact MCP has on RAG pipeline complexity. The w_mcp folder uses MCP and the wo_mcp folder provides the same functionality without MCP. Like any other hello world program, the code here is very simple for illustratic purposes so this is not production ready.

I tested this on a Google Cloud VM with an NVIDIA A100 40GB and an a2-highgpu-1g (12 vCPU, 6 core, 85 GB memory) and an 80 GB drive. I used the Deep learning VM M129 OS and opted for the CUDA installation.

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.3
git clone https://github.com/gengstrand/hello_rag_world.git
cd hello_rag_world
curl --output st1.pdf https://dn720001.ca.archive.org/0/items/star-trek-by-james-blish/Star%20Trek%2001%20-%20James%20Blish.pdf
python -m venv rag
sh rag/bin/activate
rag/bin/pip install pypdf
rag/bin/pip install txtai
rag/bin/pip install pymilvus
rag/bin/pip install mcp
rag/bin/pip install langchain-ollama
rag/bin/pip install sentence-transformers
rag/bin/pip install flair
rag/bin/pip install nltk
cd w_mcp
../rag/bin/python client.py ../st1.pdf txtai_server.py
Who was Nancy to Dr. McCoy?

cd ../wo_mcp
../rag/bin/python client_test.py
../rag/bin/python client.py ../st1.pdf txtai_facade TxtAiFacade
Where did Yeoman Rand first meet Charlie?

../rag/bin/python client.py ../st1.pdf milvus_facade MilvusFacade
Is Miri older than Kirk or younger?

```

The question loop continues until you hit the return key without typing in any more questions.

