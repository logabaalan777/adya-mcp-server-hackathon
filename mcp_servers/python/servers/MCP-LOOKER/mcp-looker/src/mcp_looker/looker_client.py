import httpx
import json
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

class LookerClient:
    def __init__(self):
        self.base_url = None
        self.client_id = None
        self.client_secret = None
        self.access_token = None
        self._initialized = False

    def initialize(self, base_url: str, client_id: str, client_secret: str):
        """Initialize the Looker client with credentials."""
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self._initialized = True

    def is_initialized(self) -> bool:
        """Check if the client has been initialized with credentials."""
        return self._initialized

    async def _get_access_token(self) -> Dict[str, Any]:
        """Get access token from Looker API."""
        if not self.is_initialized():
            raise ValueError("Looker client not initialized. Please provide base_url, client_id, and client_secret.")
        
        url = f"{self.base_url}/api/4.0/login"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            return {"success": True, "data": token_data}
        else:
            return {
                "success": False,
                "error": f"Failed to get access token: HTTP {response.status_code} - {response.text}"
            }

    def get_headers(self) -> Dict[str, str]:
        """Get the standard headers for API requests."""
        if not self.access_token:
            raise ValueError("No access token available. Please authenticate first.")
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    async def get_dashboards(self) -> Dict[str, Any]:
        """Get all dashboards from Looker."""
        if not self.access_token:
            auth_result = await self._get_access_token()
            if not auth_result["success"]:
                return auth_result

        url = f"{self.base_url}/api/4.0/dashboards"
        headers = self.get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {
                "success": False,
                "error": f"Failed to fetch dashboards: HTTP {response.status_code} - {response.text}"
            }

    async def get_looks(self) -> Dict[str, Any]:
        """Get all looks from Looker."""
        if not self.access_token:
            auth_result = await self._get_access_token()
            if not auth_result["success"]:
                return auth_result

        url = f"{self.base_url}/api/4.0/looks"
        headers = self.get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {
                "success": False,
                "error": f"Failed to fetch looks: HTTP {response.status_code} - {response.text}"
            }

    async def run_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Run a Looker query and return results."""
        if not self.access_token:
            auth_result = await self._get_access_token()
            if not auth_result["success"]:
                return auth_result

        url = f"{self.base_url}/api/4.0/queries"
        headers = self.get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=query, headers=headers)
        
        if response.status_code == 200:
            query_id = response.json().get("id")
            
            # Get query results
            results_url = f"{self.base_url}/api/4.0/queries/{query_id}/run/json"
            results_response = await client.get(results_url, headers=headers)
            
            if results_response.status_code == 200:
                return {"success": True, "data": results_response.json()}
            else:
                return {
                    "success": False,
                    "error": f"Failed to get query results: HTTP {results_response.status_code}"
                }
        else:
            return {
                "success": False,
                "error": f"Failed to run query: HTTP {response.status_code} - {response.text}"
            }

    async def get_models(self) -> Dict[str, Any]:
        """Get all data models from Looker."""
        if not self.access_token:
            auth_result = await self._get_access_token()
            if not auth_result["success"]:
                return auth_result

        url = f"{self.base_url}/api/4.0/models"
        headers = self.get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {
                "success": False,
                "error": f"Failed to fetch models: HTTP {response.status_code} - {response.text}"
            }

    async def get_explores(self, model_name: str) -> Dict[str, Any]:
        """Get explores for a specific model."""
        if not self.access_token:
            auth_result = await self._get_access_token()
            if not auth_result["success"]:
                return auth_result

        url = f"{self.base_url}/api/4.0/models/{model_name}/explores"
        headers = self.get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {
                "success": False,
                "error": f"Failed to fetch explores: HTTP {response.status_code} - {response.text}"
            }

    async def create_look(self, look_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new look in Looker."""
        if not self.access_token:
            auth_result = await self._get_access_token()
            if not auth_result["success"]:
                return auth_result

        url = f"{self.base_url}/api/4.0/looks"
        headers = self.get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=look_data, headers=headers)
        
        if response.status_code in (200, 201):
            return {"success": True, "data": response.json()}
        else:
            return {
                "success": False,
                "error": f"Failed to create look: HTTP {response.status_code} - {response.text}"
            }

    def format_query_results(self, results: List[Dict]) -> str:
        """Format query results as a readable string."""
        if not results:
            return "No results found."
        
        # Convert to DataFrame for better formatting
        df = pd.DataFrame(results)
        
        # Get basic statistics
        total_rows = len(df)
        total_cols = len(df.columns)
        
        # Format as table
        result_text = f"Query Results ({total_rows} rows, {total_cols} columns):\n"
        result_text += "=" * 50 + "\n"
        
        # Show first 10 rows
        if total_rows > 10:
            result_text += df.head(10).to_string(index=False)
            result_text += f"\n\n... and {total_rows - 10} more rows"
        else:
            result_text += df.to_string(index=False)
        
        return result_text

# Global instance
looker_client = LookerClient() 