import pytest
from deep_lynx_testing.config import DeepLynxConfig
from deep_lynx_testing.crud_base import DeepLynxCRUD

@pytest.fixture
async def deep_lynx():
    """Fixture to create and return a DeepLynxCRUD instance"""
    config = DeepLynxConfig()
    crud = DeepLynxCRUD(config)
    # Create container and await it
    await crud.create_container(
        name="test_container",
        description="Test container for CRUD operations"
    )
    try:
        yield crud  # Use yield instead of return for fixtures
    finally:
        # Add cleanup here if needed
        pass

@pytest.mark.asyncio
async def test_metatype_crud(deep_lynx):
    crud = await anext(deep_lynx)  # Get the CRUD instance from the async generator
    # Create a test metatype
    properties = [
        {
            "name": "test_property",
            "required": True,
            "data_type": "string",
            "description": "Test property"
        }
    ]
    
    metatype_id = await crud.create_metatype(
        name="test_metatype",
        description="Test metatype",
        properties=properties
    )
    
    assert metatype_id is not None

@pytest.mark.asyncio
async def test_node_crud(deep_lynx):
    crud = await anext(deep_lynx)  # Get the CRUD instance from the async generator
    # First create a metatype
    properties = [
        {
            "name": "test_property",
            "required": True,
            "data_type": "string",
            "description": "Test property"
        }
    ]
    
    metatype_id = await crud.create_metatype(
        name="test_metatype",
        description="Test metatype",
        properties=properties
    )
    
    # Create a node
    node_properties = {
        "test_property": "test_value"
    }
    
    node_id = await crud.create_node(
        metatype_id=metatype_id,
        properties=node_properties
    )
    
    assert node_id is not None
    
    # Retrieve the node
    node = await crud.get_node(node_id)
    assert node["properties"]["test_property"] == "test_value"
    
    # Update the node
    updated_properties = {
        "test_property": "updated_value"
    }
    
    update_success = await crud.update_node(
        node_id=node_id,
        properties=updated_properties
    )
    
    assert update_success
    
    # Verify update
    updated_node = await crud.get_node(node_id)
    assert updated_node["properties"]["test_property"] == "updated_value"
    
    # Delete the node
    delete_success = await crud.delete_node(node_id)
    assert delete_success