from pathlib import Path
import asyncio
import os
import logging
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
import aiohttp

from deep_lynx import (
    Configuration, 
    ApiClient,
    DataSourcesApi,
    ContainersApi,
    UsersApi,
    CreateDataSourceRequest,
    CreateContainerRequest
)
from deep_lynx.rest import ApiException

from dev.utils.logging import setup_pipeline_logging
from dev.config import DeepLynxConfig

logger = logging.getLogger('deep_lynx_pipeline')

async def verify_import_status(
    datasources_api: DataSourcesApi,
    container_id: str,
    data_source_id: str,
    timeout: int = 60
) -> bool:
    """
    Verify that data imports have completed successfully.
    Returns True if imports are completed, False otherwise.
    """
    start_time = datetime.now()
    while (datetime.now() - start_time) < timedelta(seconds=timeout):
        try:
            imports = datasources_api.list_imports_for_data_source(
                container_id=container_id,
                data_source_id=data_source_id
            )
            
            if not imports.value:
                logger.warning("No imports found")
                await asyncio.sleep(2)
                continue
                
            # Log detailed import status
            for imp in imports.value:
                logger.info(
                    f"Import {imp.id} status: {imp.status} "
                    f"(records: {getattr(imp, 'records_inserted', 'unknown')})"
                )
                
                if hasattr(imp, 'error') and imp.error:
                    logger.error(f"Import error: {imp.error}")
                
            # Check if all imports are complete
            all_complete = all(
                getattr(imp, 'status', '') == 'completed' 
                for imp in imports.value
            )
            
            if all_complete:
                return True
                
            await asyncio.sleep(2)
            
        except ApiException as e:
            logger.error(f"API error checking import status: {e}")
            return False
            
    logger.error(f"Import verification timed out after {timeout} seconds")
    return False

async def query_imported_data(
    containers_api: ContainersApi,
    container_id: str
) -> Optional[dict]:
    """
    Query the imported data to verify it exists in Deep Lynx
    """
    try:
        # Basic query to check for any data
        query = {
            "data_sources": ["Pipeline Demo Source"],
            "return_type": "graph"
        }
        
        result = containers_api.query_container_data(
            container_id=container_id,
            query=query
        )
        
        if hasattr(result, 'value'):
            logger.info(f"Query returned {len(result.value)} records")
            return result.value
            
    except ApiException as e:
        logger.error(f"Error querying data: {e}")
    return None

async def create_container_with_keys(containers_api: ContainersApi, users_api: UsersApi, container_name: str) -> tuple[str, str, str]:
    """
    Create a new container and generate service user keys for it.
    Returns (container_id, api_key, api_secret)
    """
    try:
        # Create container
        container_request = CreateContainerRequest(
            name=container_name,
            description=f"Container created by import verification demo at {datetime.now()}",
            is_public=False
        )
        container_response = containers_api.create_container(container_request)
        
        if not hasattr(container_response, 'value') or not container_response.value:
            raise Exception("No container data in response")
            
        container_id = container_response.value[0].id
        logger.info(f"Created container: {container_name} (ID: {container_id})")
        
        # Create service user for the container
        service_user = users_api.create_service_user(
            container_id=container_id,
            body={"name": f"{container_name}_service_user"}
        )
        
        if not hasattr(service_user, 'value') or not service_user.value:
            raise Exception("No service user data in response")
            
        service_user_id = service_user.value.id
        
        # Generate key pair for service user
        key_pair = users_api.create_service_user_key_pair(
            container_id=container_id,
            service_user_id=service_user_id
        )
        
        if not hasattr(key_pair, 'value') or not key_pair.value:
            raise Exception("No key pair data in response")
            
        return container_id, key_pair.value.key, key_pair.value.secret
        
    except ApiException as e:
        logger.error(f"API error creating container and keys: {e}")
        raise

