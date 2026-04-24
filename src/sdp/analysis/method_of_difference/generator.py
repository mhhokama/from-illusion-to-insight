from typing import Dict, List, Tuple

from .examples import defect_examples, TIPS
from .params import METHOD_INSTRUCTIONS, METHODS_WITH_DIFFS, METHODS_WITH_UNIFIED_DIFF
from ..diff import format_diffs, unified_diff


def extract_local_context(src: str, line_nums: List[int], window: int = 7) -> str:
    lines = src.splitlines()
    out = []
    for ln in sorted(set(line_nums)):
        start = max(0, ln - 1 - window)
        end = min(len(lines), ln + window)
        snippet = "\n".join(f"{i+1}: {lines[i]}" for i in range(start, end))
        out.append(f"Context around line {ln}:\n{snippet}\n")
    return "\n".join(out)


def get_method_instruction(method: int, bug_text: str) -> str:
    instruction = METHOD_INSTRUCTIONS.get(method, METHOD_INSTRUCTIONS[3])
    return instruction.format(bug_text=bug_text)


def generate_prompt(
    src1: str,
    src2: str,
    bug_label: int,
    diffs: Dict[str, List[Tuple]],
    method: int = 3,
    context_window: int = 5,
) -> str:
    if bug_label not in (0, 1):
        raise ValueError("bug_label must be 0 (benign) or 1 (defective)")

    bug_text = "Defective" if bug_label == 1 else "Benign"
    header = get_method_instruction(method, bug_text) + "\n\n"
    body = ""
    diffs_text = ""
    unified_text = ""
    examples_text = ""

    if method == 0:
        body += "[SRC]\n" + src2 + "\n\n"
    elif method in (1, 2, 3):
        body += "[SRC1]\n" + src1 + "\n\n[SRC2]\n" + src2 + "\n\n"
    elif method == 4:
        body += "[SRC1]\n" + src1 + "\n\n"
    elif method == 5:
        pass
    elif method == 6:
        line_nums = [ln for ln, _ in diffs.get("removed", [])] + [ln for ln, _ in diffs.get("added", [])] + [old_ln for old_ln, _, _, _ in diffs.get("changed", [])] + [new_ln for _, _, new_ln, _ in diffs.get("changed", [])]
        body += extract_local_context(src1, line_nums, window=context_window) + "\n\n"
    elif method == 7:
        examples_text = defect_examples + "\n\n"

    if method in METHODS_WITH_DIFFS:
        diffs_text = "[Differences]\n" + format_diffs(diffs) + "\n\n"
    if method in METHODS_WITH_UNIFIED_DIFF:
        unified_text = "[Unified diff]\n" + unified_diff(src1, src2) + "\n\n"

    mapping = "[SRC1] -> [" + bug_text + "]\n\n" if method != 0 else ""
    mapping += "[SRC2] -> [???]\n\n" if method != 0 else "[SRC] -> [???]\n\n"

    conclusion = "Think step by step. What is the status of SRC2? (Defective or Benign)"
    prompt = header + examples_text + mapping + body + diffs_text + unified_text + conclusion
    return prompt


def generate_prompt_v2(
    src1: str,
    src2: str,
    bug_label: int,
    diffs: Dict[str, List[Tuple]],
    method: int = 3,
    context_window: int = 5,
    add_tips: bool = False,
) -> str:
    if bug_label not in (0, 1):
        raise ValueError("bug_label must be 0 (benign) or 1 (defective)")

    prompt = generate_prompt(src1, src2, bug_label, diffs, method, context_window)
    if add_tips:
        prompt += "\n\n" + TIPS
    return prompt
