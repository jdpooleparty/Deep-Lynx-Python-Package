import pytest
import pandas as pd
from pathlib import Path

def test_sample_csv_exists(sample_csv):
    """Test that sample CSV file exists and is readable"""
    assert sample_csv.exists(), f"CSV file not found at {sample_csv}"
    
    # Try reading the file
    df = pd.read_csv(sample_csv)
    
    # Verify expected columns
    expected_columns = {"id", "equipment_name", "process_type", "duration", "status"}
    assert set(df.columns) == expected_columns
    
    # Verify we have data
    assert len(df) > 0, "CSV file is empty" 