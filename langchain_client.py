from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="learnlm-2.0-flash-experimental", google_api_key=os.getenv("GEMINI_API_KEY")
)


async def main():
    async with MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [
                    "/Users/balajivenktesh/Desktop/Education/mcp-servers/mcp-crash-course/servers/math_server.py"
                ],
                "transport": "stdio",
            },
            "weather": {
                # make sure you start your weather server on port 8000
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    ) as client:
        agent = create_react_agent(llm, client.get_tools())
        math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
        weather_response = await agent.ainvoke(
            {"messages": "what is the weather in nyc?"}
        )


if __name__ == "__main__":
    asyncio.run(main())
