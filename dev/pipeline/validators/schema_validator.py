from typing import Dict, Any, List, Optional
import pandas as pd
from dataclasses import dataclass
from enum import Enum
import re

class DataType(Enum):
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    ARRAY = "array"
    OBJECT = "object"

@dataclass
class SchemaField:
    name: str
    data_type: DataType
    required: bool = False
    description: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None

class SchemaValidator:
    """Validates data against Deep Lynx schema"""
    def __init__(self, schema: Dict[str, List[SchemaField]]):
        self.schema = schema
        
    def validate_dataframe(self, df: pd.DataFrame, metatype: str) -> Dict[str, List[str]]:
        """Validate DataFrame against schema for given metatype"""
        if metatype not in self.schema:
            raise ValueError(f"Unknown metatype: {metatype}")
            
        errors: Dict[str, List[str]] = {"missing": [], "type_mismatch": [], "constraint": []}
        fields = self.schema[metatype]
        
        # Check for required fields
        for field in fields:
            if field.required and field.name not in df.columns:
                errors["missing"].append(
                    f"Required field '{field.name}' is missing"
                )
                continue
                
            if field.name in df.columns:
                # Validate type
                type_errors = self._validate_type(df[field.name], field)
                if type_errors:
                    errors["type_mismatch"].extend(type_errors)
                    continue  # Skip constraint validation if type is invalid
                
                # Validate constraints if present
                if field.constraints:
                    constraint_errors = self._validate_constraints(
                        df[field.name],
                        field.constraints,
                        field.data_type
                    )
                    if constraint_errors:
                        errors["constraint"].extend(constraint_errors)
        
        # Only return non-empty error categories
        return {k: v for k, v in errors.items() if v}
    
    def _validate_type(
        self,
        series: pd.Series,
        field: SchemaField
    ) -> List[str]:
        """Validate data type of a series"""
        errors = []
        try:
            if field.data_type == DataType.STRING:
                # For strings, just verify they're all strings
                if not pd.api.types.is_string_dtype(series):
                    errors.append(
                        f"Field '{series.name}' contains non-string values"
                    )
            elif field.data_type == DataType.NUMBER:
                pd.to_numeric(series, errors='raise')
            elif field.data_type == DataType.INTEGER:
                pd.to_numeric(series, errors='raise', downcast='integer')
            elif field.data_type == DataType.BOOLEAN:
                series.astype(bool)
            elif field.data_type == DataType.DATETIME:
                pd.to_datetime(series, errors='raise')
        except Exception as e:
            errors.append(
                f"Field '{series.name}' has invalid {field.data_type.value} values: {str(e)}"
            )
        return errors
    
    def _validate_constraints(
        self, 
        series: pd.Series, 
        constraints: Dict[str, Any],
        data_type: DataType
    ) -> List[str]:
        """Validate constraints on a series"""
        errors = []
        
        # Convert series to appropriate type for constraint validation
        try:
            if data_type in [DataType.NUMBER, DataType.INTEGER]:
                series = pd.to_numeric(series)
            elif data_type == DataType.DATETIME:
                series = pd.to_datetime(series)
        except Exception:
            return [f"Could not convert field '{series.name}' for constraint validation"]
            
        for constraint, value in constraints.items():
            if constraint == "min":
                if series.min() < value:
                    errors.append(
                        f"Values in field '{series.name}' are below minimum: {value}"
                    )
            elif constraint == "max":
                if series.max() > value:
                    errors.append(
                        f"Values in field '{series.name}' are above maximum: {value}"
                    )
            elif constraint == "unique" and value:
                duplicates = series[series.duplicated()].unique()
                if len(duplicates) > 0:
                    errors.append(
                        f"Field '{series.name}' violates unique constraint with duplicate values: {list(duplicates)}"
                    )
            elif constraint == "pattern" and data_type == DataType.STRING:
                pattern = re.compile(value)
                invalid = series[~series.str.match(pattern)]
                if len(invalid) > 0:
                    errors.append(
                        f"Values in field '{series.name}' do not match pattern {value}: {list(invalid)}"
                    )
        
        return errors