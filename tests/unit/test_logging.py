import pytest
import logging
from pathlib import Path
from dev.utils.logging import setup_pipeline_logging

def test_logging_setup(tmp_path: Path):
    """Test logger configuration"""
    log_file = tmp_path / "test.log"
    logger = setup_pipeline_logging(log_level=logging.DEBUG, log_file=log_file)
    
    # Test logger configuration
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) == 2  # Console and file handlers
    
    # Test logging
    test_message = "Test log message"
    logger.info(test_message)
    
    # Verify message was written to file
    log_content = log_file.read_text()
    assert test_message in log_content 