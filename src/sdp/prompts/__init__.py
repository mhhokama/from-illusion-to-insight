"""
Expert system prompts for defect prediction debate.
"""
from .analyzer import get_analyzer_prompt
from .proposer import get_proposer_prompt
from .skeptic import get_skeptic_prompt
from .judge import get_judge_prompt
from .loader import load_all_prompts

__all__ = [
    "get_analyzer_prompt",
    "get_proposer_prompt",
    "get_skeptic_prompt",
    "get_judge_prompt",
    "load_all_prompts",
]
