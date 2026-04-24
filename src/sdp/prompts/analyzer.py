"""Backward compatibility shim for prompts.analyzer."""
from .roles.analyzer import get_analyzer_prompt

__all__ = ["get_analyzer_prompt"]
