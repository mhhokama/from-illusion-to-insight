"""
LLM and API wrapper for OpenAI-compatible endpoints.
"""
from typing import List, Dict, Any, Optional
import logging
from openai import OpenAI

from ..config import LLM7_KEYS, BASE_URL

logger = logging.getLogger(__name__)


class OpenAIWrapper:
    """Wrapper around OpenAI client for defect prediction system."""
    
    def __init__(self, api_keys: Optional[List[str]] = None, base_url: Optional[str] = None):
        """
        Initialize the OpenAI wrapper.
        
        Args:
            api_keys: List of API keys (defaults to LLM7_KEYS from config)
            base_url: Base URL for the API endpoint (defaults to BASE_URL from config)
        """
        self.api_keys = api_keys or LLM7_KEYS
        self.base_url = base_url or BASE_URL
        self.client = OpenAI(api_key=self.api_keys[0], base_url=self.base_url)
        self.current_key_idx = 0
        logger.info(f"OpenAIWrapper initialized with base_url={self.base_url}")
    
    def list_models(self) -> List[str]:
        """List available models from the API."""
        try:
            models = self.client.models.list()
            return [m.id for m in models.data] if hasattr(models, 'data') else []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def create_completion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> str:
        """
        Create a completion using the OpenAI API.
        
        Args:
            model: Model name to use
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional arguments to pass to the API
        
        Returns:
            The assistant's response text
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error creating completion with model {model}: {e}")
            raise
    
    def switch_key(self):
        """Switch to the next API key in the list (for rate limiting)."""
        self.current_key_idx = (self.current_key_idx + 1) % len(self.api_keys)
        self.client = OpenAI(api_key=self.api_keys[self.current_key_idx], base_url=self.base_url)
        logger.info(f"Switched to API key index {self.current_key_idx}")
