import pytest
from dev.containers import ContainersAPI
from datetime import datetime

def test_container_operations():
    """Test container, metatype, and relationship operations"""
    print("\nTesting Deep Lynx operations...")
    api = ContainersAPI()
    
    # Generate unique name using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    container_name = f"test_container_{timestamp}"
    
    # Test creating a container
    print("Creating container...")
    container_id = api.create_container(
        name=container_name,
        description="A test container created by the API"
    )
    assert container_id is not None, "Container creation failed"
    print(f"✓ Container created successfully with ID: {container_id}")
    
    # Test creating a metatype
    print("Creating metatype...")
    properties = [
        {
            "name": "test_property",
            "required": True,
            "data_type": "string",
            "description": "A test property"
        },
        {
            "name": "numeric_property",
            "required": False,
            "data_type": "number",
            "description": "A numeric test property"
        }
    ]
    
    metatype_id = api.create_metatype(
        container_id=container_id,
        name="test_metatype",
        description="A test metatype",
        properties=properties
    )
    assert metatype_id is not None, "Metatype creation failed"
    print(f"✓ Metatype created successfully with ID: {metatype_id}")
    
    # Test creating a relationship
    print("Creating relationship...")
    relationship_id = api.create_relationship(
        container_id=container_id,
        name="test_relationship",
        description="A test relationship type"
    )
    assert relationship_id is not None, "Relationship creation failed"
    print(f"✓ Relationship created successfully with ID: {relationship_id}")
    
    # Clean up - archive the container
    try:
        api.client.containers_api.archive_container(container_id)
        print("✓ Container and related items archived successfully")
    except Exception as e:
        print(f"Warning: Failed to clean up test container: {str(e)}")

def test_error_handling():
    """Test error handling in the API"""
    api = ContainersAPI()
    
    # Test creating metatype without container
    print("\nTesting error handling...")
    invalid_container_id = "nonexistent_id"
    metatype_result = api.create_metatype(
        container_id=invalid_container_id,
        name="test_metatype",
        description="This should fail",
        properties=[{"name": "test", "required": True, "data_type": "string"}]
    )
    assert metatype_result is None, "Expected metatype creation to fail with invalid container ID"
    print("✓ Error handling working as expected")

def test_container_retrieval():
    """Test container listing and retrieval operations"""
    print("\nTesting container retrieval operations...")
    api = ContainersAPI()
    
    # Create a test container
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    container_name = f"test_container_{timestamp}"
    container_id = api.create_container(
        name=container_name,
        description="Test container for retrieval operations"
    )
    assert container_id is not None, "Container creation failed"
    
    # Test listing containers
    containers = api.list_containers()
    assert len(containers) > 0, "No containers found"
    assert any(c["id"] == container_id for c in containers), "Created container not found in list"
    print("✓ Container listing successful")
    
    # Test getting specific container
    container = api.get_container(container_id)
    assert container is not None, "Failed to retrieve container"
    assert container["name"] == container_name, "Container name mismatch"
    print("✓ Container retrieval successful")
    
    # Test updating container
    updated_name = f"updated_{container_name}"
    success = api.update_container(
        container_id=container_id,
        name=updated_name,
        description="Updated description"
    )
    assert success, "Container update failed"
    
    # Verify update
    updated_container = api.get_container(container_id)
    assert updated_container["name"] == updated_name, "Container update not reflected"
    print("✓ Container update successful")
    
    # Clean up
    try:
        api.client.containers_api.archive_container(container_id)
        print("✓ Test container archived successfully")
    except Exception as e:
        print(f"Warning: Failed to clean up test container: {str(e)}")

def test_metatype_operations():
    """Test metatype listing, retrieval, and update operations"""
    print("\nTesting metatype operations...")
    api = ContainersAPI()
    
    # Create a test container
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    container_id = api.create_container(
        name=f"test_container_{timestamp}",
        description="Test container for metatype operations"
    )
    assert container_id is not None, "Container creation failed"
    
    # Create a test metatype
    properties = [
        {
            "name": "test_property",
            "required": True,
            "data_type": "string",
            "description": "Test property"
        }
    ]
    
    metatype_id = api.create_metatype(
        container_id=container_id,
        name="test_metatype",
        description="Test metatype",
        properties=properties
    )
    assert metatype_id is not None, "Metatype creation failed"
    
    # Test listing metatypes
    metatypes = api.list_metatypes(container_id)
    assert len(metatypes) > 0, "No metatypes found"
    assert any(m["id"] == metatype_id for m in metatypes), "Created metatype not found in list"
    print("✓ Metatype listing successful")
    
    # Test getting specific metatype
    metatype = api.get_metatype(container_id, metatype_id)
    assert metatype is not None, "Failed to retrieve metatype"
    assert metatype["name"] == "test_metatype", "Metatype name mismatch"
    print("✓ Metatype retrieval successful")
    
    # Test updating metatype
    updated_properties = properties + [{
        "name": "new_property",
        "required": False,
        "data_type": "number",
        "description": "New test property"
    }]
    
    success = api.update_metatype(
        container_id=container_id,
        metatype_id=metatype_id,
        name="updated_test_metatype",
        description="Updated test metatype",
        properties=updated_properties
    )
    assert success, "Metatype update failed"
    
    # Verify update
    updated_metatype = api.get_metatype(container_id, metatype_id)
    assert updated_metatype["name"] == "updated_test_metatype", "Metatype update not reflected"
    assert len(updated_metatype["properties"]) == 2, "Metatype properties not updated"
    print("✓ Metatype update successful")
    
    # Clean up
    try:
        api.client.containers_api.archive_container(container_id)
        print("✓ Test container and metatypes archived successfully")
    except Exception as e:
        print(f"Warning: Failed to clean up test container: {str(e)}")

if __name__ == "__main__":
    test_container_operations()
    test_error_handling()
    test_container_retrieval()
    test_metatype_operations() 