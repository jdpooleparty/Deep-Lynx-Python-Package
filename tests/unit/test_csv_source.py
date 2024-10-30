import pytest
import pandas as pd
from pathlib import Path
from dev.pipeline.sources.csv_source import CSVDataSource

@pytest.fixture
def sample_csv_file(tmp_path: Path) -> Path:
    """Create a sample CSV file with test data"""
    file_path = tmp_path / "test_data.csv"
    
    # Create test data
    df = pd.DataFrame({
        'id': range(1, 1001),
        'name': [f'test_{i}' for i in range(1, 1001)],
        'value': range(100, 1100)
    })
    
    df.to_csv(file_path, index=False)
    return file_path

def test_csv_source_initialization(sample_csv_file):
    """Test CSVDataSource initialization"""
    source = CSVDataSource(sample_csv_file, batch_size=100)
    assert source.file_path == sample_csv_file
    assert source.batch_size == 100

def test_csv_source_extraction(sample_csv_file):
    """Test data extraction in batches"""
    source = CSVDataSource(sample_csv_file, batch_size=250)
    
    # Extract all batches
    batches = list(source.extract())
    
    # Verify batch count and sizes
    assert len(batches) == 4  # 1000 records / 250 batch_size = 4 batches
    assert all(len(batch) == 250 for batch in batches[:-1])  # All but last batch should be full
    assert all(isinstance(batch, pd.DataFrame) for batch in batches) 