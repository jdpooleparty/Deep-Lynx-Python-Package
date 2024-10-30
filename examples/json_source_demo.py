from pathlib import Path
import json
import pandas as pd
from dev.pipeline.sources.json_source import JSONDataSource
from dev.utils.logging import setup_pipeline_logging

def run_json_source_demo():
    """Demonstrate JSON data source functionality"""
    logger = setup_pipeline_logging(log_file=Path("logs/json_source_demo.log"))
    logger.info("Starting JSON source demo")
    
    # Create sample JSON data
    sample_data = {
        "equipment": [
            {
                "id": f"EQ{i:03d}",
                "name": f"Machine_{i}",
                "process_type": "Machining" if i % 2 == 0 else "Assembly",
                "duration": i * 100,
                "status": "active"
            }
            for i in range(1, 101)
        ]
    }
    
    # Save sample data
    json_path = Path("tests/data/sample_manufacturing.json")
    json_path.parent.mkdir(exist_ok=True)
    json_path.write_text(json.dumps(sample_data, indent=2))
    
    try:
        # Initialize JSON source
        source = JSONDataSource(
            file_path=json_path,
            root_element="equipment",
            batch_size=20
        )
        
        print("\nProcessing JSON Data Source:")
        print("-" * 50)
        
        # Process data in batches
        total_records = 0
        for batch_num, batch in enumerate(source.extract(), 1):
            total_records += len(batch)
            
            print(f"\nBatch {batch_num}:")
            print(f"Records in batch: {len(batch)}")
            print("\nSample data:")
            print(batch.head(2))
            
            # Add processing metrics
            logger.info(f"Processed batch {batch_num} with {len(batch)} records")
            
        print("\nJSON Source Summary:")
        print(f"Total batches processed: {batch_num}")
        print(f"Total records processed: {total_records}")
        
    except Exception as e:
        logger.error(f"JSON source demo failed: {e}", exc_info=True)
        print(f"\nError processing JSON source: {e}")

if __name__ == "__main__":
    run_json_source_demo() 