from dev.config import DeepLynxConfig

def test_deep_lynx_connection():
    """Test the connection to Deep Lynx"""
    config = DeepLynxConfig()
    assert config.test_connection(), "Failed to connect to Deep Lynx"

if __name__ == "__main__":
    # This allows you to run this test directly
    config = DeepLynxConfig()
    config.test_connection() 