from typing import Generator, Dict, Any
import requests
import pandas as pd
from ..base import DataSource
import logging

logger = logging.getLogger('deep_lynx_pipeline')

class APIDataSource(DataSource):
    """API data source implementation"""
    def __init__(
        self, 
        base_url: str, 
        endpoint: str, 
        headers: Dict[str, str] = None,
        params: Dict[str, Any] = None,
        batch_size: int = 1000
    ):
        self.base_url = base_url.rstrip('/')
        self.endpoint = endpoint.lstrip('/')
        self.headers = headers or {}
        self.params = params or {}
        self.batch_size = batch_size
        
    def _make_request(self) -> Dict[str, Any]:
        """Make HTTP request to API endpoint"""
        url = f"{self.base_url}/{self.endpoint}"
        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=self.params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
            
    def extract(self) -> Generator[pd.DataFrame, None, None]:
        """Extract data from API in batches"""
        try:
            # Get data from API
            data = self._make_request()
            
            # Convert to DataFrame
            if isinstance(data, dict):
                # Handle nested data structure
                for key in data:
                    if isinstance(data[key], list):
                        data = data[key]
                        break
            
            if not isinstance(data, list):
                raise ValueError("API response must contain a list of records")
                
            df = pd.DataFrame(data)
            
            # Process in batches
            for i in range(0, len(df), self.batch_size):
                batch = df.iloc[i:i + self.batch_size].copy()
                logger.info(f"Extracted batch of {len(batch)} records")
                yield batch
                
        except Exception as e:
            logger.error(f"Data extraction failed: {e}")
            raise 