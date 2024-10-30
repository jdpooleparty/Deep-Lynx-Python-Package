from typing import Optional, List, Dict
from deep_lynx.models import (
    CreateContainerRequest,
    CreateContainerResponse,
    CreateMetatypeRequest,
    CreateMetatypeRelationshipRequest,
    CreateMetatypeRelationshipPairRequest
)
from .client import DeepLynxClient

class ContainersAPI:
    """API class for container operations"""
    def __init__(self):
        self.client = DeepLynxClient()
        
    def create_container(self, name: str, description: str) -> Optional[str]:
        """
        Create a new container in Deep Lynx
        
        Args:
            name: Name of the container
            description: Description of the container
            
        Returns:
            str: ID of the created container if successful, None otherwise
        """
        try:
            response = self.client.containers_api.create_container(
                CreateContainerRequest(
                    name=name,
                    description=description
                )
            )
            return response.value[0].id if response.value else None
            
        except Exception as e:
            print(f"Error creating container: {str(e)}")
            return None 
            
    def create_metatype(self, container_id: str, name: str, description: str, 
                       properties: List[Dict]) -> Optional[str]:
        """Create a new metatype in a container"""
        try:
            # First create the metatype without properties
            response = self.client.metatypes_api.create_metatype(
                container_id=container_id,
                body=CreateMetatypeRequest(
                    name=name,
                    description=description
                )
            )
            
            if not response.value:
                return None
            
            metatype_id = response.value[0].id
            
            # Then update it with properties
            self.client.metatypes_api.update_metatype(
                container_id=container_id,
                metatype_id=metatype_id,
                body={
                    "name": name,
                    "description": description,
                    "properties": properties
                }
            )
            
            return metatype_id
            
        except Exception as e:
            print(f"Error creating metatype: {str(e)}")
            return None
            
    def create_relationship(self, container_id: str, name: str, description: str) -> Optional[str]:
        """Create a new relationship type"""
        try:
            response = self.client.relationships_api.create_metatype_relationship(
                container_id=container_id,
                body=CreateMetatypeRelationshipRequest(
                    name=name,
                    description=description
                )
            )
            return response.value[0].id if response.value else None
            
        except Exception as e:
            print(f"Error creating relationship: {str(e)}")
            return None 