import pytest
import pandas as pd
from dev.pipeline.validators.schema_validator import (
    SchemaValidator,
    SchemaField,
    DataType
)

@pytest.fixture
def manufacturing_schema():
    """Create sample manufacturing schema"""
    return {
        "Equipment": [
            SchemaField(
                name="equipment_id",
                data_type=DataType.STRING,
                required=True,
                description="Unique identifier for equipment"
            ),
            SchemaField(
                name="name",
                data_type=DataType.STRING,
                required=True,
                description="Equipment name"
            ),
            SchemaField(
                name="type",
                data_type=DataType.STRING,
                required=True,
                description="Equipment type"
            ),
            SchemaField(
                name="installation_date",
                data_type=DataType.DATETIME,
                required=False,
                description="Equipment installation date"
            )
        ],
        "Process": [
            SchemaField(
                name="process_id",
                data_type=DataType.STRING,
                required=True,
                description="Unique identifier for process",
                constraints={"unique": True}
            ),
            SchemaField(
                name="name",
                data_type=DataType.STRING,
                required=True,
                description="Process name"
            ),
            SchemaField(
                name="duration",
                data_type=DataType.NUMBER,
                required=True,
                description="Process duration in minutes",
                constraints={"min": 0, "max": 1440}  # Max 24 hours
            )
        ]
    }

def test_schema_validation_success(manufacturing_schema):
    """Test successful schema validation"""
    validator = SchemaValidator(manufacturing_schema)
    
    # Valid equipment data
    equipment_data = pd.DataFrame({
        "equipment_id": ["EQ001", "EQ002"],
        "name": ["CNC Machine", "3D Printer"],
        "type": ["Machining", "Additive"],
        "installation_date": ["2023-01-01", "2023-02-01"]
    })
    
    errors = validator.validate_dataframe(equipment_data, "Equipment")
    assert not errors, f"Unexpected validation errors: {errors}"

def test_schema_validation_missing_required(manufacturing_schema):
    """Test validation with missing required fields"""
    validator = SchemaValidator(manufacturing_schema)
    
    # Missing required 'type' field
    equipment_data = pd.DataFrame({
        "equipment_id": ["EQ001"],
        "name": ["CNC Machine"]
    })
    
    errors = validator.validate_dataframe(equipment_data, "Equipment")
    assert "missing" in errors
    assert any("type" in err for err in errors["missing"])

def test_schema_validation_type_mismatch(manufacturing_schema):
    """Test validation with incorrect data types"""
    validator = SchemaValidator(manufacturing_schema)
    
    # Invalid process duration (string instead of number)
    process_data = pd.DataFrame({
        "process_id": ["P001"],
        "name": ["Milling"],
        "duration": ["invalid"]
    })
    
    errors = validator.validate_dataframe(process_data, "Process")
    assert "type_mismatch" in errors
    assert any("duration" in err for err in errors["type_mismatch"])

def test_schema_validation_constraints(manufacturing_schema):
    """Test validation of field constraints"""
    validator = SchemaValidator(manufacturing_schema)
    
    # Process duration exceeds maximum
    process_data = pd.DataFrame({
        "process_id": ["P001"],
        "name": ["Long Process"],
        "duration": [2000]  # Exceeds 24 hours (1440 minutes)
    })
    
    errors = validator.validate_dataframe(process_data, "Process")
    assert "constraint" in errors
    assert any("duration" in err and "maximum" in err for err in errors["constraint"]) 