from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from dev.pipeline.sources.sql_source import SQLDataSource
from dev.pipeline.state import PipelineState, PipelineStatus
from dev.utils.logging import setup_pipeline_logging

def run_sql_source_demo():
    """Demonstrate SQL data source functionality"""
    logger = setup_pipeline_logging(log_file=Path("logs/sql_source_demo.log"))
    logger.info("Starting SQL source demo")
    
    # Setup demo database connection
    engine = create_engine('sqlite:///tests/data/sample_manufacturing.db')
    
    # Create sample data in SQLite
    sample_data = pd.DataFrame({
        'equipment_id': range(1, 1001),
        'equipment_name': [f'Machine_{i}' for i in range(1, 1001)],
        'process_type': ['Machining'] * 500 + ['Assembly'] * 500,
        'duration': range(100, 1100),
        'status': ['active'] * 800 + ['maintenance'] * 200
    })
    
    # Save to SQLite for demo
    sample_data.to_sql('equipment', engine, if_exists='replace', index=False)
    
    try:
        # Initialize SQL source
        source = SQLDataSource(
            connection_string='sqlite:///tests/data/sample_manufacturing.db',
            query="SELECT * FROM equipment WHERE status = 'active'",
            batch_size=100
        )
        
        print("\nProcessing SQL Data Source:")
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
            
        print("\nSQL Source Summary:")
        print(f"Total batches processed: {batch_num}")
        print(f"Total records processed: {total_records}")
        
    except Exception as e:
        logger.error(f"SQL source demo failed: {e}", exc_info=True)
        print(f"\nError processing SQL source: {e}")

if __name__ == "__main__":
    run_sql_source_demo() 