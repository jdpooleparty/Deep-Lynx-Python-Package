import os
from pathlib import Path

# Test configuration
TEST_DATA_DIR = Path(__file__).parent / "data"
TEST_LOG_DIR = Path(__file__).parent / "logs"

# Create directories if they don't exist
TEST_DATA_DIR.mkdir(exist_ok=True)
TEST_LOG_DIR.mkdir(exist_ok=True)

# Test constants
BATCH_SIZE = 100
TEST_CONTAINER_NAME = "test_container"
TEST_DATASOURCE_NAME = "test_datasource" 