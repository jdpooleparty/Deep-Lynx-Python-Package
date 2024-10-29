"""
Test file for creating and populating an ontology in Deep Lynx
This demonstrates creating a container, ontology structure, and importing mapped data
"""

import pytest
import asyncio
from deep_lynx_testing.config import DeepLynxConfig
from deep_lynx.api.containers_api import ContainersApi
from deep_lynx.api.data_sources_api import DataSourcesApi
from deep_lynx.api.metatypes_api import MetatypesApi
from deep_lynx.api.metatype_relationships_api import MetatypeRelationshipsApi
from deep_lynx.api.metatype_relationship_pairs_api import MetatypeRelationshipPairsApi
from deep_lynx.models.create_container_request import CreateContainerRequest
from deep_lynx.models.create_data_source_request import CreateDataSourceRequest
from deep_lynx.models.create_metatype_request import CreateMetatypeRequest
from deep_lynx.models.create_metatype_relationship_request import CreateMetatypeRelationshipRequest
from deep_lynx.rest import ApiException

@pytest.fixture
async def deep_lynx_client():
    """Fixture to create and return API clients"""
    config = DeepLynxConfig()
    api_client = config.get_api_client()
    
    # Set Authorization header with token
    token = api_client.configuration.access_token
    api_client.default_headers['Authorization'] = f'Bearer {token}'
    
    # Initialize APIs
    apis = {
        'containers_api': ContainersApi(api_client),
        'metatypes_api': MetatypesApi(api_client),
        'relationships_api': MetatypeRelationshipsApi(api_client),
        'relationship_pairs_api': MetatypeRelationshipPairsApi(api_client),
        'datasources_api': DataSourcesApi(api_client)
    }
    
    try:
        yield apis
    finally:
        # Cleanup will happen in the test
        pass

