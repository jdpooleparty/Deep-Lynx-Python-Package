from typing import Optional
import logging
import asyncio
from datetime import datetime
from .state import PipelineState, PipelineStatus
from .base import DataSource, DataTransformer, DataLoader

logger = logging.getLogger('deep_lynx_pipeline')

class PipelineOrchestrator:
    """Orchestrate pipeline execution"""
    def __init__(
        self,
        source: DataSource,
        transformer: DataTransformer,
        loader: DataLoader,
        state: PipelineState
    ):
        self.source = source
        self.transformer = transformer
        self.loader = loader
        self.state = state

    async def run(self) -> bool:
        """Run the complete pipeline"""
        try:
            self.state.status = PipelineStatus.RUNNING
            self.state.start_time = datetime.now()

            for batch in self.source.extract():
                transformed_data = self.transformer.transform(batch)
                success = await self.loader.load(transformed_data)
                
                if not success:
                    logger.error("Failed to load batch")
                    raise Exception("Failed to load batch")
                
                self.state.records_processed += len(batch)
                logger.info(f"Processed batch of {len(batch)} records")

            self.state.status = PipelineStatus.COMPLETED
            self.state.end_time = datetime.now()
            logger.info("Pipeline execution completed successfully")
            return True

        except Exception as e:
            self.state.status = PipelineStatus.FAILED
            self.state.errors["pipeline_error"] = str(e)
            logger.error(f"Pipeline failed: {e}")
            raise