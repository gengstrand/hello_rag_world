import sys
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters, types
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))
from llm.ollama_facade import OllamaFacade

async def run(pdf_file: str, mcp_server: str):
    server_params = StdioServerParameters(
        command="python", 
        args=[mcp_server], 
        env=None
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            await session.initialize()
            await session.list_tools()
            llm = OllamaFacade("llama:3.3")
            apr = await session.call_tool("add_pages", arguments={"pdf_file": pdf_file})
            if not apr.isError and len(apr.content) > 0:
                title = apr.content[0].text
                question = input(f"What do you want to know about {title}? ")
                while len(question) > 0:
                    sr = await session.call_tool("search", arguments={"query": question, "top_results": "10", "simularity": "0.1"})
                    if not sr.isError:
                        ranked_results = []
                        for r in sr.content:
                            ranked_results.append(
                                {
                                    "relevance": llm.relevance(question, r.text),
                                    "result": r.text
                                }
                            )
                        ranked_results.sort(key=lambda result: result["relevance"], reverse=True)
                        rr = ranked_results if len(ranked_results) <= 6 else ranked_results[:5]
                        print(llm.ask(question, [ r["result"] for r in rr ]))
                    else:
                        print("cannot search PDF")
                    question = input(f"Do you have another question to ask? ")
            else:
                print("cannot load PDF")

if __name__ == "__main__":
    import asyncio

    if len(sys.argv) < 3:
        print("usage: python client.py pdf_file mcp_server.py")
        sys.exit(-1)
    asyncio.run(run(sys.argv[1], sys.argv[2]))
