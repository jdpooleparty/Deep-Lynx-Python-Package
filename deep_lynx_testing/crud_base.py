from typing import Dict, List, Optional, Any
from deep_lynx import (
    ContainersApi, 
    MetatypesApi,
    MetatypeRelationshipsApi,
    GraphApi,
    CreateContainerRequest,
    CreateMetatypeRequest,
    CreateMetatypeRelationshipRequest,
    CreateOrUpdateNodesRequest,
    Node
)
from deep_lynx_testing.config import DeepLynxConfig

class DeepLynxCRUD:
    def __init__(self, config: DeepLynxConfig):
        self.api_client = config.get_api_client()
        self.containers_api = ContainersApi(self.api_client)
        self.metatypes_api = MetatypesApi(self.api_client)
        self.relationships_api = MetatypeRelationshipsApi(self.api_client)
        self.graph_api = GraphApi(self.api_client)
        self._container_id: Optional[str] = None

    async def create_container(self, name: str, description: str) -> str:
        """Create a new container and return its ID"""
        response = self.containers_api.create_container(
            CreateContainerRequest(
                name=name,
                description=description
            )
        )
        self._container_id = response.value[0].id
        return self._container_id

    async def create_metatype(self, name: str, description: str, properties: List[Dict]) -> str:
        """Create a new metatype and return its ID"""
        if not self._container_id:
            raise ValueError("Container ID not set. Create container first.")
            
        response = self.metatypes_api.create_metatype(
            container_id=self._container_id,
            body=CreateMetatypeRequest(
                name=name,
                description=description,
                properties=properties
            )
        )
        return response.value[0].id

    async def create_relationship(
        self, 
        name: str, 
        description: str,
        source_metatype_id: str,
        destination_metatype_id: str
    ) -> str:
        """Create a new metatype relationship and return its ID"""
        if not self._container_id:
            raise ValueError("Container ID not set. Create container first.")
            
        response = self.relationships_api.create_metatype_relationship(
            container_id=self._container_id,
            body=CreateMetatypeRelationshipRequest(
                name=name,
                description=description,
                source_metatype_id=source_metatype_id,
                destination_metatype_id=destination_metatype_id
            )
        )
        return response.value[0].id

    async def create_node(
        self,
        metatype_id: str,
        properties: Dict[str, Any]
    ) -> str:
        """Create a new node and return its ID"""
        if not self._container_id:
            raise ValueError("Container ID not set. Create container first.")
            
        response = self.graph_api.create_or_update_nodes(
            container_id=self._container_id,
            body=CreateOrUpdateNodesRequest(
                nodes=[Node(
                    metatype_id=metatype_id,
                    properties=properties
                )]
            )
        )
        return response.value[0].id

    async def get_node(self, node_id: str) -> Dict:
        """Retrieve a node by ID"""
        if not self._container_id:
            raise ValueError("Container ID not set. Create container first.")
            
        response = self.graph_api.retrieve_node(
            container_id=self._container_id,
            node_id=node_id
        )
        return response.value

    async def update_node(
        self,
        node_id: str,
        properties: Dict[str, Any]
    ) -> bool:
        """Update a node's properties"""
        if not self._container_id:
            raise ValueError("Container ID not set. Create container first.")
            
        response = self.graph_api.create_or_update_nodes(
            container_id=self._container_id,
            body=CreateOrUpdateNodesRequest(
                nodes=[Node(
                    id=node_id,
                    properties=properties
                )]
            )
        )
        return bool(response.value)

    async def delete_node(self, node_id: str) -> bool:
        """Delete a node by ID"""
        if not self._container_id:
            raise ValueError("Container ID not set. Create container first.")
            
        response = self.graph_api.archive_node(
            container_id=self._container_id,
            node_id=node_id
        )
        return bool(response.value) 