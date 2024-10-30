import pytest
import pandas as pd
from pathlib import Path
from datetime import datetime
from deep_lynx_testing.config import DeepLynxConfig
from deep_lynx.api.containers_api import ContainersApi
from deep_lynx.api.data_sources_api import DataSourcesApi
from deep_lynx.api.metatypes_api import MetatypesApi
from deep_lynx.api.metatype_relationships_api import MetatypeRelationshipsApi
from deep_lynx.api.metatype_relationship_pairs_api import MetatypeRelationshipPairsApi
from deep_lynx.models.create_metatype_request import CreateMetatypeRequest
from deep_lynx.models.create_metatype_relationship_request import CreateMetatypeRelationshipRequest
from deep_lynx.models.create_data_source_request import CreateDataSourceRequest
from deep_lynx.rest import ApiException

@pytest.fixture
async def deep_lynx_client():
    """Fixture to create and return API clients"""
    config = DeepLynxConfig()
    api_client = config.get_api_client()
    
    # Initialize APIs
    apis = {
        'metatypes_api': MetatypesApi(api_client),
        'relationships_api': MetatypeRelationshipsApi(api_client),
        'relationship_pairs_api': MetatypeRelationshipPairsApi(api_client),
        'datasources_api': DataSourcesApi(api_client)
    }
    
    return apis

