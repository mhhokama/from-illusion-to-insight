"""
Verdict parsing utilities for extracting judge predictions and confidence.
"""
import re
from typing import Tuple, Optional


def parse_judge_verdict(text: str) -> Tuple[Optional[str], Optional[int]]:
    """
    Parse the Judge's decision text -> ('BENIGN' or 'DEFECTIVE', 0 or 1).

    Handles variations like:
      - ### Final Prediction: BENIGN
      - Final Prediction: **Defective**
      - final-prediction: benign
      - final prediction - defective
    
    Args:
        text: Judge's response text
    
    Returns:
        Tuple of (verdict_str, verdict_int) where:
        - verdict_str: 'BENIGN' or 'DEFECTIVE'
        - verdict_int: 0 for BENIGN, 1 for DEFECTIVE
        - Returns (None, None) if unparseable
    """
    if not text:
        return None, None

    # Normalize text
    text_normalized = text.lower()

    # Regex: match 'final prediction' optionally followed by :, -, whitespace, then optional **, then label
    pattern = r"final\s*prediction\s*[:\-]?\s*\**\s*(benign|defective)\s*\**"
    match = re.search(pattern, text_normalized, flags=re.IGNORECASE)

    if match:
        verdict_str = match.group(1).upper()
        verdict_int = 0 if verdict_str == "BENIGN" else 1
        return verdict_str, verdict_int

    return None, None


def parse_confidence(text: str) -> Optional[int]:
    """
    Extract confidence percentage from Judge response.
    
    Handles variations like:
      - ### Confidence: 85
      - confidence: 0.85 (converts to 85)
      - Confidence (85%)
    
    Args:
        text: Judge's response text
    
    Returns:
        Confidence percentage (0-100) or None if not found
    """
    if not text:
        return None

    # Try to find "Confidence: XX" or similar
    pattern = r"confidence\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*%?"
    match = re.search(pattern, text, flags=re.IGNORECASE)

    if match:
        conf_str = match.group(1)
        conf_val = float(conf_str)
        # If it's a decimal between 0 and 1, assume it's a proportion
        if conf_val <= 1.0:
            conf_val = conf_val * 100
        return int(conf_val)

    return None
