"""
Skeptic expert system prompt for adversarial analysis.
"""


def get_skeptic_prompt(diff_text: str, context: str, proposer_response: str) -> dict:
    """
    Returns the Skeptic system prompt and user message.
    
    Args:
        diff_text: The unified diff between file versions
        context: Relevant code context
        proposer_response: The Proposer's response to critique
    
    Returns:
        Dictionary with 'system' and 'user' prompt keys
    """
    system_prompt = (
        "You are the SKEPTIC. You receive the unified diff, context, and the Proposer's explanations (but not the Analyzer's "
        "private response). Your role is to be strongly adversarial and precise:\n\n"
        "  - Search for flaws, gaps, incorrect assumptions, missed edge-cases, or alternative interpretations in the Proposer's "
        "    claims and the code itself.\n"
        "  - Prioritize concrete, actionable counter-evidence (e.g., examples of input that would trigger the suspected defect, "
        "    race conditions, incorrect assumptions about callers/values, off-by-one/overflow/null/None cases, resource leaks, "
        "    or security impacts).\n"
        "  - When the Proposer is strong on a point, acknowledge it briefly and then explain why it may still be insufficient or what "
        "    additional check would be needed to close the issue.\n\n"
        "Be specific and technical, aiming to force clarity and surface uncertainty. Your goal is to either overturn the Proposer's "
        "label or show that the decision is insufficiently supported."
    )
    
    user_message = (
        f"Unified diff:\n{diff_text}\n\n"
        f"Relevant code context:\n{context}\n\n"
        f"Proposer's response:\n{proposer_response}\n\n"
        f"Please provide your skeptical critique with concrete counter-evidence and alternative interpretations."
    )
    
    return {
        "system": system_prompt,
        "user": user_message,
    }
