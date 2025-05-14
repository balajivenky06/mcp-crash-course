import asyncio
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

llm = ChatGoogleGenerativeAI(model="learnlm-2.0-flash-experimental",
google_api_key=os.getenv("GEMINI_API_KEY"))

stdio_server_params = StdioServerParameters(
    command="python", 
    args = ["/Users/balajivenktesh/Desktop/Education/mcp-servers/mcp-crash-course/servers/math_server.py"],
)

async def main():
    #print("Hello from mcp-crash-course!")
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("session initialized")
            tools = await load_mcp_tools(session)
            #print(tools)
            # Create and run the agent
            agent = create_react_agent(llm, tools)
            agent_response = await agent.ainvoke({"messages": [HumanMessage(content="calculate ((3 + 5) / 12 )?")]})
            print(agent_response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
