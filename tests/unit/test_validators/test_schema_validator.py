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
                description="Unique identifier for equipment",
                constraints={"pattern": r"^EQ\d{3}$"}
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
            ),
            SchemaField(
                name="maintenance_interval",
                data_type=DataType.INTEGER,
                required=False,
                description="Maintenance interval in days",
                constraints={"min": 1, "max": 365}
            )
        ],
        "Process": [
            SchemaField(
                name="process_id",
                data_type=DataType.STRING,
                required=True,
                description="Process identifier",
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
                constraints={"min": 0, "max": 1440}
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
        "installation_date": ["2023-01-01", "2023-02-01"],
        "maintenance_interval": [30, 90]
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
    
    # Process data with invalid types
    process_data = pd.DataFrame({
        "process_id": ["P001"],
        "name": ["Milling"],
        "duration": ["invalid"]  # Should be numeric
    })
    
    errors = validator.validate_dataframe(process_data, "Process")
    assert "type_mismatch" in errors
    assert any("duration" in err for err in errors["type_mismatch"])

def test_schema_validation_constraints(manufacturing_schema):
    """Test validation of field constraints"""
    validator = SchemaValidator(manufacturing_schema)
    
    # Data with constraint violations
    process_data = pd.DataFrame({
        "process_id": ["P001", "P001"],  # Duplicate IDs (violates unique)
        "name": ["Process 1", "Process 2"],
        "duration": [2000, 1500]  # Exceeds max duration
    })
    
    errors = validator.validate_dataframe(process_data, "Process")
    assert "constraint" in errors
    assert any("unique" in err for err in errors["constraint"])
    assert any("maximum" in err for err in errors["constraint"])

def test_schema_validation_pattern_constraint(manufacturing_schema):
    """Test validation of pattern constraints"""
    validator = SchemaValidator(manufacturing_schema)
    
    # Invalid equipment IDs
    equipment_data = pd.DataFrame({
        "equipment_id": ["EQQ01", "123"],  # Invalid patterns
        "name": ["Machine 1", "Machine 2"],
        "type": ["Type A", "Type B"]
    })
    
    errors = validator.validate_dataframe(equipment_data, "Equipment")
    assert "constraint" in errors
    assert any("pattern" in err for err in errors["constraint"])

def test_schema_validation_datetime(manufacturing_schema):
    """Test validation of datetime fields"""
    validator = SchemaValidator(manufacturing_schema)
    
    # Invalid datetime format
    equipment_data = pd.DataFrame({
        "equipment_id": ["EQ001"],
        "name": ["Machine 1"],
        "type": ["Type A"],
        "installation_date": ["invalid-date"]
    })
    
    errors = validator.validate_dataframe(equipment_data, "Equipment")
    assert "type_mismatch" in errors
    assert any("installation_date" in err for err in errors["type_mismatch"])

def test_schema_validation_integer_constraints(manufacturing_schema):
    """Test validation of integer constraints"""
    validator = SchemaValidator(manufacturing_schema)
    
    # Invalid maintenance intervals
    equipment_data = pd.DataFrame({
        "equipment_id": ["EQ001", "EQ002"],
        "name": ["Machine 1", "Machine 2"],
        "type": ["Type A", "Type B"],
        "maintenance_interval": [0, 400]  # Outside valid range
    })
    
    errors = validator.validate_dataframe(equipment_data, "Equipment")
    assert "constraint" in errors
    assert any("minimum" in err for err in errors["constraint"])
    assert any("maximum" in err for err in errors["constraint"])

def test_unknown_metatype(manufacturing_schema):
    """Test validation with unknown metatype"""
    validator = SchemaValidator(manufacturing_schema)
    
    data = pd.DataFrame({"field": ["value"]})
    
    with pytest.raises(ValueError, match="Unknown metatype"):
        validator.validate_dataframe(data, "UnknownType")