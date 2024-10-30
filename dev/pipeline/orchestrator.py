from typing import Optional
import logging
from pathlib import Path
from datetime import datetime

from .state import PipelineState, PipelineStatus
from .base import DataSource, DataTransformer, DataLoader
from ..utils.logging import setup_pipeline_logging

class PipelineOrchestrator:
    """Orchestrates the ETL pipeline flow"""
    def __init__(
        self,
        source: DataSource,
        transformer: DataTransformer,
        loader: DataLoader,
        log_file: Optional[Path] = None
    ):
        self.source = source
        self.transformer = transformer
        self.loader = loader
        self.logger = setup_pipeline_logging(log_file=log_file)
        self.state = PipelineState(status=PipelineStatus.INITIALIZED)
        
    async def execute(self) -> bool:
        """Execute the complete pipeline"""
        try:
            self.state.status = PipelineStatus.RUNNING
            self.state.start_time = datetime.now()
            self.logger.info("Starting pipeline execution")
            
            # Process each batch
            for batch in self.source.extract():
                # Transform data
                transformed_data = self.transformer.transform(batch)
                
                # Load data
                success = self.loader.load(transformed_data)
                if not success:
                    raise Exception("Failed to load batch")
                    
                self.state.records_processed += len(batch)
                self.logger.info(f"Processed batch of {len(batch)} records")
            
            # Complete pipeline
            self.state.status = PipelineStatus.COMPLETED
            self.state.end_time = datetime.now()
            self.logger.info("Pipeline execution completed successfully")
            return True
            
        except Exception as e:
            self.state.status = PipelineStatus.FAILED
            self.state.end_time = datetime.now()
            self.state.errors["pipeline_error"] = str(e)
            self.logger.error(f"Pipeline failed: {e}")
            return False 