@pytest.mark.asyncio
async def test_create_food_manufacturing_ontology(deep_lynx_client):
    """Test creating a food manufacturing ontology and importing data"""
    container_id = "74"  # Using the specified container
    apis = deep_lynx_client
    
    try:
        # 1. Create Product Metatype
        product_type = apis['metatypes_api'].create_metatype(
            container_id=container_id,
            body=CreateMetatypeRequest(
                name="Product",
                description="Food or beverage product"
            )
        )
        
        # Add properties to Product metatype
        product_properties = [
            {
                "name": "product_id",
                "required": True,
                "data_type": "string",
                "description": "Unique product identifier"
            },
            {
                "name": "product_name",
                "required": True,
                "data_type": "string",
                "description": "Product name"
            },
            {
                "name": "product_type",
                "required": True,
                "data_type": "string",
                "description": "Type of product"
            },
            {
                "name": "batch_number",
                "required": True,
                "data_type": "string",
                "description": "Production batch number"
            },
            {
                "name": "quantity",
                "required": True,
                "data_type": "number",
                "description": "Production quantity"
            },
            {
                "name": "unit",
                "required": True,
                "data_type": "string",
                "description": "Unit of measurement"
            },
            {
                "name": "quality_score",
                "required": True,
                "data_type": "number",
                "description": "Quality assessment score"
            }
        ]
        
        apis['metatypes_api'].update_metatype(
            container_id=container_id,
            metatype_id=product_type.value[0].id,
            body={
                "name": "Product",
                "description": "Food or beverage product",
                "properties": product_properties
            }
        )

        # 2. Create Production Line Metatype
        line_type = apis['metatypes_api'].create_metatype(
            container_id=container_id,
            body=CreateMetatypeRequest(
                name="ProductionLine",
                description="Manufacturing production line"
            )
        )
        
        # Add properties to ProductionLine metatype
        line_properties = [
            {
                "name": "line_id",
                "required": True,
                "data_type": "string",
                "description": "Production line identifier"
            },
            {
                "name": "name",
                "required": True,
                "data_type": "string",
                "description": "Line name"
            }
        ]
        
        apis['metatypes_api'].update_metatype(
            container_id=container_id,
            metatype_id=line_type.value[0].id,
            body={
                "name": "ProductionLine",
                "description": "Manufacturing production line",
                "properties": line_properties
            }
        )

        # 3. Create Ingredient Metatype
        ingredient_type = apis['metatypes_api'].create_metatype(
            container_id=container_id,
            body=CreateMetatypeRequest(
                name="Ingredient",
                description="Product ingredient"
            )
        )
        
        # Add properties to Ingredient metatype
        ingredient_properties = [
            {
                "name": "name",
                "required": True,
                "data_type": "string",
                "description": "Ingredient name"
            }
        ]
        
        apis['metatypes_api'].update_metatype(
            container_id=container_id,
            metatype_id=ingredient_type.value[0].id,
            body={
                "name": "Ingredient",
                "description": "Product ingredient",
                "properties": ingredient_properties
            }
        )

        # 4. Create Relationships
        # Product is manufactured on ProductionLine
        manufactured_on = apis['relationships_api'].create_metatype_relationship(
            container_id=container_id,
            body=CreateMetatypeRelationshipRequest(
                name="manufactured_on",
                description="Product is manufactured on production line"
            )
        )

        # Product contains Ingredient
        contains = apis['relationships_api'].create_metatype_relationship(
            container_id=container_id,
            body=CreateMetatypeRelationshipRequest(
                name="contains",
                description="Product contains ingredient"
            )
        )

        # 5. Create Relationship Pairs
        # Product -> ProductionLine
        apis['relationship_pairs_api'].create_metatype_relationship_pair(
            container_id=container_id,
            body={
                "name": "manufactured_on",
                "description": "Product is manufactured on production line",
                "relationship_type": "one:many",
                "origin_metatype_id": str(product_type.value[0].id),
                "destination_metatype_id": str(line_type.value[0].id),
                "metatype_relationship_id": str(manufactured_on.value[0].id)
            }
        )

        # Product -> Ingredient
        apis['relationship_pairs_api'].create_metatype_relationship_pair(
            container_id=container_id,
            body={
                "name": "contains",
                "description": "Product contains ingredient",
                "relationship_type": "many:many",
                "origin_metatype_id": str(product_type.value[0].id),
                "destination_metatype_id": str(ingredient_type.value[0].id),
                "metatype_relationship_id": str(contains.value[0].id)
            }
        )

        # 6. Create Data Source
        datasource = apis['datasources_api'].create_data_source(
            container_id=container_id,
            body=CreateDataSourceRequest(
                name="Food Manufacturing Data",
                adapter_type="standard",
                active=True
            )
        )

        # 7. Import Data
        # Read CSV data
        csv_path = Path(__file__).parent / "data" / "food_manufacturing_data.csv"
        df = pd.read_csv(csv_path)
        
        # Prepare nodes and edges for import
        nodes = []
        edges = []
        
        # Create production line nodes
        unique_lines = df['production_line'].unique()
        for line in unique_lines:
            nodes.append({
                "id": line,
                "metatype": "ProductionLine",
                "properties": {
                    "line_id": line,
                    "name": line
                }
            })

        # Create ingredient nodes and product nodes with relationships
        for _, row in df.iterrows():
            # Product node
            product_node = {
                "id": row['product_id'],
                "metatype": "Product",
                "properties": {
                    "product_id": row['product_id'],
                    "product_name": row['product_name'],
                    "product_type": row['product_type'],
                    "batch_number": row['batch_number'],
                    "quantity": float(row['quantity']),
                    "unit": row['unit'],
                    "quality_score": float(row['quality_score'])
                }
            }
            nodes.append(product_node)

            # Add manufactured_on relationship
            edges.append({
                "relationship_type": "manufactured_on",
                "from_node": row['product_id'],
                "to_node": row['production_line']
            })

            # Create ingredient nodes and relationships
            ingredients = row['ingredients'].split('|')
            for ingredient in ingredients:
                ingredient_id = f"ING_{ingredient.strip()}"
                
                # Add ingredient node if not already added
                nodes.append({
                    "id": ingredient_id,
                    "metatype": "Ingredient",
                    "properties": {
                        "name": ingredient.strip()
                    }
                })

                # Add contains relationship
                edges.append({
                    "relationship_type": "contains",
                    "from_node": row['product_id'],
                    "to_node": ingredient_id
                })

        # Perform the import
        import_data = {
            "nodes": nodes,
            "edges": edges
        }

        import_response = apis['datasources_api'].create_manual_import(
            container_id=container_id,
            data_source_id=datasource.value.id,
            body=import_data
        )

        assert import_response is not None
        print(f"Successfully imported {len(nodes)} nodes and {len(edges)} edges")

    except ApiException as e:
        pytest.fail(f"API Exception occurred: {str(e)}") 