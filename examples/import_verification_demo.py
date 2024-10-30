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
        container_response = containers_api.create_container(
            body=CreateContainerRequest(name=container_name)
        )
        if not hasattr(container_response, 'value'):
            raise Exception("Container creation response missing value")
            
        container_id = container_response.value.id
        
        # Create service user for container
        service_user = users_api.create_service_user(container_id)
        if not hasattr(service_user, 'value'):
            raise Exception("Service user creation response missing value")
            
        return (
            container_id,
            service_user.value.key,
            service_user.value.secret
        )
    except ApiException as e:
        logger.error(f"Failed to create container or service user: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in container creation: {e}")
        raise

async def verify_credentials(base_config: DeepLynxConfig) -> bool:
    """Verify that credentials have correct container access"""
    try:
        auth_api = base_config.get_auth_api()
        # Use the environment variables directly since they're already validated
        token_response = auth_api.retrieve_o_auth_token(
            x_api_key=os.getenv('API_KEY'),
            x_api_secret=os.getenv('API_SECRET')
        )
        
        if not hasattr(token_response, 'value') or not token_response.value:
            return False
            
        # Test container access
        api_client = ApiClient(base_config.configuration)
        containers_api = ContainersApi(api_client)
        containers = containers_api.list_containers()
        
        if not hasattr(containers, 'value'):
            return False
            
        return True
        
    except ApiException as e:
        logger.error(f"Credential verification failed: {e}")
        return False

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

    try:
        # Initialize configuration with auth
        base_config = DeepLynxConfig(
            base_url=env_vars['BASE_URL'],
            api_key=env_vars['API_KEY'],
            api_secret=env_vars['API_SECRET']
        )
        
        # Verify credentials have correct access
        if not await verify_credentials(base_config):
            error_msg = (
                "\nCredential verification failed:\n"
                "1. Credentials exist but lack container access\n"
                "2. Please ensure credentials have container admin permissions\n"
                "3. Try creating a new container and using its service user credentials\n"
                "4. Current credentials may be for a different container"
            )
            logger.error(error_msg)
            print(f"\nAccess Error: {error_msg}")
            return

        # Verify authentication before proceeding
        auth_api = base_config.get_auth_api()
        try:
            token_response = auth_api.retrieve_o_auth_token(
                x_api_key=env_vars['API_KEY'],
                x_api_secret=env_vars['API_SECRET']
            )
            if not hasattr(token_response, 'value') or not token_response.value:
                raise ApiException(status=401, reason="Invalid token response")
            logger.info("Successfully authenticated with provided credentials")
            
            # Create API clients with authenticated configuration
            api_client = ApiClient(base_config.configuration)
            containers_api = ContainersApi(api_client)
            users_api = UsersApi(api_client)
            
            # Create new container with service user keys
            container_name = f"verification_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            container_id, new_api_key, new_api_secret = await create_container_with_keys(
                containers_api, 
                users_api, 
                container_name
            )
            
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
                    x_api_key=new_api_key,
                    x_api_secret=new_api_secret
                )
                if not hasattr(token_response, 'value') or not token_response.value:
                    raise ApiException(status=401, reason="Invalid token response")
                logger.info("Successfully authenticated with new service user credentials")
            except ApiException as auth_e:
                if auth_e.status == 401:
                    error_msg = (
                        "Authentication failed with new service user credentials:\n"
                        "1. Container created successfully but authentication failed\n"
                        f"2. Container ID: {container_id}\n"
                        "3. Please verify the service user was created correctly"
                    )
                    logger.error(error_msg)
                    print(f"\nAuthentication Error: {error_msg}")
                    return
                raise auth_e

            # Get new API clients with updated configuration
            containers_api = ContainersApi(ApiClient(base_config.configuration))
            datasources_api = DataSourcesApi(ApiClient(base_config.configuration))
            
            try:
                # List all containers and their data sources
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
                                        
                        except ApiException as ds_e:
                            logger.error(f"Error listing data sources: {ds_e}")
                            
            except ApiException as list_e:
                logger.error(f"Error listing containers: {list_e}")
                
        except ApiException as auth_e:
            if auth_e.status == 401:
                error_msg = (
                    "\nAuthentication failed with provided credentials:\n"
                    "1. API key and secret were found but are invalid\n"
                    "2. Please verify your credentials in .env file\n"
                    "3. Ensure you have proper permissions in Deep Lynx"
                )
                logger.error(error_msg)
                print(f"\nAuthentication Error: {error_msg}")
                return
            raise auth_e

    except ApiException as e:
        logger.error(f"API error occurred: {e}")
        print(f"\nAPI Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\nError: {e}")

if __name__ == "__main__":
    asyncio.run(run_import_verification())