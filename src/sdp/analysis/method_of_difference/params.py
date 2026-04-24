from typing import Dict

METHOD_INSTRUCTIONS: Dict[int, str] = {
    0: "You are given SRC2 only. Decide whether the code is Defective or Benign.",
    1: "You are given SRC1 (known to be {bug_text}) and SRC2. Compare the two versions and decide if SRC2 is Defective or Benign.",
    2: "You are given SRC1 (known to be {bug_text}), SRC2, and the explicit line-level differences. Decide if SRC2 is Defective or Benign.",
    3: "You are given SRC1 (known to be {bug_text}), SRC2, their line-level differences, and a unified diff. Determine whether SRC2 is Defective or Benign.",
    4: "You are given SRC1 (known to be {bug_text}), differences, and a unified diff. Predict whether the unseen SRC2 is Defective or Benign.",
    5: "You are only given the differences and unified diff, and you know SRC1 was {bug_text}. Decide whether SRC2 is Defective or Benign.",
    6: "You are only given the local code context around changes, and you know SRC1 was {bug_text}. Predict whether the updated SRC2 is Defective or Benign.",
    7: "You are only given the differences, a unified diff, and examples of defect patterns, and you know SRC1 was {bug_text}. Decide whether SRC2 is Defective or Benign.",
}

DEFAULT_METHOD = 3
METHODS_WITH_DIFFS = {2, 3, 4, 5, 7}
METHODS_WITH_UNIFIED_DIFF = {3, 4, 5, 7}
