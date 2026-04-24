"""Backward compatibility shim for prompts.judge."""
from .roles.judge import get_judge_prompt

__all__ = ["get_judge_prompt"]
