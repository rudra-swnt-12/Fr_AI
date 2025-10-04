"""
Proactive Multimodal AI Assistant
Main application entry point
"""

import cv2
import time
import threading
from pathlib import Path
from typing import Optional
import logging

from src.vision.frame_capture import FrameCapture
from src.vision.scene_analyzer import SceneAnalyzer
from src.reasoning.intent_engine import IntentEngine
from src.output.response_handler import ResponseHandler
from src.config.settings import Settings
from src.utils.privacy import PrivacyManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/assistant.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ProactiveAssistant:
    """Main application class for the proactive AI assistant"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the assistant with configuration"""
        self.settings = Settings(config_path)
        self.privacy_manager = PrivacyManager()
        
        # Initialize components
        self.frame_capture = FrameCapture(
            camera_id=self.settings.camera_id,
            fps=self.settings.capture_fps
        )
        
        self.scene_analyzer = SceneAnalyzer(
            model_name=self.settings.vision_model
        )
        
        self.intent_engine = IntentEngine(
            llm_model=self.settings.llm_model,
            context_window=self.settings.context_window
        )
        
        self.response_handler = ResponseHandler(
            enable_tts=self.settings.enable_tts,
            output_mode=self.settings.output_mode
        )
        
        # State management
        self.is_running = False
        self.is_paused = False
        self.last_intervention_time = 0
        self.context_history = []
        
        logger.info("Proactive Assistant initialized successfully")
    
    def start(self):
        """Start the assistant's main processing loop"""
        if not self.privacy_manager.is_enabled():
            logger.warning("Privacy mode is ON. Assistant will not start.")
            print("\n⚠️  Privacy mode is enabled. Disable it to start monitoring.")
            return
        
        self.is_running = True
        logger.info("Assistant started")
        print("\n✅ Proactive Assistant is now running...")
        print("Press 'q' to quit, 'p' to pause/resume, 'x' for privacy mode\n")
        
        try:
            self.main_loop()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
            self.stop()
        except Exception as e:
            logger.error(f"Error in main loop: {e}", exc_info=True)
            self.stop()
    
    def main_loop(self):
        """Main processing loop"""
        while self.is_running:
            # Check if paused
            if self.is_paused:
                time.sleep(0.1)
                continue
            
            # Capture frame
            frame = self.frame_capture.get_frame()
            if frame is None:
                logger.warning("Failed to capture frame")
                time.sleep(1)
                continue
            
            # Analyze scene
            scene_data = self.scene_analyzer.analyze(frame)
            
            if scene_data:
                # Add timestamp and update context
                scene_data['timestamp'] = time.time()
                self.update_context(scene_data)
                
                # Infer user intent
                intent_result = self.intent_engine.infer_intent(
                    scene_data,
                    self.context_history
                )
                
                # Check if intervention is needed
                if self.should_intervene(intent_result):
                    # Generate and deliver response
                    self.response_handler.handle_response(intent_result)
                    self.last_intervention_time = time.time()
                
                # Display preview (optional)
                if self.settings.show_preview:
                    self.display_preview(frame, scene_data, intent_result)
            
            # Control loop timing
            time.sleep(self.settings.capture_interval)
    
    def update_context(self, scene_data: dict):
        """Update context history with new scene data"""
        self.context_history.append(scene_data)
        
        # Keep only recent context (last N items)
        max_history = self.settings.context_window
        if len(self.context_history) > max_history:
            self.context_history = self.context_history[-max_history:]
    
    def should_intervene(self, intent_result: dict) -> bool:
        """Determine if the assistant should intervene"""
        if not intent_result or not intent_result.get('should_assist'):
            return False
        
        # Check minimum time between interventions
        time_since_last = time.time() - self.last_intervention_time
        if time_since_last < self.settings.min_intervention_interval:
            return False
        
        # Check confidence threshold
        confidence = intent_result.get('confidence', 0.0)
        if confidence < self.settings.confidence_threshold:
            return False
        
        return True
    
    def display_preview(self, frame, scene_data: dict, intent_result: dict):
        """Display preview window with annotations"""
        preview = frame.copy()
        
        # Add text overlay
        description = scene_data.get('description', 'Processing...')[:60]
        cv2.putText(preview, description, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        if intent_result and intent_result.get('should_assist'):
            cv2.putText(preview, "Intent detected!", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        cv2.imshow('Proactive Assistant', preview)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            self.stop()
        elif key == ord('p'):
            self.toggle_pause()
        elif key == ord('x'):
            self.toggle_privacy()
    
    def toggle_pause(self):
        """Toggle pause state"""
        self.is_paused = not self.is_paused
        state = "paused" if self.is_paused else "resumed"
        logger.info(f"Assistant {state}")
        print(f"\n⏸️  Assistant {state}")
    
    def toggle_privacy(self):
        """Toggle privacy mode"""
        self.privacy_manager.toggle()
        if not self.privacy_manager.is_enabled():
            self.stop()
    
    def stop(self):
        """Stop the assistant gracefully"""
        logger.info("Stopping assistant...")
        self.is_running = False
        self.frame_capture.release()
        cv2.destroyAllWindows()
        print("\n👋 Assistant stopped. Goodbye!")


def main():
    """Entry point"""
    print("=" * 60)
    print("Proactive Multimodal AI Assistant v0.1")
    print("=" * 60)
    
    # Create necessary directories
    Path("logs").mkdir(exist_ok=True)
    Path("data/models").mkdir(parents=True, exist_ok=True)
    Path("data/cache").mkdir(parents=True, exist_ok=True)
    
    # Initialize and start assistant
    assistant = ProactiveAssistant()
    assistant.start()


if __name__ == "__main__":
    main()