from typing import Dict, Any, List
import pandas as pd
from ..base import DataLoader
from ...pipeline_config import PipelineConfig

class DeepLynxLoader(DataLoader):
    """Loader for inserting data into Deep Lynx"""
    def __init__(self, config: PipelineConfig, container_id: str):
        self.client = config.client
        self.container_id = container_id
        self.batch_size = config.batch_size
        self.retry_attempts = config.retry_attempts
        
    def load(self, data: pd.DataFrame) -> bool:
        """Load transformed data into Deep Lynx"""
        try:
            # Convert DataFrame to list of dictionaries
            records = data.to_dict('records')
            
            # Split into batches
            batches = [
                records[i:i + self.batch_size] 
                for i in range(0, len(records), self.batch_size)
            ]
            
            # Process each batch
            for batch in batches:
                self._process_batch(batch)
                
            return True
            
        except Exception as e:
            # Log error and return False to indicate failure
            print(f"Error loading data: {str(e)}")
            return False
            
    def _process_batch(self, batch: List[Dict[str, Any]]) -> None:
        """Process a single batch of records"""
        for attempt in range(self.retry_attempts):
            try:
                # Create nodes in Deep Lynx
                response = self.client.create_data_nodes(
                    self.container_id,
                    batch
                )
                
                if response.is_success():
                    break
                    
            except Exception as e:
                if attempt == self.retry_attempts - 1:
                    raise Exception(f"Failed to load batch after {self.retry_attempts} attempts: {str(e)}") 