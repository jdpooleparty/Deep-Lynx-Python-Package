from pathlib import Path
import asyncio
import os
from dotenv import load_dotenv
import requests
import pandas as pd
from deep_lynx import (
    CreateContainerRequest,
    CreateDataSourceRequest,
    Configuration,
    ApiClient
)
from deep_lynx.rest import ApiException
from dev.pipeline.sources.api_source import APIDataSource
from dev.pipeline.transformers.base_transformer import DeepLynxTransformer
from dev.pipeline.loaders.deep_lynx_loader import DeepLynxLoader
from dev.pipeline.orchestrator import PipelineOrchestrator
from dev.pipeline.state import PipelineState, PipelineStatus
from dev.pipeline_config import PipelineConfig
from dev.config import DeepLynxConfig
from dev.utils.logging import setup_pipeline_logging
from datetime import datetime
import json

# Mock API data based on sample_manufacturing_data.csv
MOCK_API_DATA = {
    "equipment": [
        {"id": "EQ001", "equipment_name": "CNC Machine", "process_type": "Machining", "duration": 120, "status": "active"},
        {"id": "EQ002", "equipment_name": "3D Printer", "process_type": "Additive", "duration": 240, "status": "active"},
        {"id": "EQ003", "equipment_name": "Robot Arm", "process_type": "Assembly", "duration": 60, "status": "maintenance"},
        {"id": "EQ004", "equipment_name": "Laser Cutter", "process_type": "Cutting", "duration": 90, "status": "active"},
        {"id": "EQ005", "equipment_name": "Inspection Station", "process_type": "QC", "duration": 30, "status": "active"}
    ]
}

# Mock API server
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json

class MockAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/equipment'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(MOCK_API_DATA).encode())
        else:
            self.send_response(404)
            self.end_headers()

def start_mock_server(port=8000):
    server = HTTPServer(('localhost', port), MockAPIHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server

async def run_api_source_demo():
    """Demonstrate API data source functionality with Deep Lynx integration"""
    logger = setup_pipeline_logging(log_file=Path("logs/api_source_demo.log"))
    logger.info("Starting API source demo")
    
    # Start mock API server
    mock_server = start_mock_server()
    logger.info("Started mock API server")
    
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize Deep Lynx configuration
        base_config = DeepLynxConfig(
            base_url=os.getenv('BASE_URL', 'http://localhost:8090'),
            api_key=os.getenv('API_KEY'),
            api_secret=os.getenv('API_SECRET')
        )
        pipeline_config = PipelineConfig(base_config)
        
        # Configure API source with mock server
        api_config = {
            'base_url': 'http://localhost:8000',
            'endpoint': '/api/equipment',
            'headers': {'Content-Type': 'application/json'},
            'params': {'status': 'active', 'limit': 100}
        }
        
        # Initialize components
        source = APIDataSource(
            base_url=api_config['base_url'],
            endpoint=api_config['endpoint'],
            headers=api_config['headers'],
            params=api_config['params'],
            batch_size=100
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
        
        # Create container and data source
        containers_api = pipeline_config.get_containers_api()
        datasources_api = pipeline_config.get_datasources_api()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        container_name = f"API_Demo_Container_{timestamp}"
        
        container_response = containers_api.create_container(
            CreateContainerRequest(
                name=container_name,
                description="Container for API demo"
            )
        )
        container_id = container_response.value[0].id
        
        datasource_response = datasources_api.create_data_source(
            container_id=container_id,
            body=CreateDataSourceRequest(
                name="API Demo Source",
                adapter_type="standard",
                active=True
            )
        )
        datasource_id = datasource_response.value.id
        
        loader = DeepLynxLoader(
            pipeline_config,
            container_id=container_id,
            data_source_id=datasource_id
        )
        
        # Create and run orchestrator
        orchestrator = PipelineOrchestrator(
            source=source,
            transformer=transformer,
            loader=loader,
            state=PipelineState(status=PipelineStatus.INITIALIZED)
        )
        
        success = await orchestrator.run()
        
        if success:
            print("\nAPI Pipeline completed successfully!")
            print(f"Container Name: {container_name}")
            print(f"Container ID: {container_id}")
            print(f"Data Source ID: {datasource_id}")
            print("\nYou can view this data in the Deep Lynx UI at:")
            print(f"{base_config.configuration.host}/containers/{container_id}/data")
            print("\nOr query the data using:")
            print(f"{base_config.configuration.host}/containers/{container_id}/data/query")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}", exc_info=True)
        print(f"\nAPI request error: {e}")
    except Exception as e:
        logger.error(f"API source demo failed: {e}", exc_info=True)
        print(f"\nError processing API source: {e}")
    finally:
        # Cleanup
        mock_server.shutdown()
        mock_server.server_close()
        logger.info("Stopped mock API server")

if __name__ == "__main__":
    asyncio.run(run_api_source_demo())