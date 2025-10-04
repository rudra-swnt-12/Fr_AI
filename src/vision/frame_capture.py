"""
Handles webcam frame capture using OpenCV
"""

import cv2
import numpy as np
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class FrameCapture:
    """Captures frames from webcam"""
    
    def __init__(self, camera_id: int = 0, fps: int = 30):
        """
        Initialize webcam capture
        
        Args:
            camera_id: Camera device ID (default 0 for primary webcam)
            fps: Frames per second for capture
        """
        self.camera_id = camera_id
        self.fps = fps
        self.cap = None
        self.frame_count = 0
        
        self._initialize_camera()
    
    def _initialize_camera(self):
        """Initialize the camera capture"""
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            
            if not self.cap.isOpened():
                raise RuntimeError(f"Cannot open camera {self.camera_id}")
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            # Warm up camera
            for _ in range(5):
                self.cap.read()
            
            logger.info(f"Camera {self.camera_id} initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            raise
    
    def get_frame(self) -> Optional[np.ndarray]:
        """
        Capture and return current frame
        
        Returns:
            Numpy array of frame in BGR format, or None if capture fails
        """
        if self.cap is None or not self.cap.isOpened():
            logger.error("Camera not initialized")
            return None
        
        ret, frame = self.cap.read()
        
        if not ret:
            logger.warning("Failed to read frame")
            return None
        
        self.frame_count += 1
        return frame
    
    def get_frame_rgb(self) -> Optional[np.ndarray]:
        """Get frame in RGB format (for model input)"""
        frame = self.get_frame()
        if frame is not None:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None
    
    def release(self):
        """Release camera resources"""
        if self.cap is not None:
            self.cap.release()
            logger.info("Camera released")
    
    def __del__(self):
        """Cleanup on deletion"""
        self.release()