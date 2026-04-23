from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

import numpy as np


@dataclass
class Hunk:
    file_path: str
    src1: str
    src2: str
    unified_diff: str
    changes_dict: Dict[str, List] = field(default_factory=dict)
    relevant_context: str = ""
    label: Optional[int] = None
    old_label: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[np.ndarray] = None
