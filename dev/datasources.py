from typing import Optional, Dict
from deep_lynx import (
    DataSourcesApi,  # For defining data sources
    GraphApi,        # For data relationships
    CreateDataSourceRequest,
    CreateOrUpdateNodesRequest,
    CreateOrUpdateEdgesRequest
)

class DataSourceAPI:
    def __init__(self):
        self.client = DeepLynxClient()
        
    def create_data_source(self, container_id: str, name: str) -> Optional[str]:
        """Create a data source for importing data"""
        try:
            response = self.client.datasources_api.create_data_source(
                container_id=container_id,
                body=CreateDataSourceRequest(
                    name=name,
                    adapter_type="standard",  # or "file", "timeseries" etc.
                    active=True
                )
            )
            return str(response.value.id) if response.value else None
            
    async def import_data(self, container_id: str, datasource_id: str, data: Dict):
        """Import data into Deep Lynx"""
        try:
            return await self.client.datasources_api.create_manual_import(
                data=data,
                container_id=container_id,
                datasource_id=datasource_id
            ) 