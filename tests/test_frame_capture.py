"""
Unit tests for frame capture module
"""

import pytest
import numpy as np
from src.vision.frame_capture import FrameCapture

class TestFrameCapture:
    """Test cases for FrameCapture class"""
def test_initialization(self):
    """Test camera initialization"""
    try:
        fc = FrameCapture(camera_id=0)
        assert fc.cap is not None
        assert fc.cap.isOpened()
        fc.release()
    except RuntimeError:
        pytest.skip("No camera available for testing")

def test_get_frame(self):
    """Test frame capture"""
    try:
        fc = FrameCapture(camera_id=0)
        frame = fc.get_frame()
        
        assert frame is not None
        assert isinstance(frame, np.ndarray)
        assert len(frame.shape) == 3  # Height, Width, Channels
        assert frame.shape[2] == 3  # BGR format
        
        fc.release()
    except RuntimeError:
        pytest.skip("No camera available for testing")

def test_get_frame_rgb(self):
    """Test RGB frame conversion"""
    try:
        fc = FrameCapture(camera_id=0)
        frame = fc.get_frame_rgb()
        
        assert frame is not None
        assert isinstance(frame, np.ndarray)
        
        fc.release()
    except RuntimeError:
        pytest.skip("No camera available for testing")

def test_frame_count(self):
    """Test frame counting"""
    try:
        fc = FrameCapture(camera_id=0)
        initial_count = fc.frame_count
        
        fc.get_frame()
        fc.get_frame()
        
        assert fc.frame_count == initial_count + 2
        
        fc.release()
    except RuntimeError:
        pytest.skip("No camera available for testing")
