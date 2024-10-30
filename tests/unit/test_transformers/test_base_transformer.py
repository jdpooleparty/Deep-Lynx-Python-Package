import pytest
import pandas as pd
from dev.pipeline.transformers.base_transformer import DeepLynxTransformer

@pytest.fixture
def sample_mapping_config():
    """Provide sample mapping configuration"""
    return {
        "column_mappings": {
            "equipment_name": "name",
            "process_type": "type",
            "duration": "process_duration"
        },
        "type_conversions": {
            "duration": "int64"
        },
        "metadata": {
            "source": "manufacturing_data",
            "version": "1.0"
        }
    }

@pytest.fixture
def sample_data():
    """Provide sample manufacturing data"""
    return pd.DataFrame({
        "equipment_name": ["CNC Machine", "3D Printer"],
        "process_type": ["Machining", "Additive"],
        "duration": ["120", "240"],
        "status": ["active", "active"]
    })

def test_transformer_initialization(sample_mapping_config):
    """Test transformer initialization with config"""
    transformer = DeepLynxTransformer(sample_mapping_config)
    assert transformer.mapping_config == sample_mapping_config

def test_column_mapping(sample_mapping_config, sample_data):
    """Test column name mapping"""
    transformer = DeepLynxTransformer(sample_mapping_config)
    result = transformer.transform(sample_data)
    
    # Check mapped column names
    assert "name" in result.columns
    assert "type" in result.columns
    assert "process_duration" in result.columns
    
    # Verify original values maintained
    assert result["name"].tolist() == ["CNC Machine", "3D Printer"]
    assert result["type"].tolist() == ["Machining", "Additive"]

def test_type_conversion(sample_mapping_config, sample_data):
    """Test data type conversion"""
    transformer = DeepLynxTransformer(sample_mapping_config)
    result = transformer.transform(sample_data)
    
    # Check converted data type
    assert result["process_duration"].dtype == "int64"
    assert result["process_duration"].tolist() == [120, 240]

def test_metadata_addition(sample_mapping_config, sample_data):
    """Test metadata column addition"""
    transformer = DeepLynxTransformer(sample_mapping_config)
    result = transformer.transform(sample_data)
    
    # Check metadata columns
    assert result["source"].unique() == ["manufacturing_data"]
    assert result["version"].unique() == ["1.0"] 