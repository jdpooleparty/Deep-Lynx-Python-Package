from typing import Optional
from deep_lynx import (
    ContainersApi,
    MetatypesApi,
    MetatypeRelationshipsApi
)
from .config import DeepLynxConfig

class DeepLynxClient:
    """Client class for Deep Lynx API interactions"""
    def __init__(self):
        self.config = DeepLynxConfig()
        self._api_client = self.config.get_api_client()
        
        # Initialize all required APIs
        self.containers_api = ContainersApi(self._api_client)
        self.metatypes_api = MetatypesApi(self._api_client)
        self.relationships_api = MetatypeRelationshipsApi(self._api_client)