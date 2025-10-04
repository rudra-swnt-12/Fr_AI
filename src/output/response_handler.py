"""
src/output/response_handler.py
Handles output delivery via text and optional TTS
"""

import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ResponseHandler:
    """Handles delivery of assistant responses"""
    
    def __init__(self, enable_tts: bool = False, output_mode: str = "text"):
        """
        Initialize response handler
        
        Args:
            enable_tts: Whether to enable text-to-speech output
            output_mode: Output mode - 'text', 'tts', or 'both'
        """
        self.enable_tts = enable_tts
        self.output_mode = output_mode
        self.tts_engine = None
        
        if enable_tts:
            self._initialize_tts()
    
    def _initialize_tts(self):
        """Initialize text-to-speech engine"""
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            self.tts_engine.setProperty('rate', 150)  # Speed
            self.tts_engine.setProperty('volume', 0.8)  # Volume
            
            logger.info("TTS engine initialized")
            
        except ImportError:
            logger.warning("pyttsx3 not installed. TTS disabled.")
            self.enable_tts = False
        except Exception as e:
            logger.error(f"Failed to initialize TTS: {e}")
            self.enable_tts = False
    
    def handle_response(self, intent_result: Dict):
        """
        Process and deliver response based on intent
        
        Args:
            intent_result: Intent inference result from IntentEngine
        """
        if not intent_result or not intent_result.get('should_assist'):
            return
        
        suggestion = intent_result.get('suggestion')
        intent = intent_result.get('intent')
        confidence = intent_result.get('confidence', 0.0)
        
        if not suggestion:
            return
        
        # Format response message
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = self._format_message(suggestion, intent, confidence, timestamp)
        
        # Deliver response
        if self.output_mode in ['text', 'both']:
            self._output_text(message)
        
        if self.output_mode in ['tts', 'both'] and self.enable_tts:
            self._output_speech(suggestion)
        
        # Log response
        logger.info(f"Response delivered: {suggestion}")
    
    def _format_message(self, suggestion: str, intent: str, 
                       confidence: float, timestamp: str) -> str:
        """Format response message for display"""
        confidence_pct = int(confidence * 100)
        
        message = f"\n{'='*60}\n"
        message += f"🤖 Assistant Suggestion [{timestamp}]\n"
        message += f"{'='*60}\n"
        message += f"Intent: {intent}\n"
        message += f"Confidence: {confidence_pct}%\n\n"
        message += f"💡 {suggestion}\n"
        message += f"{'='*60}\n"
        
        return message
    
    def _output_text(self, message: str):
        """Output message as text to console"""
        print(message)
    
    def _output_speech(self, text: str):
        """Output message as speech via TTS"""
        if self.tts_engine is None:
            return
        
        try:
            # Clean text for better speech output
            clean_text = text.replace('\n', ' ').strip()
            
            self.tts_engine.say(clean_text)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            logger.error(f"TTS output failed: {e}")
    
    def emergency_alert(self, message: str):
        """
        Deliver high-priority emergency alert
        
        Args:
            message: Emergency message to deliver
        """
        alert = f"\n🚨 ALERT: {message}\n"
        print(alert)
        
        if self.enable_tts:
            self._output_speech(f"Alert! {message}")