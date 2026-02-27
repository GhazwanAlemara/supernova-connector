import httpx
from typing import List, Dict, Any, Optional

class SupernovaClient:
    """
    Official Python Connector for Supernova.cool
    The Universal Agent Tool Platform.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://supernova.cool"):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "X-Agent-ID": "supernova-python-client-v1"
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    async def search_tools(self, intent: str) -> List[Dict[str, Any]]:
        """Find the best tool for a given natural language intent."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/discovery/search",
                json={"intent": intent},
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def execute_tool(self, tool_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool via the Supernova Secure Proxy."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/execution/proxy/{tool_id}",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def list_registry(self) -> List[Dict[str, Any]]:
        """Retrieve the full list of available tools in the registry."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/discovery/list",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
