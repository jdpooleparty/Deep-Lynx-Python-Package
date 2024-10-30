import pytest
from pathlib import Path
from dev.pipeline.sources.csv_source import CSVDataSource
from dev.pipeline_config import PipelineConfig

@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """Create a sample CSV file for testing"""
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(
        "id,name,value\n"
        "1,test1,100\n"
        "2,test2,200\n"
    )
    return csv_path

@pytest.mark.asyncio
async def test_csv_pipeline_integration(
    mock_pipeline_config: PipelineConfig,
    sample_csv: Path
):
    """Test complete CSV pipeline flow"""
    source = CSVDataSource(sample_csv, batch_size=100)
    
    # Test extraction
    batches = list(source.extract())
    assert len(batches) == 1
    assert len(batches[0]) == 2 