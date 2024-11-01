from pathlib import Path
from datetime import datetime
import time
import os
from dotenv import load_dotenv
from dev.pipeline.sources.csv_source import CSVDataSource
from dev.pipeline.state import PipelineState, PipelineStatus
from dev.pipeline_config import PipelineConfig
from dev.config import DeepLynxConfig
from dev.utils.logging import setup_pipeline_logging

def run_demo_pipeline():
    """Demonstrate basic pipeline functionality with the manufacturing data"""
    start_time = time.time()
    metrics = {
        "batch_times": [],
        "records_per_second": [],
        "memory_usage": [],
        "total_records": 0
    }
    
    # 1. Setup logging with more detail
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logger = setup_pipeline_logging(log_file=log_dir / "demo_pipeline.log")
    logger.info("Starting demo pipeline with enhanced metrics")

    # 2. Load and verify environment variables
    load_dotenv(override=True)
    env_vars = {
        'BASE_URL': os.getenv('BASE_URL', 'http://localhost:8090'),
        'API_KEY': os.getenv('API_KEY'),
        'API_SECRET': os.getenv('API_SECRET')
    }
    
    if not env_vars['API_KEY'] or not env_vars['API_SECRET']:
        error_msg = (
            "\nMissing API credentials. Please check your .env file:\n"
            "1. Ensure .env file exists in project root\n"
            "2. File should contain:\n"
            "   API_KEY=your_api_key\n"
            "   API_SECRET=your_api_secret\n"
            "   BASE_URL=http://localhost:8090 (optional)\n"
            f"\n3. Current values:\n"
            f"   BASE_URL: {env_vars['BASE_URL']}\n"
            f"   API_KEY: {'[SET]' if env_vars['API_KEY'] else '[MISSING]'}\n"
            f"   API_SECRET: {'[SET]' if env_vars['API_SECRET'] else '[MISSING]'}"
        )
        logger.error("Missing API credentials")
        print(error_msg)
        return

    # 3. Initialize configuration with credentials
    base_config = DeepLynxConfig(
        base_url=env_vars['BASE_URL'],
        api_key=env_vars['API_KEY'],
        api_secret=env_vars['API_SECRET']
    )
    pipeline_config = PipelineConfig(base_config)
    logger.info(f"Pipeline configured with batch size: {pipeline_config.batch_size}")
    
    # 4. Initialize pipeline state
    state = PipelineState(status=PipelineStatus.INITIALIZED)
    logger.info(f"Pipeline initialized with state: {state.status}")

    try:
        # 5. Configure CSV source
        csv_path = Path("tests/data/sample_manufacturing_data.csv")
        source = CSVDataSource(csv_path, batch_size=2)  # Small batch size for demo
        logger.info(f"Configured CSV source: {csv_path}")

        # 6. Process data with metrics
        state.status = PipelineStatus.RUNNING
        state.start_time = datetime.now()
        
        logger.info("Beginning data processing...")
        for batch_num, batch in enumerate(source.extract(), 1):
            batch_start = time.time()
            
            # Log batch details
            logger.info(f"Processing batch {batch_num} with {len(batch)} records")
            logger.debug(f"Batch columns: {batch.columns.tolist()}")
            logger.debug(f"Sample data: {batch.iloc[0].to_dict()}")
            
            # Update state and collect metrics
            state.records_processed += len(batch)
            batch_time = time.time() - batch_start
            records_per_second = len(batch) / batch_time if batch_time > 0 else 0
            
            # Store metrics
            metrics["batch_times"].append(batch_time)
            metrics["records_per_second"].append(records_per_second)
            metrics["total_records"] = state.records_processed
            
            logger.info(f"Batch {batch_num} processed in {batch_time:.2f} seconds")
            logger.info(f"Processing rate: {records_per_second:.2f} records/second")
            
        # 7. Complete pipeline
        state.status = PipelineStatus.COMPLETED
        state.end_time = datetime.now()
        total_time = time.time() - start_time
        
        # 8. Display detailed results
        print("\nPipeline Execution Summary:")
        print(f"Status: {state.status}")
        print(f"Records Processed: {state.records_processed}")
        print(f"Total Duration: {total_time:.2f} seconds")
        print(f"Average Processing Rate: {state.records_processed/total_time:.2f} records/second")
        print(f"Number of Batches: {len(metrics['batch_times'])}")
        print(f"Average Batch Time: {sum(metrics['batch_times'])/len(metrics['batch_times']):.2f} seconds")
        print(f"Errors: {len(state.errors)}")
        
        logger.info("Pipeline execution completed successfully")
        
    except Exception as e:
        state.status = PipelineStatus.FAILED
        state.errors["pipeline_error"] = str(e)
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        print("\nPipeline failed! Check logs for details.")

if __name__ == "__main__":
    run_demo_pipeline() 