async def run_import_verification():
    """Demo script to verify data imports and query results"""
    # Setup logging first
    log_file = Path("logs/import_verification.log")
    log_file.parent.mkdir(exist_ok=True)
    logger = setup_pipeline_logging(log_file=log_file)
    
    # Load environment variables
    load_dotenv(override=True)  # Add override=True to ensure env vars are reloaded
    
    # Verify Deep Lynx is running
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(os.getenv('BASE_URL', 'http://localhost:8090') + '/health') as response:
                if response.status != 200:
                    logger.error(f"Deep Lynx health check failed: {response.status}")
                    print("\nError: Deep Lynx server is not responding properly")
                    print("Please ensure Deep Lynx is running and accessible")
                    return
                version = await response.text()
                logger.info(f"Deep Lynx server running (version {version})")
    except Exception as e:
        logger.error(f"Could not connect to Deep Lynx: {e}")
        print("\nError: Could not connect to Deep Lynx server")
        print("Please ensure Deep Lynx is running and accessible")
        return

    # Verify required environment variables with detailed feedback
    env_vars = {
        'BASE_URL': os.getenv('BASE_URL', 'http://localhost:8090'),
        'API_KEY': os.getenv('API_KEY'),
        'API_SECRET': os.getenv('API_SECRET')
    }
    
    if not env_vars['API_KEY'] or not env_vars['API_SECRET']:
        print("\nMissing API credentials. Please check your .env file:")
        print("1. Ensure .env file exists in project root")
        print("2. File should contain:")
        print("   API_KEY=your_api_key")
        print("   API_SECRET=your_api_secret")
        print("   BASE_URL=http://localhost:8090 (optional)")
        print("\n3. Current values:")
        print(f"   BASE_URL: {env_vars['BASE_URL']}")
        print(f"   API_KEY: {'[SET]' if env_vars['API_KEY'] else '[MISSING]'}")
        print(f"   API_SECRET: {'[SET]' if env_vars['API_SECRET'] else '[MISSING]'}")
        return

    try:
        # Initialize configuration with auth
        base_config = DeepLynxConfig(
            base_url=env_vars['BASE_URL'],
            api_key=env_vars['API_KEY'],
            api_secret=env_vars['API_SECRET']
        )
        
        # Get API clients
        containers_api = ContainersApi(ApiClient(base_config.configuration))
        users_api = UsersApi(ApiClient(base_config.configuration))
        
        # Create new container with service user keys
        container_name = f"verification_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            container_id, new_api_key, new_api_secret = await create_container_with_keys(
                containers_api, 
                users_api, 
                container_name
            )
            print("\nCreated new container with credentials:")
            print(f"Container ID: {container_id}")
            print(f"API Key: {new_api_key}")
            print(f"API Secret: {new_api_secret}")
            print("\nIMPORTANT: Save these credentials! The API secret cannot be retrieved later.")
            
            # Update configuration to use new credentials
            base_config = DeepLynxConfig(
                base_url=env_vars['BASE_URL'],
                api_key=new_api_key,
                api_secret=new_api_secret
            )
            
            # Test authentication with NEW credentials
            auth_api = base_config.get_auth_api()
            try:
                token_response = auth_api.retrieve_o_auth_token(
                    x_api_key=new_api_key,  # Use new credentials here
                    x_api_secret=new_api_secret  # Use new credentials here
                )
                if not hasattr(token_response, 'value') or not token_response.value:
                    raise ApiException(status=401, reason="Invalid token response")
                logger.info("Successfully authenticated with new service user credentials")
            except ApiException as e:
                if e.status == 401:
                    error_msg = (
                        "Authentication failed with new service user credentials:\n"
                        "1. Container created successfully but authentication failed\n"
                        "2. Container ID: " + container_id + "\n"
                        "3. Please verify the service user was created correctly"
                    )
                    logger.error(error_msg)
                    print(f"\nAuthentication Error: {error_msg}")
                    return
                raise e

            # Get new API clients with updated configuration
            containers_api = ContainersApi(ApiClient(base_config.configuration))
            datasources_api = DataSourcesApi(ApiClient(base_config.configuration))
            
            # List all containers and their data sources
            try:
                containers = containers_api.list_containers()
                
                if not hasattr(containers, 'value') or not containers.value:
                    logger.error("No containers found")
                    return
                    
                print("\nAvailable Containers:")
                for container in containers.value:
                    if not getattr(container, 'archived', False):
                        print(f"\nContainer: {container.name} (ID: {container.id})")
                        
                        try:
                            datasources = datasources_api.list_data_sources(container.id)
                            if hasattr(datasources, 'value') and datasources.value:
                                print("Data Sources:")
                                for ds in datasources.value:
                                    print(f"- {ds.name} (ID: {ds.id})")
                                    
                                    # Check import status
                                    print("\nChecking import status...")
                                    import_success = await verify_import_status(
                                        datasources_api,
                                        container.id,
                                        ds.id,
                                        timeout=30
                                    )
                                    
                                    if import_success:
                                        print("Imports completed successfully")
                                        
                                        # Query the data
                                        print("\nQuerying imported data...")
                                        data = await query_imported_data(
                                            containers_api,
                                            container.id
                                        )
                                        
                                        if data:
                                            print(f"Found {len(data)} records")
                                            print("\nSample data structure:")
                                            if len(data) > 0:
                                                print(data[0])
                                        else:
                                            print("No data found in query results")
                                    else:
                                        print("Import verification failed or timed out")
                                        
                        except ApiException as e:
                            logger.error(f"Error listing data sources: {e}")
                            
            except ApiException as e:
                logger.error(f"Error listing containers: {e}")

    except ApiException as e:
        logger.error(f"API error occurred: {e}")
        print(f"\nAPI Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\nError: {e}")

if __name__ == "__main__":
    asyncio.run(run_import_verification())