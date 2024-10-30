from pathlib import Path
import pandas as pd
from dev.pipeline.sources.csv_source import CSVDataSource
from dev.pipeline.transformers.base_transformer import DeepLynxTransformer
from dev.utils.logging import setup_pipeline_logging

def run_transformer_demo():
    """Demonstrate transformer functionality"""
    logger = setup_pipeline_logging()
    logger.info("Starting transformer demo")
    
    # Setup mapping configuration
    mapping_config = {
        "column_mappings": {
            "equipment_name": "name",
            "process_type": "type",
            "duration": "process_duration"
        },
        "type_conversions": {
            "process_duration": "int64"
        },
        "metadata": {
            "source": "manufacturing_data",
            "version": "1.0"
        }
    }
    
    try:
        # Initialize components
        source = CSVDataSource(
            Path("tests/data/sample_manufacturing_data.csv"), 
            batch_size=2
        )
        transformer = DeepLynxTransformer(mapping_config)
        
        # Process and transform data
        print("\nTransformation Results:")
        for batch_num, batch in enumerate(source.extract(), 1):
            print(f"\nBatch {batch_num} - Original Data:")
            print(batch)
            
            transformed_data = transformer.transform(batch)
            print(f"\nBatch {batch_num} - Transformed Data:")
            print(transformed_data)
            
            # Show mapping details
            print("\nColumn Mapping Details:")
            for orig_col, new_col in mapping_config["column_mappings"].items():
                print(f"{orig_col} -> {new_col}")
            
            print("\nData Type Conversions:")
            for col, dtype in mapping_config["type_conversions"].items():
                print(f"{col}: {dtype}")
                
    except Exception as e:
        logger.error(f"Transformer demo failed: {e}", exc_info=True)
        print("\nTransformer demo failed! Check logs for details.")

if __name__ == "__main__":
    run_transformer_demo() 