from typing import Optional
import os
from deep_lynx import Configuration, ApiClient, AuthenticationApi
from dotenv import load_dotenv

class DeepLynxConfig:
    """Configuration for Deep Lynx connection"""
    def __init__(
        self,
        base_url: str = "http://localhost:8090",
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None
    ):
        # Initialize configuration
        self.configuration = Configuration()
        self.configuration.host = base_url
        
        # Initialize API client
        self.api_client = ApiClient(self.configuration)
        
        # Set default headers
        self.api_client.default_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        # Get auth token
        auth_api = AuthenticationApi(self.api_client)
        token = auth_api.retrieve_o_auth_token(
            x_api_key=api_key,
            x_api_secret=api_secret,
            x_api_expiry='1h'
        )
        
        # Set token in configuration and headers
        self.api_client.configuration.access_token = token
        self.api_client.default_headers['Authorization'] = f'Bearer {token}'

    def get_api_client(self) -> ApiClient:
        """Get the configured API client"""
        return self.api_client

    def get_auth_api(self) -> AuthenticationApi:
        """Get the Authentication API instance"""
        return AuthenticationApi(self.api_client)