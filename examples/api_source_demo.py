from pathlib import Path
import asyncio
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import aiohttp
from aiohttp import web
from deep_lynx import ApiClient
from deep_lynx.rest import ApiException
from dev.config import DeepLynxConfig
from dev.utils.logging import setup_pipeline_logging

logger = logging.getLogger('deep_lynx_pipeline')

async def start_mock_api():
    """Start a mock API server for testing"""
    async def health_check(request):
        return web.Response(text="OK")

    async def mock_data(request):
        return web.json_response({
            "data": [
                {"id": 1, "name": "Test Item 1"},
                {"id": 2, "name": "Test Item 2"}
            ]
        })

    app = web.Application()
    app.router.add_get('/health', health_check)
    app.router.add_get('/api/data', mock_data)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8081)
    await site.start()
    return runner

async def run_api_source_demo():
    """Demo script for API data source"""
    # Setup logging
    log_file = Path("logs/api_source.log")
    log_file.parent.mkdir(exist_ok=True)
    logger = setup_pipeline_logging(log_file=log_file)
    logger.info("Starting API source demo")

    # Load environment variables
    load_dotenv(override=True)
    
    # Verify environment variables
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

    # Start mock API server
    runner = await start_mock_api()
    logger.info("Started mock API server")

    try:
        # Initialize configuration with auth
        base_config = DeepLynxConfig(
            base_url=env_vars['BASE_URL'],
            api_key=env_vars['API_KEY'],
            api_secret=env_vars['API_SECRET']
        )

        # Test Deep Lynx connection first
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{env_vars['BASE_URL']}/health") as response:
                if response.status != 200:
                    raise Exception("Deep Lynx health check failed")
                logger.info("Deep Lynx connection verified")

        # Create API client with authentication
        api_client = ApiClient(base_config.configuration)
        
        # Test mock API connection
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8081/api/data") as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Retrieved {len(data['data'])} records from mock API")
                    print("\nMock API Data:")
                    print(data)
                else:
                    raise Exception(f"Mock API request failed: {response.status}")

    except ApiException as e:
        logger.error(f"API source demo failed: {e}")
        print(f"\nError processing API source: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\nError: {e}")
    finally:
        # Cleanup
        await runner.cleanup()
        logger.info("Stopped mock API server")

if __name__ == "__main__":
    asyncio.run(run_api_source_demo())