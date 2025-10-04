"""
Unit tests for settings module
"""

import pytest
import json
from pathlib import Path
from src.config.settings import Settings

class TestSettings:
    """Test cases for Settings class"""

def test_default_settings(self):
    """Test default configuration loading"""
    settings = Settings(config_path="test_config.json")
    
    assert settings.camera_id == 0
    assert settings.capture_interval == 3.0
    assert settings.llm_model == "llama3.1"
    
    # Cleanup
    Path("test_config.json").unlink(missing_ok=True)

def test_custom_settings(self):
    """Test custom configuration loading"""
    test_config = {
        "camera_id": 1,
        "capture_interval": 5.0,
        "llm_model": "phi3"
    }
    
    with open("test_config.json", "w") as f:
        json.dump(test_config, f)
    
    settings = Settings(config_path="test_config.json")
    
    assert settings.camera_id == 1
    assert settings.capture_interval == 5.0
    assert settings.llm_model == "phi3"
    
    # Cleanup
    Path("test_config.json").unlink()

def test_setting_update(self):
    """Test runtime setting updates"""
    settings = Settings(config_path="test_config.json")
    settings.update_setting("capture_interval", 10.0)
    
    assert settings.capture_interval == 10.0
    
    # Cleanup
    Path("test_config.json").unlink(missing_ok=True)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])