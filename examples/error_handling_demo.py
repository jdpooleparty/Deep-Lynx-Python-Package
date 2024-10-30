from pathlib import Path
import pandas as pd
from dev.pipeline.sources.csv_source import CSVDataSource
from dev.pipeline.state import PipelineState, PipelineStatus
from dev.pipeline_config import PipelineConfig
from dev.config import DeepLynxConfig
from dev.utils.logging import setup_pipeline_logging

def demonstrate_error_scenarios():
    """Demonstrate various error handling scenarios"""
    logger = setup_pipeline_logging(log_file=Path("logs/error_handling.log"))
    state = PipelineState(status=PipelineStatus.INITIALIZED)
    
    # Scenario 1: Missing File
    try:
        logger.info("Testing missing file scenario...")
        source = CSVDataSource(Path("nonexistent.csv"))
        next(source.extract())
    except FileNotFoundError as e:
        logger.error(f"File not found error handled: {e}")
        state.errors["file_error"] = str(e)

    # Scenario 2: Schema Validation
    try:
        logger.info("Testing schema validation scenario...")
        invalid_data = pd.DataFrame({
            'invalid_column': ['test'],
            'age': ['not_a_number']
        })
        # Simulate validation
        if 'required_column' not in invalid_data.columns:
            raise ValueError("Missing required column: required_column")
    except ValueError as e:
        logger.error(f"Schema validation error handled: {e}")
        state.errors["validation_error"] = str(e)

    # Scenario 3: Type Conversion
    try:
        logger.info("Testing type conversion scenario...")
        bad_data = pd.DataFrame({
            'number_field': ['abc', '123', 'xyz']
        })
        bad_data['number_field'] = pd.to_numeric(bad_data['number_field'])
    except ValueError as e:
        logger.error(f"Type conversion error handled: {e}")
        state.errors["conversion_error"] = str(e)

    # Display error summary
    print("\nError Handling Summary:")
    for error_type, error_msg in state.errors.items():
        print(f"\n{error_type}:")
        print(f"- {error_msg}")

if __name__ == "__main__":
    demonstrate_error_scenarios() 