from pathlib import Path
import requests
import pandas as pd
from dev.pipeline.sources.api_source import APIDataSource
from dev.utils.logging import setup_pipeline_logging

def run_api_source_demo():
    """Demonstrate API data source functionality"""
    logger = setup_pipeline_logging(log_file=Path("logs/api_source_demo.log"))
    logger.info("Starting API source demo")
    
    # Configure API source
    api_config = {
        'base_url': 'https://api.example.com',
        'endpoint': '/equipment',
        'headers': {
            'Authorization': 'Bearer demo_token',
            'Content-Type': 'application/json'
        },
        'params': {
            'status': 'active',
            'limit': 100
        }
    }
    
    try:
        # Initialize API source
        source = APIDataSource(
            base_url=api_config['base_url'],
            endpoint=api_config['endpoint'],
            headers=api_config['headers'],
            params=api_config['params'],
            batch_size=100
        )
        
        print("\nProcessing API Data Source:")
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
            
        print("\nAPI Source Summary:")
        print(f"Total batches processed: {batch_num}")
        print(f"Total records processed: {total_records}")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}", exc_info=True)
        print(f"\nAPI request error: {e}")
    except Exception as e:
        logger.error(f"API source demo failed: {e}", exc_info=True)
        print(f"\nError processing API source: {e}")

if __name__ == "__main__":
    run_api_source_demo() 