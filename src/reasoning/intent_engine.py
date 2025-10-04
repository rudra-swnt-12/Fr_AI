"""
src/reasoning/intent_engine.py
Infers user intent using LLM (via Ollama)
"""

import logging
import json
from typing import Dict, List, Optional
import requests

logger = logging.getLogger(__name__)


class IntentEngine:
    """Infers user intent from scene context using LLM"""
    
    def __init__(self, llm_model: str = "phi3:latest", 
                 context_window: int = 5,
                 ollama_url: str = "http://localhost:11434"):
        """
        Initialize intent engine
        
        Args:
            llm_model: Name of Ollama model to use
            context_window: Number of recent scenes to consider
            ollama_url: URL of Ollama API endpoint
        """
        self.llm_model = llm_model
        self.context_window = context_window
        self.ollama_url = ollama_url
        
        self._verify_ollama_connection()
    
    def _verify_ollama_connection(self):
        """Verify Ollama is running and model is available"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                
                if any(self.llm_model in name for name in model_names):
                    logger.info(f"Connected to Ollama with model: {self.llm_model}")
                else:
                    logger.warning(f"Model {self.llm_model} not found. Available: {model_names}")
            else:
                logger.warning("Ollama API returned unexpected status")
                
        except requests.exceptions.RequestException:
            logger.warning("Cannot connect to Ollama. Make sure it's running: ollama serve")
    
    def infer_intent(self, scene_data: Dict, 
                    context_history: List[Dict]) -> Optional[Dict]:
        """
        Infer user intent from current scene and context
        
        Args:
            scene_data: Current scene analysis
            context_history: List of recent scene analyses
            
        Returns:
            Dictionary with intent information and suggested action
        """
        try:
            # Build context from recent history
            context_summary = self._build_context(context_history[-self.context_window:])
            
            # Create prompt for LLM
            prompt = self._create_intent_prompt(scene_data, context_summary)
            
            # Query LLM via Ollama
            response = self._query_ollama(prompt)
            
            if response:
                intent = self._parse_intent_response(response)
                return intent
            
            return None
            
        except Exception as e:
            logger.error(f"Error inferring intent: {e}")
            return None
    
    def _build_context(self, history: List[Dict]) -> str:
        """Build context summary from history"""
        if not history:
            return "No prior context available."
        
        context_items = []
        for i, scene in enumerate(history[-3:]):  # Last 3 scenes
            desc = scene.get('description', 'Unknown scene')
            context_items.append(f"- {desc}")
        
        return "Recent observations:\n" + "\n".join(context_items)
    
    def _create_intent_prompt(self, scene_data: Dict, context: str) -> str:
        """Create prompt for intent inference"""
        description = scene_data.get('description', 'Unknown scene')
        objects = scene_data.get('objects', [])
        activity = scene_data.get('activity')
        
        prompt = f"""You are an AI assistant observing a user through their webcam to provide proactive help.

Current observation: {description}
{context}

Your task: Determine if the user needs assistance and what kind of help would be useful.

Rules:
1. Only suggest help if there's a clear, actionable need
2. Don't over-intervene - respect the user's autonomy
3. Be concise and practical
4. Focus on immediate, helpful actions

Respond ONLY with a JSON object in this exact format:
{{
    "should_assist": true/false,
    "confidence": 0.0-1.0,
    "intent": "brief description of inferred intent",
    "suggestion": "specific, actionable suggestion if should_assist is true",
    "reasoning": "brief explanation of why you reached this conclusion"
}}

Response:"""
        
        return prompt
    
    def _query_ollama(self, prompt: str) -> Optional[str]:
        """Query Ollama API with prompt"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.llm_model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3,  # Lower temperature for more consistent output
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            logger.warning("Ollama request timed out")
            return None
        except Exception as e:
            logger.error(f"Error querying Ollama: {e}")
            return None
    
    def _parse_intent_response(self, response: str) -> Dict:
        """Parse LLM response into structured intent"""
        try:
            # Try to extract JSON from response
            # LLM might add extra text, so find JSON block
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start >= 0 and end > start:
                json_str = response[start:end]
                intent_data = json.loads(json_str)
                
                # Validate required fields
                required = ['should_assist', 'confidence', 'intent']
                if all(field in intent_data for field in required):
                    return intent_data
            
            logger.warning("Could not parse valid intent from LLM response")
            return self._default_intent()
            
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON from LLM response")
            return self._default_intent()
    
    def _default_intent(self) -> Dict:
        """Return default intent when parsing fails"""
        return {
            'should_assist': False,
            'confidence': 0.0,
            'intent': 'Unable to determine intent',
            'suggestion': None,
            'reasoning': 'Failed to process scene'
        }