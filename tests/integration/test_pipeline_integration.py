import pytest
import asyncio
from pathlib import Path
from dev.pipeline.sources.csv_source import CSVDataSource
from dev.pipeline.state import PipelineState, PipelineStatus
from dev.pipeline_config import PipelineConfig
from dev.utils.logging import setup_pipeline_logging

@pytest.mark.asyncio
async def test_complete_pipeline_flow(
    mock_pipeline_config: PipelineConfig,
    sample_csv: Path,
    tmp_path: Path
):
    """Test complete pipeline flow with all components"""
    # Setup logging
    log_file = tmp_path / "pipeline.log"
    logger = setup_pipeline_logging(log_file=log_file)
    
    # Initialize pipeline state
    state = PipelineState(status=PipelineStatus.INITIALIZED)
    
    try:
        # Start pipeline
        state.status = PipelineStatus.RUNNING
        logger.info("Starting pipeline execution")
        
        # Initialize source
        source = CSVDataSource(sample_csv, batch_size=100)
        
        # Process batches
        for batch in source.extract():
            state.records_processed += len(batch)
            logger.info(f"Processed batch of {len(batch)} records")
            
            # Simulate some processing time
            await asyncio.sleep(0.1)
        
        # Complete pipeline
        state.status = PipelineStatus.COMPLETED
        logger.info("Pipeline execution completed successfully")
        
    except Exception as e:
        state.status = PipelineStatus.FAILED
        state.errors["pipeline_error"] = str(e)
        logger.error(f"Pipeline failed: {e}")
        raise
    
    # Verify results
    assert state.status == PipelineStatus.COMPLETED
    assert state.records_processed > 0
    assert state.errors == {} 