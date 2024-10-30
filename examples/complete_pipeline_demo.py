from pathlib import Path
import asyncio
import os
import logging
from dotenv import load_dotenv
from deep_lynx import (
    CreateContainerRequest,
    CreateDataSourceRequest,
    Configuration,
    ApiClient
)
from deep_lynx.rest import ApiException
from dev.pipeline.sources.csv_source import CSVDataSource
from dev.pipeline.transformers.base_transformer import DeepLynxTransformer
from dev.pipeline.loaders.deep_lynx_loader import DeepLynxLoader
from dev.pipeline.orchestrator import PipelineOrchestrator
from dev.pipeline_config import PipelineConfig
from dev.config import DeepLynxConfig
from dev.utils.logging import setup_pipeline_logging
from dev.pipeline.state import PipelineState, PipelineStatus
from datetime import datetime

# Set up logging
logger = logging.getLogger('deep_lynx_pipeline')

async def run_complete_pipeline():
    """Demonstrate complete pipeline with all components"""
    # Set up logging first
    log_file = Path("logs/complete_pipeline.log")
    log_file.parent.mkdir(exist_ok=True)  # Create logs directory if it doesn't exist
    logger = setup_pipeline_logging(log_file=log_file)
    logger.info("Starting pipeline execution")
    
    # Load environment variables
    load_dotenv()
    
    # Initialize configuration with auth
    base_config = DeepLynxConfig(
        base_url=os.getenv('BASE_URL', 'http://localhost:8090'),
        api_key=os.getenv('API_KEY'),
        api_secret=os.getenv('API_SECRET')
    )
    
    # No need for separate token retrieval since it's handled in DeepLynxConfig
    pipeline_config = PipelineConfig(base_config)
    
    # Configure components
    source = CSVDataSource(
        Path("tests/data/sample_manufacturing_data.csv"),
        batch_size=2
    )
    
    transformer = DeepLynxTransformer({
        "column_mappings": {
            "equipment_name": "name",
            "process_type": "metatype",
            "duration": "process_duration"
        },
        "type_conversions": {
            "process_duration": "int64"
        }
    })
    
    # Create or get container and data source
    containers_api = pipeline_config.get_containers_api()
    datasources_api = pipeline_config.get_datasources_api()
    
    # Generate unique container name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    container_name = f"Pipeline_Demo_Container_{timestamp}"
    
    # Try to find existing container
    container_id = None
    try:
        containers = containers_api.list_containers()
        if hasattr(containers, 'value') and containers.value:
            for container in containers.value:
                # Look for any non-archived container with our prefix
                if (hasattr(container, 'name') and 
                    container.name.startswith("Pipeline_Demo_Container_") and
                    not getattr(container, 'archived', False)):
                    container_id = container.id
                    logger.info(f"Found existing container with ID: {container_id}")
                    break
    except Exception as e:
        logger.warning(f"Error checking existing containers: {e}")
    
    # Create container if no suitable one exists
    if not container_id:
        try:
            container_response = containers_api.create_container(
                CreateContainerRequest(
                    name=container_name,
                    description="Container for pipeline demo"
                )
            )
            if hasattr(container_response, 'value') and container_response.value:
                container_id = container_response.value[0].id
                logger.info(f"Created new container with ID: {container_id}")
            else:
                raise Exception("Container creation response missing value")
        except ApiException as e:
            # Archive old containers if we hit the duplicate name error
            if "already exists" in str(e):
                try:
                    old_containers = containers_api.list_containers()
                    for container in old_containers.value:
                        if (container.name.startswith("Pipeline_Demo_Container_") and
                            not getattr(container, 'archived', False)):
                            try:
                                containers_api.archive_container(container.id)
                                logger.info(f"Archived old container: {container.name}")
                            except Exception as archive_error:
                                logger.warning(f"Failed to archive container {container.name}: {archive_error}")
                    
                    # Try creating container again with new name
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    container_name = f"Pipeline_Demo_Container_{timestamp}"
                    container_response = containers_api.create_container(
                        CreateContainerRequest(
                            name=container_name,
                            description="Container for pipeline demo"
                        )
                    )
                    container_id = container_response.value[0].id
                    logger.info(f"Created new container with ID: {container_id} after cleanup")
                except Exception as retry_error:
                    logger.error(f"Failed to create container after cleanup: {retry_error}")
                    raise Exception(f"Failed to create container after cleanup: {retry_error}")
            else:
                logger.error(f"Failed to create container: {e}")
                raise Exception(f"Failed to create container: {e}")
    
    # Try to find existing data source
    datasource_id = None
    try:
        datasources = datasources_api.list_data_sources(container_id=container_id)
        if hasattr(datasources, 'value') and datasources.value:
            for datasource in datasources.value:
                if datasource.name == "Pipeline Demo Source":
                    datasource_id = datasource.id
                    logger.info(f"Found existing data source with ID: {datasource_id}")
                    break
    except Exception as e:
        logger.warning(f"Error checking existing data sources: {e}")
    
    # Create data source if it doesn't exist
    if not datasource_id:
        try:
            datasource_response = datasources_api.create_data_source(
                container_id=container_id,
                body=CreateDataSourceRequest(
                    name="Pipeline Demo Source",
                    adapter_type="standard",
                    active=True
                )
            )
            if hasattr(datasource_response, 'value'):
                datasource_id = datasource_response.value.id
                logger.info(f"Created new data source with ID: {datasource_id}")
            else:
                raise Exception("Data source creation response missing value")
        except ApiException as e:
            logger.error(f"Failed to create data source: {e}")
            raise Exception(f"Failed to create data source: {e}")
    
    # Initialize loader with container and data source IDs
    loader = DeepLynxLoader(
        pipeline_config,
        container_id=container_id,
        data_source_id=datasource_id
    )
    
    # Create orchestrator with correct parameters
    orchestrator = PipelineOrchestrator(
        source=source,
        transformer=transformer,
        loader=loader,
        state=PipelineState(status=PipelineStatus.INITIALIZED)  # Add state parameter
    )
    
    # Execute pipeline
    success = await orchestrator.run()  # Use run() instead of execute()
    
    if success:
        print("\nPipeline completed successfully!")
        print(f"Container Name: {container_name}")
        print(f"Container ID: {container_id}")
        print(f"Data Source ID: {datasource_id}")
        
        # Wait for imports to complete
        try:
            max_retries = 10
            retry_delay = 2  # seconds
            
            for attempt in range(max_retries):
                imports = datasources_api.list_imports_for_data_source(
                    container_id=container_id,
                    data_source_id=datasource_id
                )
                
                if not imports.value:
                    logger.warning(f"No imports found on attempt {attempt + 1}")
                    await asyncio.sleep(retry_delay)
                    continue
                
                all_complete = all(
                    getattr(imp, 'status', '') == 'completed' 
                    for imp in imports.value
                )
                
                if all_complete:
                    logger.info("All imports completed successfully")
                    break
                    
                logger.info(f"Waiting for imports to complete (attempt {attempt + 1}/{max_retries})")
                await asyncio.sleep(retry_delay)
            else:
                logger.warning("Import completion check timed out")
                
        except Exception as e:
            logger.error(f"Error checking import status: {e}")
            
        print("\nYou can view this data in the Deep Lynx UI at:")
        print(f"{base_config.configuration.host}/containers/{container_id}/data")
        print("\nOr query the data using:")
        print(f"{base_config.configuration.host}/containers/{container_id}/data/query")
        
        # Check container status
        try:
            container = containers_api.retrieve_container(container_id)
            if hasattr(container, 'value') and container.value:
                if getattr(container.value, 'archived', False):
                    print("\nWARNING: This container is archived. Please unarchive it to view the data.")
            else:
                print("\nWARNING: Could not verify container status: No container data returned")
        except Exception as e:
            print(f"\nWARNING: Could not verify container status: {e}")
    else:
        print("\nPipeline failed! Check logs for details.")

if __name__ == "__main__":
    # Run the async function using asyncio
    asyncio.run(run_complete_pipeline())