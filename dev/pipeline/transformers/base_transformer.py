from typing import Dict, Any
import pandas as pd
from ..base import DataTransformer

class DeepLynxTransformer(DataTransformer):
    """Base transformer for mapping data to Deep Lynx schema"""
    def __init__(self, mapping_config: Dict[str, Any]):
        self.mapping_config = mapping_config
        
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform data according to mapping configuration"""
        transformed_data = data.copy()
        
        # Apply column mappings first
        if 'column_mappings' in self.mapping_config:
            transformed_data = transformed_data.rename(
                columns=self.mapping_config['column_mappings']
            )
        
        # Apply data type conversions to the renamed columns
        if 'type_conversions' in self.mapping_config:
            for source_col, dtype in self.mapping_config['type_conversions'].items():
                # Get the new column name if it was mapped, otherwise use original
                target_col = self.mapping_config['column_mappings'].get(source_col, source_col)
                if target_col in transformed_data.columns:
                    transformed_data[target_col] = transformed_data[target_col].astype(dtype)
        
        # Add metadata columns
        if 'metadata' in self.mapping_config:
            for meta_key, meta_value in self.mapping_config['metadata'].items():
                transformed_data[meta_key] = meta_value
                
        return transformed_data