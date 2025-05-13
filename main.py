import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
#print(os.getenv("GEMINI_API_KEY"))

async def main():
    print("Hello from mcp-crash-course!")


if __name__ == "__main__":
    asyncio.run(main())
