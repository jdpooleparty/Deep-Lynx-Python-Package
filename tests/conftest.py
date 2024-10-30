import pytest
from pathlib import Path
from dev.config import DeepLynxConfig
from dev.pipeline_config import PipelineConfig

# Get the path to the test data directory
TEST_DATA_DIR = Path(__file__).parent / "data"

@pytest.fixture
def mock_pipeline_config():
    """Create a pipeline configuration for testing"""
    config = DeepLynxConfig()
    return PipelineConfig(config)

@pytest.fixture
def sample_csv() -> Path:
    """Return path to sample CSV file"""
    csv_path = TEST_DATA_DIR / "sample_manufacturing_data.csv"
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Sample CSV file not found at {csv_path}. "
            "Please ensure the file exists in the test data directory."
        )
    return csv_path

@pytest.fixture
def sample_data():
    """Provide sample data for pipeline testing"""
    return {
        "nodes": [
            {
                "id": "EQ001",
                "type": "equipment",
                "properties": {
                    "equipment_name": "CNC Machine",
                    "process_type": "Machining",
                    "duration": 120,
                    "status": "active"
                }
            }
        ]
    } 