"""
Change-aware Software Defect Prediction (SDP) Package

A modular Python package for file-level defect prediction using expert debate systems,
CodeBERT embeddings, FAISS retrieval, and LLM-based analysis.

Submodules:
- config: Configuration loader for datasets and LLM settings
- data: Dataset loading, selection, and partitioning
- analysis: Diff computation, Java parsing, and context extraction
- llm: OpenAI wrapper and expert debate orchestration
- prompts: Expert system prompt templates and loaders
- cli: Command-line interface for running experiments
"""

__version__ = "0.1.0"
__author__ = "Change-aware SDP Team"

from .config import DATASET_NAME_RUN, LLM7_KEYS, BASE_URL
from .llm import OpenAIWrapper, ExpertDebateSystem, DebateRound
from .prompts import load_all_prompts

__all__ = [
    "DATASET_NAME_RUN",
    "LLM7_KEYS",
    "BASE_URL",
    "OpenAIWrapper",
    "ExpertDebateSystem",
    "DebateRound",
    "load_all_prompts",
]
