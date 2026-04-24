"""
Prompt role modules for expert debate system prompts.
"""

from .analyzer import get_analyzer_prompt
from .judge import get_judge_prompt
from .proposer import get_proposer_prompt
from .skeptic import get_skeptic_prompt

__all__ = [
    "get_analyzer_prompt",
    "get_judge_prompt",
    "get_proposer_prompt",
    "get_skeptic_prompt",
]
