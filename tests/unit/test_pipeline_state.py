import pytest
from datetime import datetime
from dev.pipeline.state import PipelineState, PipelineStatus

def test_pipeline_state_initialization():
    """Test PipelineState initialization and defaults"""
    state = PipelineState(status=PipelineStatus.INITIALIZED)
    
    assert state.status == PipelineStatus.INITIALIZED
    assert state.records_processed == 0
    assert state.errors == {}
    assert state.start_time is None
    assert state.end_time is None

def test_pipeline_state_tracking():
    """Test PipelineState tracking functionality"""
    state = PipelineState(status=PipelineStatus.INITIALIZED)
    
    # Simulate pipeline execution
    state.status = PipelineStatus.RUNNING
    state.start_time = datetime.now()
    state.records_processed = 50
    
    assert state.status == PipelineStatus.RUNNING
    assert state.start_time is not None
    assert state.records_processed == 50 