@pytest.mark.asyncio
async def test_create_ontology_and_import(deep_lynx_client):
    """Test creating an ontology structure and importing mapped data"""
    container_id = None  # Initialize outside try block
    try:
        # Get the API clients from the async generator
        apis = await anext(deep_lynx_client)
        
        # 1. Create Container
        container_response = apis['containers_api'].create_container(
            CreateContainerRequest(
                name="Manufacturing Ontology",
                description="Ontology for manufacturing processes and equipment"
            )
        )
        container_id = container_response.value[0].id

        # 2. Create Metatypes (Classes)
        # Equipment class
        equipment_type = apis['metatypes_api'].create_metatype(
            container_id=container_id,
            body=CreateMetatypeRequest(
                name="Equipment",
                description="Manufacturing equipment"
            )
        )

        # Add properties to Equipment metatype
        equipment_properties = [
            {
                "name": "equipment_id",
                "required": True,
                "data_type": "string",
                "description": "Unique identifier for equipment"
            },
            {
                "name": "name",
                "required": True,
                "data_type": "string",
                "description": "Equipment name"
            },
            {
                "name": "type",
                "required": True,
                "data_type": "string",
                "description": "Type of equipment"
            }
        ]
        apis['metatypes_api'].update_metatype(
            container_id=container_id,
            metatype_id=equipment_type.value[0].id,
            body={
                "name": "Equipment",
                "description": "Manufacturing equipment",
                "properties": equipment_properties
            }
        )
        await asyncio.sleep(1)  # Add delay after Equipment update

        # Process class
        process_type = apis['metatypes_api'].create_metatype(
            container_id=container_id,
            body=CreateMetatypeRequest(
                name="Process",
                description="Manufacturing process"
            )
        )

        # Add properties to Process metatype
        process_properties = [
            {
                "name": "process_id",
                "required": True,
                "data_type": "string",
                "description": "Unique identifier for process"
            },
            {
                "name": "name",
                "required": True,
                "data_type": "string",
                "description": "Process name"
            },
            {
                "name": "duration",
                "required": True,
                "data_type": "number",
                "description": "Process duration in minutes"
            }
        ]
        apis['metatypes_api'].update_metatype(
            container_id=container_id,
            metatype_id=process_type.value[0].id,
            body={
                "name": "Process",
                "description": "Manufacturing process",
                "properties": process_properties
            }
        )
        await asyncio.sleep(1)  # Add delay after Process update

        # 3. Create Relationships
        # First create the relationship type without properties
        relationship = apis['relationships_api'].create_metatype_relationship(
            container_id=container_id,
            body=CreateMetatypeRelationshipRequest(
                name="performs",
                description="Equipment performs Process"
            )
        )
        await asyncio.sleep(1)  # Add delay after relationship creation

        # Then update the relationship to add properties
        relationship_update = apis['relationships_api'].update_metatype_relationship(
            container_id=container_id,
            relationship_id=relationship.value[0].id,
            body={
                "name": "performs",
                "description": "Equipment performs Process",
                "properties": [
                    {
                        "name": "efficiency",
                        "required": True,
                        "data_type": "number",
                        "description": "Process efficiency percentage"
                    }
                ]
            }
        )
        await asyncio.sleep(2)  # Increase delay after relationship update

        # Then create the relationship pair
        relationship_pair = apis['relationship_pairs_api'].create_metatype_relationship_pair(
            container_id=container_id,
            body={
                "name": "performs",
                "description": "Equipment performs Process",
                "relationship_type": "many:many",
                "origin_metatype_id": str(equipment_type.value[0].id),
                "destination_metatype_id": str(process_type.value[0].id),
                "metatype_relationship_id": str(relationship.value[0].id),
                "container_id": str(container_id),
                "ontology_version": str(container_id),
                "relationship_key": "performs",
                "originMetatype": {
                    "name": "Equipment",
                    "description": "Manufacturing equipment",
                    "id": str(equipment_type.value[0].id)
                },
                "destinationMetatype": {
                    "name": "Process",
                    "description": "Manufacturing process",
                    "id": str(process_type.value[0].id)
                },
                "relationship": {
                    "name": "performs",
                    "description": "Equipment performs Process",
                    "id": str(relationship.value[0].id)
                }
            }
        )
        await asyncio.sleep(2)  # Keep delay after pair creation

        # Add delay after relationship creation and update
        await asyncio.sleep(1)

        # 4. Create Data Source
        datasource = apis['datasources_api'].create_data_source(
            container_id=container_id,
            body=CreateDataSourceRequest(
                name="Manufacturing Data",
                adapter_type="standard",
                active=True
            )
        )

        # 5. Import Data with Mappings
        import_data = {
            "nodes": [
                {
                    "id": "EQ001",
                    "metatype": "Equipment",
                    "properties": {
                        "equipment_id": "EQ001",
                        "name": "CNC Machine",
                        "type": "Machining"
                    }
                },
                {
                    "id": "EQ002",
                    "metatype": "Equipment",
                    "properties": {
                        "equipment_id": "EQ002",
                        "name": "3D Printer",
                        "type": "Additive Manufacturing"
                    }
                },
                {
                    "id": "P001",
                    "metatype": "Process",
                    "properties": {
                        "process_id": "P001",
                        "name": "Part Milling",
                        "duration": 45
                    }
                },
                {
                    "id": "P002",
                    "metatype": "Process",
                    "properties": {
                        "process_id": "P002",
                        "name": "3D Printing",
                        "duration": 180
                    }
                }
            ],
            "edges": [
                {
                    "relationship_type": "performs",
                    "from_node": "EQ001",
                    "to_node": "P001",
                    "properties": {
                        "efficiency": 95
                    }
                },
                {
                    "relationship_type": "performs",
                    "from_node": "EQ002",
                    "to_node": "P002",
                    "properties": {
                        "efficiency": 88
                    }
                }
            ]
        }

        # Perform the import
        import_response = apis['datasources_api'].create_manual_import(
            container_id=container_id,
            data_source_id=datasource.value.id,
            body=import_data
        )

        # Verify import was created
        assert import_response is not None
        assert 'value' in import_response
        assert 'id' in import_response['value']

        # Check import status
        imports_response = apis['datasources_api'].list_imports_for_data_source(
            container_id=container_id,
            data_source_id=datasource.value.id
        )

        # Find our import
        import_status = None
        for import_item in imports_response.value:
            if import_item._id == import_response['value']['id']:
                import_status = import_item
                break

        assert import_status is not None
        assert '_status' in vars(import_status)
        assert import_status._status in ['ready', 'completed', 'processing']

    except ApiException as e:
        pytest.fail(f"API Exception occurred: {str(e)}")
    finally:
        # Cleanup
        if container_id:  # Only attempt cleanup if container was created
            try:
                apis['containers_api'].archive_container(container_id)
            except ApiException:
                pass
