from pathlib import Path
from dev.pipeline.sources.csv_source import CSVDataSource
from dev.pipeline.transformers.base_transformer import DeepLynxTransformer
from dev.pipeline.loaders.deep_lynx_loader import DeepLynxLoader
from dev.pipeline.orchestrator import PipelineOrchestrator
from dev.pipeline_config import PipelineConfig
from dev.config import DeepLynxConfig

def run_complete_pipeline():
    """Demonstrate complete pipeline with all components"""
    # Initialize configuration
    base_config = DeepLynxConfig()
    pipeline_config = PipelineConfig(base_config)
    
    # Configure components
    source = CSVDataSource(
        Path("tests/data/sample_manufacturing_data.csv"),
        batch_size=2
    )
    
    transformer = DeepLynxTransformer({
        "column_mappings": {
            "equipment_name": "name",
            "process_type": "type",
            "duration": "process_duration"
        },
        "type_conversions": {
            "process_duration": "int64"
        }
    })
    
    loader = DeepLynxLoader(pipeline_config, "test-container-id")
    
    # Create orchestrator
    orchestrator = PipelineOrchestrator(
        source=source,
        transformer=transformer,
        loader=loader,
        log_file=Path("logs/complete_pipeline.log")
    )
    
    # Execute pipeline
    success = orchestrator.execute()
    
    if success:
        print("\nPipeline completed successfully!")
    else:
        print("\nPipeline failed! Check logs for details.")

if __name__ == "__main__":
    run_complete_pipeline() 