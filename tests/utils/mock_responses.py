from typing import Dict, Any
import pytest
from deep_lynx.models.create_container_response import CreateContainerResponse

class MockDeepLynxResponses:
    """Mock API responses for testing"""
    @staticmethod
    def mock_container_response(container_id: str) -> Dict[str, Any]:
        return {
            "value": [{
                "id": container_id,
                "name": "test_container",
                "description": "Test container"
            }]
        }

    @staticmethod
    def mock_datasource_response(datasource_id: str) -> Dict[str, Any]:
        return {
            "value": {
                "id": datasource_id,
                "name": "test_datasource",
                "adapter_type": "standard",
                "active": True
            }
        } 