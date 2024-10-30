from typing import Dict, Optional, Any
from .config import DeepLynxConfig

class PipelineConfig:
    """Configuration for ETL pipeline operations"""
    def __init__(self, base_config: DeepLynxConfig):
        self.client = base_config.get_api_client()
        self.batch_size: int = 1000  # Default batch size
        self.retry_attempts: int = 3
        self.retry_delay: int = 5  # seconds
        self.source_configs: Dict[str, Any] = {}
        
    def add_source_config(self, source_name: str, config: Dict[str, Any]) -> None:
        """Add configuration for a specific data source"""
        self.source_configs[source_name] = config 