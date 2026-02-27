# Supernova Connector 🚀

The official Python client for [Supernova.cool](https://supernova.cool) — the Universal Agent Tool Platform.

## 📦 Installation

```bash
pip install supernova-connector
```

## 🚀 Quick Start

```python
from supernova_connector import SupernovaClient
import asyncio

async def main():
    # Initialize client
    client = SupernovaClient()

    # 1. Semantic Search for Tools
    tools = await client.search_tools("I need to scrape real estate data from Zillow")
    print(f"Found Tool: {tools[0]['name']}")

    # 2. Execute via Secure Proxy
    result = await client.execute_tool(
        tool_id=tools[0]['tool_id'],
        payload={"url": "https://zillow.com/..."}
    )
    print(result['data'])

if __name__ == "__main__":
    asyncio.run(main())
```

## 🌌 Features
- **Semantic Routing**: Powered by Gemini 1.5 Flash.
- **A2A Native**: Built for the agent-to-agent economy.
- **Secure Proxy**: Integrated rate-limiting and secret management.
