from typing import Optional
import os
from deep_lynx import Configuration, ApiClient, AuthenticationApi
from dotenv import load_dotenv

load_dotenv()

class DeepLynxConfig:
    """Configuration class for Deep Lynx API connection"""
    def __init__(self):
        self.host = os.getenv('BASE_URL')
        self.api_key = os.getenv('API_KEY')
        self.api_secret = os.getenv('API_SECRET')
        
        if not all([self.host, self.api_key, self.api_secret]):
            raise ValueError("Missing required environment variables. Please check .env file")
        
        self._api_client: Optional[ApiClient] = None

    def get_api_client(self) -> ApiClient:
        """Initialize and return an authenticated API client"""
        if not self._api_client:
            # Create base configuration
            configuration = Configuration()
            configuration.host = self.host
            
            # Initialize API client
            self._api_client = ApiClient(configuration)
            
            # Set default headers
            self._api_client.default_headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            # Authenticate and get token
            auth_api = AuthenticationApi(self._api_client)
            token = auth_api.retrieve_o_auth_token(
                x_api_key=self.api_key,
                x_api_secret=self.api_secret,
                x_api_expiry='1h'
            )
            
            # Set token in configuration and headers
            self._api_client.configuration.access_token = token
            self._api_client.default_headers['Authorization'] = f'Bearer {token}'
            
        return self._api_client 

    def test_connection(self) -> bool:
        """
        Test the connection to Deep Lynx
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            # Try to get an API client (this will attempt authentication)
            api_client = self.get_api_client()
            
            # If we got here, authentication was successful
            print("✓ Successfully authenticated with Deep Lynx")
            print(f"✓ Connected to: {self.host}")
            return True
            
        except Exception as e:
            print("✗ Failed to connect to Deep Lynx")
            print(f"Error: {str(e)}")
            return False