"""
src/config/settings.py
Configuration management for the assistant
"""

import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class Settings:
    """Manages application configuration"""
    
    # Default configuration
    DEFAULTS = {
        # Camera settings
        "camera_id": 0,
        "capture_fps": 30,
        "capture_interval": 3.0,  # seconds between captures
        
        # Vision settings
        "vision_model": "blip-base",  # or "blip-large"
        "show_preview": True,
        
        # LLM settings
        "llm_model": "llama3.1",  # Ollama model name
        "ollama_url": "http://localhost:11434",
        "context_window": 5,  # number of recent scenes to consider
        
        # Intervention settings
        "confidence_threshold": 0.6,  # minimum confidence to intervene
        "min_intervention_interval": 30.0,  # min seconds between interventions
        
        # Output settings
        "output_mode": "text",  # 'text', 'tts', or 'both'
        "enable_tts": False,
        
        # Privacy settings
        "privacy_mode": False,
        "save_frames": False,
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize settings
        
        Args:
            config_path: Path to custom configuration file (JSON)
        """
        self.config_path = config_path or "config.json"
        self.config = self.DEFAULTS.copy()
        
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file if exists"""
        config_file = Path(self.config_path)
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
                    logger.info(f"Loaded configuration from {self.config_path}")
            except Exception as e:
                logger.warning(f"Failed to load config file: {e}. Using defaults.")
        else:
            logger.info("No config file found. Using default settings.")
            self.save_config()  # Create default config file
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
                logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def __getattr__(self, name):
        """Allow dot notation access to config values"""
        if name in self.config:
            return self.config[name]
        raise AttributeError(f"Setting '{name}' not found")
    
    def update_setting(self, key: str, value):
        """Update a specific setting"""
        if key in self.config:
            self.config[key] = value
            self.save_config()
        else:
            logger.warning(f"Unknown setting: {key}")