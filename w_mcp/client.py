import sys
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters, types

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python", 
    args=["main.py"], 
    env=None
)

async def run(pdf_file: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            await session.initialize()
            await session.list_tools()
            apr = await session.call_tool("add_pages", arguments={"pdf_file": pdf_file})
            if not apr.isError and len(apr.content) > 0:
                title = apr.content[0].text
                question = input(f"What do you want to know about {title}? ")
                while len(question) > 0:
                    sr = await session.call_tool("search", arguments={"query": question, "top_results": "10", "simularity": "0.1"})
                    if not sr.isError:
                        for r in sr.content:
                            print(r.text + '\n\n')
                    else:
                        print("cannot search PDF")
                    question = input(f"Do you have another question to ask? ")
            else:
                print("cannot load PDF")

if __name__ == "__main__":
    import asyncio

    if len(sys.argv) < 2:
        print("usage: python client.py pdf_file")
        sys.exit(-1)
    asyncio.run(run(sys.argv[1]))
