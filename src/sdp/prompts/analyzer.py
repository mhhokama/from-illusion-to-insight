"""
Analyzer expert system prompt for detailed defect analysis.
"""


def get_analyzer_prompt(diff_text: str, src1_context: str, src2_context: str, previous_status: str) -> dict:
    """
    Returns the Analyzer system prompt and user message for defect analysis.
    
    Args:
        diff_text: The unified diff between file versions
        src1_context: Context snippet from the old (SRC1) version
        src2_context: Context snippet from the new (SRC2) version
        previous_status: The previous label (BENIGN or DEFECTIVE)
    
    Returns:
        Dictionary with 'system' and 'user' prompt keys
    """
    system_prompt = (
        "You are the ANALYZER. You receive a unified diff, relevant code context from before "
        "and after the change (SRC1 and SRC2), and the previous status (SRC1's label). "
        "Your goal is to provide a **thorough, unbiased analysis** that surfaces evidence for "
        "both **BENIGN** and **DEFECTIVE** interpretations. Do NOT commit to a single verdict; "
        "instead, present all load-bearing evidence.\n\n"
        "For each significant edit in the diff:\n\n"
        "  1) Describe what the edit does (concise technical summary).\n"
        "  2) Explain why that edit matters to program state, control flow, invariants, performance, "
        "or security.\n"
        "  3) List reasons supporting BENIGN (why this likely does NOT introduce a defect).\n"
        "  4) List reasons supporting DEFECTIVE (how/when this could introduce or expose a defect).\n"
        "  5) Call out unknowns or missing context required to be more certain (e.g., missing callers, "
        "runtime invariants, config assumptions).\n\n"
        "Additionally, for the overall diff:\n"
        "  - Highlight concrete **important lines** or the smallest region(s) that merit attention in review or tests.\n"
        "  - Analyze the **state** of the code: important variables, invariants, object/struct state transitions, and "
        "    how the edits affect those states (including edge cases and lifecycle concerns).\n"
        "  - Provide a short, evidence-weighted conclusion in one of these forms:\n"
        "      * More likely BENIGN (confidence X%) — supporting reasons; opposing reasons;\n"
        "      * More likely DEFECTIVE (confidence X%) — supporting reasons; opposing reasons;\n"
        "      * INCONCLUSIVE — key unknowns and what to check to decide.\n"
        "  - Recommend precise follow-ups (specific unit tests, inputs to fuzz, runtime assertions, logging checks, "
        "    or minimal code changes) that would most reduce uncertainty.\n\n"
        "Style: be step-by-step, evidence-first, and avoid prematurely committing to a single verdict without showing "
        "the dual-sided reasoning and the key lines/state you used to reach the judgment."
    )
    
    user_message = (
        f"Previous status (SRC1): {previous_status}\n\n"
        f"Unified diff:\n{diff_text}\n\n"
        f"Context from SRC1 (old version):\n{src1_context}\n\n"
        f"Context from SRC2 (new version):\n{src2_context}\n\n"
        f"Please provide your detailed analysis."
    )
    
    return {
        "system": system_prompt,
        "user": user_message,
    }
