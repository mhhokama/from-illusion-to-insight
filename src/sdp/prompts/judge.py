"""
Judge expert system prompt for final defect verdict.
"""


def get_judge_prompt(diff_text: str, context: str, proposer_response: str, skeptic_response: str, previous_status: str) -> dict:
    """
    Returns the Judge system prompt and user message.
    
    Args:
        diff_text: The unified diff between file versions
        context: Relevant code context
        proposer_response: The Proposer's response(s)
        skeptic_response: The Skeptic's response(s)
        previous_status: The previous label (BENIGN or DEFECTIVE)
    
    Returns:
        Dictionary with 'system' and 'user' prompt keys
    """
    system_prompt = (
        "You are the JUDGE. You receive: the unified diff, relevant code context, the SRC1 previous status, "
        "and the debate messages from both the PROPOSER and the SKEPTIC (but not the ANALYZER's private response). "
        "Your job is to weigh both sides and make a final, well-justified decision.\n\n"
        "Requirements:\n"
        "  - Evaluate the most load-bearing claims from PROPOSER and SKEPTIC and reference the diff and context when weighing them.\n"
        "  - Reason thoroughly and transparently: explain which arguments you found most persuasive and why, and which remaining unknowns "
        "    influenced your confidence.\n"
        "  - Be sensitive to the *previous label (SRC1)*:\n"
        f"      * If SRC1 was **BENIGN**, require **clear, specific, and reproducible evidence** before changing the status to DEFECTIVE. "
        "        In other words, assume continuity unless strong, well-supported reasoning shows a new defect was introduced.\n"
        f"      * If SRC1 was **DEFECTIVE**, be more open to considering that the issue might have been fixed—but still demand direct, "
        "        testable justification before declaring it BENIGN.\n"
        "  - This means when SRC1 was BENIGN, the threshold for flipping to DEFECTIVE is higher: the evidence must include at least one "
        "    concrete defect mechanism (not merely hypothetical risk) that clearly arises from the shown edit.\n\n"
        "At the end, produce a final decision that is programmatically parseable. **You MUST include these two lines exactly at the end "
        "of your message (no extra text after them):**\n\n"
        "### Final Prediction: <BENIGN or DEFECTIVE>\n"
        "### Confidence: <confidence_percentage>\n\n"
        "  - The confidence must be a percentage (0-100).\n"
        "  - If your decision is INCONCLUSIVE, choose the label you believe is safest given the available evidence and explain why in the body, "
        "    but still output one of the two labels in the final header lines.\n\n"
        "Style: be decisive but evidence-based. Cite the most relevant edits/lines and the strongest arguments from both sides, explain how the "
        "previous label influenced your confidence threshold, and make clear what follow-ups would most change your judgment."
    )
    
    user_message = (
        f"Previous status (SRC1): {previous_status}\n\n"
        f"Unified diff:\n{diff_text}\n\n"
        f"Relevant code context:\n{context}\n\n"
        f"PROPOSER's response:\n{proposer_response}\n\n"
        f"SKEPTIC's response:\n{skeptic_response}\n\n"
        f"Please provide your final decision with detailed reasoning."
    )
    
    return {
        "system": system_prompt,
        "user": user_message,
    }
