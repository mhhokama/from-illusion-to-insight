"""
Prompt loader for managing and substituting expert system prompts.
"""
from typing import Dict, Any
from .analyzer import get_analyzer_prompt
from .proposer import get_proposer_prompt
from .skeptic import get_skeptic_prompt
from .judge import get_judge_prompt


class PromptLoader:
    """Manages loading and templating expert system prompts."""
    
    def __init__(self):
        self.prompts = {
            "analyzer": get_analyzer_prompt,
            "proposer": get_proposer_prompt,
            "skeptic": get_skeptic_prompt,
            "judge": get_judge_prompt,
        }
    
    def get_analyzer(self, diff_text: str, src1_context: str, src2_context: str, previous_status: str) -> Dict[str, str]:
        """Get the Analyzer prompt."""
        return self.prompts["analyzer"](diff_text, src1_context, src2_context, previous_status)
    
    def get_proposer(self, diff_text: str, context: str, analyzer_response: str, previous_status: str) -> Dict[str, str]:
        """Get the Proposer prompt."""
        return self.prompts["proposer"](diff_text, context, analyzer_response, previous_status)
    
    def get_skeptic(self, diff_text: str, context: str, proposer_response: str) -> Dict[str, str]:
        """Get the Skeptic prompt."""
        return self.prompts["skeptic"](diff_text, context, proposer_response)
    
    def get_judge(self, diff_text: str, context: str, proposer_response: str, skeptic_response: str, previous_status: str) -> Dict[str, str]:
        """Get the Judge prompt."""
        return self.prompts["judge"](diff_text, context, proposer_response, skeptic_response, previous_status)


def load_all_prompts() -> PromptLoader:
    """Factory function to create and return a PromptLoader instance."""
    return PromptLoader()
