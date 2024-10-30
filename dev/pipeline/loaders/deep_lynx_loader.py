from typing import Dict, Any, List
import pandas as pd
from ..base import DataLoader
from ...pipeline_config import PipelineConfig
import asyncio
import logging

logger = logging.getLogger('deep_lynx_pipeline')

class DeepLynxLoader(DataLoader):
    """Loader for inserting data into Deep Lynx"""
    def __init__(
        self,
        config: PipelineConfig,
        container_id: str,
        data_source_id: str,
        batch_size: int = 100,
        retry_attempts: int = 3
    ):
        self.config = config
        self.container_id = container_id
        self.data_source_id = data_source_id
        self.batch_size = batch_size
        self.retry_attempts = retry_attempts
        self.datasources_api = config.get_datasources_api()

    async def load(self, data: pd.DataFrame) -> bool:
        """Load transformed data into Deep Lynx"""
        try:
            # Convert DataFrame to Deep Lynx import format
            import_data = {
                "data": {
                    "nodes": [
                        {
                            "metatype": row.get('metatype', 'default_type'),
                            "properties": {k: v for k, v in row.items() if k != 'metatype'}
                        } for _, row in data.iterrows()
                    ],
                    "edges": []
                }
            }

            # Attempt to create manual import with retry logic
            for attempt in range(self.retry_attempts):
                try:
                    response = self.datasources_api.create_manual_import(
                        container_id=self.container_id,
                        data_source_id=self.data_source_id,
                        body=import_data
                    )
                    
                    # Check for successful response
                    if (
                        isinstance(response, dict) and
                        'value' in response and
                        isinstance(response['value'], dict) and
                        response['value'].get('status', '') in ['ready', 'queued', 'processing']
                    ):
                        logger.info(f"Successfully queued batch of {len(data)} records for import")
                        return True
                    
                    logger.warning(f"Import attempt {attempt + 1} returned unexpected response: {response}")
                    if attempt < self.retry_attempts - 1:
                        await asyncio.sleep(1 * (attempt + 1))
                        
                except Exception as e:
                    if attempt < self.retry_attempts - 1:
                        logger.warning(f"Load attempt {attempt + 1} failed: {e}")
                        await asyncio.sleep(1 * (attempt + 1))
                    else:
                        raise Exception(f"Failed to load batch after {self.retry_attempts} attempts: {e}")
            
            return False
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise