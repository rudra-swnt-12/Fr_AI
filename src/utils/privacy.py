"""
src/utils/privacy.py
Privacy controls and data management
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class PrivacyManager:
    """Manages privacy settings and controls"""
    
    def __init__(self):
        """Initialize privacy manager"""
        self.privacy_file = Path("data/.privacy_mode")
        
        # Clean up if it's a directory instead of file
        if self.privacy_file.is_dir():
            logger.warning("Privacy flag is a directory, removing...")
            import shutil
            shutil.rmtree(self.privacy_file)
        
        self.enabled = not self.privacy_file.exists()
    
    def toggle(self):
        """Toggle privacy mode on/off"""
        if self.enabled:
            self.disable()
        else:
            self.enable()
    
    def enable(self):
        """Enable monitoring (privacy mode OFF)"""
        if self.privacy_file.exists():
            if self.privacy_file.is_file():
                self.privacy_file.unlink()
            elif self.privacy_file.is_dir():
                import shutil
                shutil.rmtree(self.privacy_file)
        self.enabled = True
        logger.info("Privacy mode OFF - Monitoring enabled")
        print("\n✅ Privacy mode OFF - Assistant monitoring enabled")
    
    def disable(self):
        """Disable monitoring (privacy mode ON)"""
        # Ensure parent directory exists
        self.privacy_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create as file, not directory
        self.privacy_file.touch()
        self.enabled = False
        logger.info("Privacy mode ON - Monitoring disabled")
        print("\n🔒 Privacy mode ON - All monitoring stopped")
    
    def is_enabled(self) -> bool:
        """Check if monitoring is enabled"""
        # Refresh status from file
        if self.privacy_file.is_dir():
            import shutil
            shutil.rmtree(self.privacy_file)
        self.enabled = not self.privacy_file.exists()
        return self.enabled