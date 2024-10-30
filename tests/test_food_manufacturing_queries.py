import pytest
from deep_lynx_testing.config import DeepLynxConfig
from deep_lynx.api.containers_api import ContainersApi

@pytest.fixture
def deep_lynx_client():
    """Fixture to create and return API client"""
    config = DeepLynxConfig()
    api_client = config.get_api_client()
    return ContainersApi(api_client)

def test_query_products(deep_lynx_client):
    """Test querying products and their relationships"""
    container_id = "74"
    
    # Query all products
    query = {
        "return_type": "graph",
        "type": "Product"
    }
    
    result = deep_lynx_client.query_container_data(
        container_id=container_id,
        query=query
    )
    
    assert result.value is not None
    assert len(result.value) > 0
    print(f"Found {len(result.value)} products")

def test_query_product_ingredients(deep_lynx_client):
    """Test querying product ingredients relationships"""
    container_id = "74"
    
    # Query products and their ingredients
    query = {
        "return_type": "graph",
        "type": "Product",
        "traverse_outbound": [{
            "type": "contains",
            "destination_type": "Ingredient"
        }]
    }
    
    result = deep_lynx_client.query_container_data(
        container_id=container_id,
        query=query
    )
    
    assert result.value is not None
    print("\nProduct-Ingredient Relationships:")
    for node in result.value:
        if 'properties' in node and 'product_name' in node['properties']:
            print(f"\nProduct: {node['properties']['product_name']}")
            if 'edges' in node:
                for edge in node['edges']:
                    if edge['destination_properties']['name']:
                        print(f"- Contains: {edge['destination_properties']['name']}")

def test_query_production_lines(deep_lynx_client):
    """Test querying production lines and their products"""
    container_id = "74"
    
    # Query production lines and their products
    query = {
        "return_type": "graph",
        "type": "ProductionLine",
        "traverse_inbound": [{
            "type": "manufactured_on",
            "origin_type": "Product"
        }]
    }
    
    result = deep_lynx_client.query_container_data(
        container_id=container_id,
        query=query
    )
    
    assert result.value is not None
    print("\nProduction Line Products:")
    for node in result.value:
        if 'properties' in node and 'name' in node['properties']:
            print(f"\nProduction Line: {node['properties']['name']}")
            if 'edges' in node:
                for edge in node['edges']:
                    if edge['origin_properties']['product_name']:
                        print(f"- Produces: {edge['origin_properties']['product_name']}") 