"""
Method-of-difference analysis helpers for prompt generation and dataset partitioning.
"""

from .examples import defect_examples, TIPS
from .generator import extract_local_context, generate_prompt, generate_prompt_v2
from .params import METHOD_INSTRUCTIONS, METHODS_WITH_DIFFS, METHODS_WITH_UNIFIED_DIFF
from .partition import partition_dataset_versions

__all__ = [
    "defect_examples",
    "TIPS",
    "METHOD_INSTRUCTIONS",
    "METHODS_WITH_DIFFS",
    "METHODS_WITH_UNIFIED_DIFF",
    "extract_local_context",
    "generate_prompt",
    "generate_prompt_v2",
    "partition_dataset_versions",
]
