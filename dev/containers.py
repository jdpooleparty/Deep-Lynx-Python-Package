from typing import Optional, List, Dict, Any
from deep_lynx.models import (
    CreateContainerRequest,
    CreateContainerResponse,
    CreateMetatypeRequest,
    CreateMetatypeRelationshipRequest,
    CreateMetatypeRelationshipPairRequest,
    UpdateContainerRequest,
    UpdateMetatypeRequest
)
from .client import DeepLynxClient
from datetime import datetime
from time import sleep

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
            
            if not response.value:
                return None
                
            container_id = str(response.value[0].id)
            
            # Verify container creation with retries
            max_retries = 5
            for attempt in range(max_retries):
                sleep(2)  # Longer delay between attempts
                verify_response = self.client.containers_api.list_containers()
                if verify_response.value:
                    if any(str(c.id) == container_id for c in verify_response.value):
                        return container_id
                        
            return None
            
        except Exception as e:
            print(f"Error creating container: {str(e)}")
            return None
            
    def create_metatype(self, container_id: str, name: str, description: str, 
                       properties: List[Dict]) -> Optional[str]:
        """Create a new metatype in a container"""
        try:
            # Format properties for creation
            formatted_properties = []
            for prop in properties:
                formatted_prop = {
                    "name": prop["name"],
                    "description": prop["description"],
                    "required": prop["required"],
                    "property_type": prop["data_type"],
                    "validation": {},
                    "options": {}
                }
                formatted_properties.append(formatted_prop)
            
            # Create metatype with properties
            response = self.client.metatypes_api.create_metatype(
                container_id=container_id,
                body=CreateMetatypeRequest(
                    name=name,
                    description=description,
                    properties=formatted_properties  # Include properties in creation
                )
            )
            
            if not response.value:
                return None
            
            metatype_id = str(response.value[0].id)
            
            # Verify creation with retries
            max_retries = 3
            for attempt in range(max_retries):
                sleep(1)
                verify = self.get_metatype(container_id, metatype_id)
                if verify and verify["properties"]:
                    return metatype_id
                    
            return None
            
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
            
    def list_containers(self) -> List[Dict[str, Any]]:
        """List all containers"""
        try:
            # Add retry logic with delay
            max_retries = 3
            containers = []
            
            for attempt in range(max_retries):
                response = self.client.containers_api.list_containers()
                if response.value:
                    containers = [
                        {
                            "id": str(c.id),
                            "name": c.name,
                            "description": c.description,
                            "created_at": c.created_at
                        }
                        for c in response.value
                    ]
                    if containers:
                        break
                print(f"Attempt {attempt + 1}: Found {len(containers)} containers")
                sleep(2)  # Longer delay between retries
                
            print(f"Found containers: {[(c['id'], c['name']) for c in containers]}")
            return containers
                
        except Exception as e:
            print(f"Error listing containers: {str(e)}")
            return []
            
    def get_container(self, container_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific container by ID"""
        try:
            # Change to retrieve_container
            response = self.client.containers_api.retrieve_container(container_id)
            if not response.value:
                return None
                
            container = response.value[0]
            return {
                "id": str(container.id),  # Convert ID to string
                "name": container.name,
                "description": container.description,
                "created_at": container.created_at
            }
            
        except Exception as e:
            print(f"Error retrieving container: {str(e)}")
            return None
            
    def update_container(self, container_id: str, name: str, description: str) -> bool:
        """Update a container's information"""
        try:
            self.client.containers_api.update_container(
                container_id=container_id,
                body=UpdateContainerRequest(
                    name=name,
                    description=description
                )
            )
            return True
            
        except Exception as e:
            print(f"Error updating container: {str(e)}")
            return False
            
    def list_metatypes(self, container_id: str) -> List[Dict[str, Any]]:
        """List all metatypes in a container"""
        try:
            response = self.client.metatypes_api.list_metatypes(container_id)
            return [
                {
                    "id": metatype.id,
                    "name": metatype.name,
                    "description": metatype.description,
                    "properties": getattr(metatype, 'property_names', [])
                }
                for metatype in response.value
            ] if response.value else []
            
        except Exception as e:
            print(f"Error listing metatypes: {str(e)}")
            return []
            
    def get_metatype(self, container_id: str, metatype_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific metatype by ID"""
        try:
            response = self.client.metatypes_api.list_metatypes(container_id)
            if not response.value:
                return None
                
            metatype = next((m for m in response.value if str(m.id) == str(metatype_id)), None)
            if not metatype:
                return None
                
            return {
                "id": str(metatype.id),
                "name": metatype.name,
                "description": metatype.description,
                "properties": getattr(metatype, 'properties', [])  # Changed from property_names to properties
            }
                
        except Exception as e:
            print(f"Error retrieving metatype: {str(e)}")
            return None
            
    def update_metatype(
        self, 
        container_id: str, 
        metatype_id: str, 
        name: str, 
        description: str, 
        properties: List[Dict]
    ) -> bool:
        """Update a metatype's information and properties"""
        try:
            # Format properties correctly
            formatted_properties = []
            for prop in properties:
                formatted_prop = {
                    "name": prop["name"],
                    "description": prop["description"],
                    "required": prop["required"],
                    "property_type": prop["data_type"],
                    "validation": {},
                    "options": {}
                }
                formatted_properties.append(formatted_prop)
            
            # Create update request without container_id
            update_request = UpdateMetatypeRequest(
                name=name,
                description=description
            )
            
            # Set properties after initialization
            update_request.properties = formatted_properties
            
            # Perform update
            response = self.client.metatypes_api.update_metatype(
                container_id=container_id,
                metatype_id=metatype_id,
                body=update_request
            )
            
            # Verify the update with retries
            max_retries = 3
            for attempt in range(max_retries):
                sleep(1)  # Wait between attempts
                updated = self.get_metatype(container_id, metatype_id)
                if updated and updated["name"] == name:
                    return True
                    
            return False
            
        except Exception as e:
            print(f"Error updating metatype: {str(e)}")
            return False
            
    def archive_metatype(self, container_id: str, metatype_id: str) -> bool:
        """Archive a metatype"""
        try:
            self.client.metatypes_api.archive_metatype(
                container_id=container_id,
                metatype_id=metatype_id
            )
            return True
            
        except Exception as e:
            print(f"Error archiving metatype: {str(e)}")
            return False