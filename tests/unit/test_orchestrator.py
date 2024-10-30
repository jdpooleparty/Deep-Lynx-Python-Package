import pytest
from unittest.mock import Mock, patch
import pandas as pd
from pathlib import Path
from dev.pipeline.orchestrator import PipelineOrchestrator
from dev.pipeline.state import PipelineStatus

@pytest.fixture
def mock_components():
    """Create mock pipeline components"""
    source = Mock()
    transformer = Mock()
    loader = Mock()
    
    # Configure source to return two batches
    source.extract.return_value = [
        pd.DataFrame({"data": range(5)}),
        pd.DataFrame({"data": range(5, 10)})
    ]
    
    # Configure transformer to return same data
    transformer.transform.side_effect = lambda x: x
    
    # Configure loader to succeed
    loader.load.return_value = True
    
    return source, transformer, loader

@pytest.mark.asyncio
async def test_successful_pipeline_execution(mock_components, tmp_path):
    """Test successful pipeline execution"""
    source, transformer, loader = mock_components
    log_file = tmp_path / "pipeline.log"
    
    orchestrator = PipelineOrchestrator(
        source=source,
        transformer=transformer,
        loader=loader,
        log_file=log_file
    )
    
    success = await orchestrator.execute()
    
    assert success is True
    assert orchestrator.state.status == PipelineStatus.COMPLETED
    assert orchestrator.state.records_processed == 10
    assert len(orchestrator.state.errors) == 0
    
    # Verify component calls
    assert source.extract.called
    assert transformer.transform.call_count == 2
    assert loader.load.call_count == 2

@pytest.mark.asyncio
async def test_pipeline_failure_handling(mock_components, tmp_path):
    """Test pipeline failure handling"""
    source, transformer, loader = mock_components
    log_file = tmp_path / "pipeline.log"
    
    # Configure loader to fail
    loader.load.return_value = False
    
    orchestrator = PipelineOrchestrator(
        source=source,
        transformer=transformer,
        loader=loader,
        log_file=log_file
    )
    
    success = await orchestrator.execute()
    
    assert success is False
    assert orchestrator.state.status == PipelineStatus.FAILED
    assert "pipeline_error" in orchestrator.state.errors

@pytest.mark.asyncio
async def test_pipeline_state_tracking(mock_components, tmp_path):
    """Test pipeline state tracking"""
    source, transformer, loader = mock_components
    log_file = tmp_path / "pipeline.log"
    
    orchestrator = PipelineOrchestrator(
        source=source,
        transformer=transformer,
        loader=loader,
        log_file=log_file
    )
    
    await orchestrator.execute()
    
    assert orchestrator.state.start_time is not None
    assert orchestrator.state.end_time is not None
    assert orchestrator.state.records_processed == 10 