from typing import Dict, Optional, Any
from deep_lynx import (
    Configuration, 
    ApiClient,
    DataSourcesApi,
    ContainersApi,
    MetatypesApi
)
from .config import DeepLynxConfig

class PipelineConfig:
    """Configuration for ETL pipeline operations"""
    def __init__(self, base_config: DeepLynxConfig):
        self.api_client = base_config.get_api_client()
        self.batch_size: int = 1000
        self.retry_attempts: int = 3
        self.retry_delay: int = 5
        self.source_configs: Dict[str, Any] = {}
        
        # Initialize Deep Lynx APIs
        self._datasources_api = DataSourcesApi(self.api_client)
        self._containers_api = ContainersApi(self.api_client)
        self._metatypes_api = MetatypesApi(self.api_client)

    def get_datasources_api(self) -> DataSourcesApi:
        """Get Deep Lynx Data Sources API instance"""
        return self._datasources_api

    def get_containers_api(self) -> ContainersApi:
        """Get Deep Lynx Containers API instance"""
        return self._containers_api

    def get_metatypes_api(self) -> MetatypesApi:
        """Get Deep Lynx Metatypes API instance"""
        return self._metatypes_api