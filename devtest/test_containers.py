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

if __name__ == "__main__":
    test_container_operations()
    test_error_handling() 