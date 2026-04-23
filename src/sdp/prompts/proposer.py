"""
Proposer expert system prompt for initial defect verdict.
"""


def get_proposer_prompt(diff_text: str, context: str, analyzer_response: str, previous_status: str) -> dict:
    """
    Returns the Proposer system prompt and user message.
    
    Args:
        diff_text: The unified diff between file versions
        context: Relevant code context from the new version
        analyzer_response: The Analyzer's detailed response
        previous_status: The previous label (BENIGN or DEFECTIVE)
    
    Returns:
        Dictionary with 'system' and 'user' prompt keys
    """
    system_prompt = (
        "You are the PROPOSER. You receive: the unified diff, relevant new-version context, and the ANALYZER's "
        "response. Your primary responsibilities are:\n\n"
        "  1) Use the ANALYZER's evidence (both benign and defective points) together with the diff and code context "
        "     to decide whether the updated code (SRC2) should **remain the same status as SRC1** (i.e., still "
        f"{previous_status}) or should change status. Explicitly state the previous status (SRC1) and whether "
        "     you think SRC2 preserves it.\n"
        "  2) Present a concise, evidence-based proposition: label (BENIGN or DEFECTIVE) and the top supporting points.\n"
        "  3) Anticipate likely Skeptic objections and defend your position preemptively: address the strongest counter-arguments "
        "     that could be raised and explain why they do not overturn your proposition (or where they would).\n\n"
        "During debate rounds you will see the Analyzer (only in first round) and subsequent messages: keep your reasoning "
        "grounded in visible evidence, be explicit about remaining uncertainties, and be prepared to revise your view if the "
        "Skeptic surfaces convincing counter-evidence. Provide a clear final label and the top 3 supporting evidence items."
    )
    
    user_message = (
        f"Previous status (SRC1): {previous_status}\n\n"
        f"Unified diff:\n{diff_text}\n\n"
        f"Relevant code context:\n{context}\n\n"
        f"ANALYZER's response:\n{analyzer_response}\n\n"
        f"Please provide your initial proposition with label (BENIGN or DEFECTIVE) and supporting evidence."
    )
    
    return {
        "system": system_prompt,
        "user": user_message,
    }
