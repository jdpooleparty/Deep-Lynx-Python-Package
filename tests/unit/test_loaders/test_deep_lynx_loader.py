import pytest
import pandas as pd
from unittest.mock import Mock, patch
from dev.pipeline.loaders.deep_lynx_loader import DeepLynxLoader
from dev.pipeline_config import PipelineConfig

@pytest.fixture
def mock_client():
    """Create mock Deep Lynx client"""
    client = Mock()
    client.create_data_nodes.return_value.is_success.return_value = True
    return client

@pytest.fixture
def sample_transformed_data():
    """Provide sample transformed data"""
    return pd.DataFrame({
        "id": ["EQ001", "EQ002"],
        "name": ["CNC Machine", "3D Printer"],
        "type": ["Machining", "Additive"],
        "process_duration": [120, 240],
        "source": ["manufacturing_data", "manufacturing_data"]
    })

@pytest.fixture
def loader_config(mock_client):
    """Create loader configuration"""
    config = Mock(spec=PipelineConfig)
    config.client = mock_client
    config.batch_size = 100
    config.retry_attempts = 3
    return config

def test_loader_initialization(loader_config):
    """Test loader initialization"""
    loader = DeepLynxLoader(loader_config, "test-container-id")
    assert loader.container_id == "test-container-id"
    assert loader.batch_size == 100
    assert loader.retry_attempts == 3

def test_successful_load(loader_config, sample_transformed_data):
    """Test successful data loading"""
    loader = DeepLynxLoader(loader_config, "test-container-id")
    success = loader.load(sample_transformed_data)
    
    assert success is True
    loader_config.client.create_data_nodes.assert_called_once()

def test_failed_load_with_retry(loader_config, sample_transformed_data):
    """Test load retry on failure"""
    # Configure mock to fail twice then succeed
    loader_config.client.create_data_nodes.side_effect = [
        Mock(is_success=lambda: False),
        Mock(is_success=lambda: False),
        Mock(is_success=lambda: True)
    ]
    
    loader = DeepLynxLoader(loader_config, "test-container-id")
    success = loader.load(sample_transformed_data)
    
    assert success is True
    assert loader_config.client.create_data_nodes.call_count == 3

@pytest.mark.asyncio
async def test_load_with_large_dataset(loader_config):
    """Test loading large dataset in batches"""
    # Create large dataset
    large_data = pd.DataFrame({
        "id": [f"EQ{i:03d}" for i in range(250)],
        "name": [f"Equipment {i}" for i in range(250)],
        "type": ["Type A"] * 250,
        "process_duration": [120] * 250
    })
    
    loader = DeepLynxLoader(loader_config, "test-container-id")
    success = loader.load(large_data)
    
    assert success is True
    # Should have made 3 calls (250 records / 100 batch_size = 3 batches)
    assert loader_config.client.create_data_nodes.call_count == 3 