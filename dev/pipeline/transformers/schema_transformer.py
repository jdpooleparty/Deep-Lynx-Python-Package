from typing import Dict, Any, Optional
import pandas as pd
from .base_transformer import DeepLynxTransformer
from ..validators.schema_validator import SchemaValidator

class SchemaTransformer(DeepLynxTransformer):
    """Transformer with schema validation"""
    def __init__(
        self,
        mapping_config: Dict[str, Any],
        schema_validator: SchemaValidator,
        metatype: str
    ):
        super().__init__(mapping_config)
        self.schema_validator = schema_validator
        self.metatype = metatype
        
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform and validate data"""
        # First apply basic transformations
        transformed_data = super().transform(data)
        
        # Validate against schema
        validation_errors = self.schema_validator.validate_dataframe(
            transformed_data,
            self.metatype
        )
        
        if validation_errors:
            raise ValueError(
                f"Schema validation failed: {validation_errors}"
            )
            
        return transformed_data 