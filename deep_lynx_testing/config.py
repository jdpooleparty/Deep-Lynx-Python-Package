from typing import Optional
import os
from deep_lynx import Configuration, ApiClient, AuthenticationApi
from dotenv import load_dotenv

load_dotenv()

class DeepLynxConfig:
    def __init__(self):
        self.host = os.getenv('BASE_URL', 'http://localhost:8090')
        self.api_key = os.getenv('API_KEY')
        self.api_secret = os.getenv('API_SECRET')
        
        # Add debug logging
        print(f"Host: {self.host}")
        print(f"API Key exists: {bool(self.api_key)}")
        print(f"API Secret exists: {bool(self.api_secret)}")
        
        self._api_client: Optional[ApiClient] = None
        self._auth_token: Optional[str] = None

    def get_api_client(self) -> ApiClient:
        """Initialize and return an authenticated API client"""
        if not self._api_client:
            # Create base configuration
            configuration = Configuration()
            configuration.host = self.host
            
            # Initialize API client
            self._api_client = ApiClient(configuration)
            
            # Set default headers for all requests
            self._api_client.default_headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            # Authenticate and get token using the working method
            auth_api = AuthenticationApi(self._api_client)
            token = auth_api.retrieve_o_auth_token(
                x_api_key=self.api_key,
                x_api_secret=self.api_secret,
                x_api_expiry='1h'
            )
            
            # Set token in configuration
            self._api_client.configuration.access_token = token
            
        return self._api_client