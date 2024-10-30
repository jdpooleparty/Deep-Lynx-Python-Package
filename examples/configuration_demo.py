from pathlib import Path
from dev.pipeline_config import PipelineConfig
from dev.config import DeepLynxConfig
from dev.utils.logging import setup_pipeline_logging

def demonstrate_configurations():
    """Demonstrate different pipeline configurations"""
    logger = setup_pipeline_logging(log_file=Path("logs/config.log"))
    
    # Basic configuration
    base_config = DeepLynxConfig()
    pipeline_config = PipelineConfig(base_config)
    
    # 1. CSV Source Configuration
    pipeline_config.add_source_config("csv_source", {
        "file_path": "data/input.csv",
        "batch_size": 1000,
        "encoding": "utf-8",
        "delimiter": ",",
        "date_format": "%Y-%m-%d"
    })
    
    # 2. Database Source Configuration
    pipeline_config.add_source_config("db_source", {
        "connection_string": "postgresql://user:pass@localhost:5432/db",
        "query": "SELECT * FROM table",
        "batch_size": 500,
        "timeout": 30
    })
    
    # 3. API Source Configuration
    pipeline_config.add_source_config("api_source", {
        "base_url": "https://api.example.com",
        "endpoint": "/data",
        "headers": {"Authorization": "Bearer token"},
        "rate_limit": 100,
        "timeout": 10
    })
    
    # Display configurations
    print("\nPipeline Configurations:")
    print("\n1. General Settings:")
    print(f"Batch Size: {pipeline_config.batch_size}")
    print(f"Retry Attempts: {pipeline_config.retry_attempts}")
    print(f"Retry Delay: {pipeline_config.retry_delay} seconds")
    
    print("\n2. Source Configurations:")
    for source_name, config in pipeline_config.source_configs.items():
        print(f"\n{source_name}:")
        for key, value in config.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    demonstrate_configurations() 