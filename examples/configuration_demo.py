from pathlib import Path
import os
from dotenv import load_dotenv
from dev.pipeline_config import PipelineConfig
from dev.config import DeepLynxConfig
from dev.utils.logging import setup_pipeline_logging

def demonstrate_configurations():
    """Demonstrate different pipeline configurations"""
    # Setup logging
    logger = setup_pipeline_logging(log_file=Path("logs/config.log"))
    logger.info("Starting configuration demo")
    
    # Load and verify environment variables
    load_dotenv(override=True)
    env_vars = {
        'BASE_URL': os.getenv('BASE_URL', 'http://localhost:8090'),
        'API_KEY': os.getenv('API_KEY'),
        'API_SECRET': os.getenv('API_SECRET')
    }
    
    if not env_vars['API_KEY'] or not env_vars['API_SECRET']:
        error_msg = (
            "\nMissing API credentials. Please check your .env file:\n"
            "1. Ensure .env file exists in project root\n"
            "2. File should contain:\n"
            "   API_KEY=your_api_key\n"
            "   API_SECRET=your_api_secret\n"
            "   BASE_URL=http://localhost:8090 (optional)\n"
            f"\n3. Current values:\n"
            f"   BASE_URL: {env_vars['BASE_URL']}\n"
            f"   API_KEY: {'[SET]' if env_vars['API_KEY'] else '[MISSING]'}\n"
            f"   API_SECRET: {'[SET]' if env_vars['API_SECRET'] else '[MISSING]'}"
        )
        logger.error("Missing API credentials")
        print(error_msg)
        return

    # Initialize configuration with auth
    base_config = DeepLynxConfig(
        base_url=env_vars['BASE_URL'],
        api_key=env_vars['API_KEY'],
        api_secret=env_vars['API_SECRET']
    )
    pipeline_config = PipelineConfig(base_config)
    
    # 1. CSV Source Configuration
    pipeline_config.source_configs["csv_source"] = {
        "file_path": "data/input.csv",
        "batch_size": 1000,
        "encoding": "utf-8",
        "delimiter": ",",
        "date_format": "%Y-%m-%d"
    }
    
    # 2. Database Source Configuration
    pipeline_config.source_configs["db_source"] = {
        "connection_string": "postgresql://user:pass@localhost:5432/db",
        "query": "SELECT * FROM table",
        "batch_size": 500,
        "timeout": 30
    }
    
    # 3. API Source Configuration
    pipeline_config.source_configs["api_source"] = {
        "base_url": "https://api.example.com",
        "endpoint": "/data",
        "headers": {"Authorization": "Bearer token"},
        "rate_limit": 100,
        "timeout": 10
    }
    
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