import os
import json
import re
import difflib
import logging
from typing import List, Dict, Tuple, Any, Optional
from dataclasses import dataclass, field

import pandas as pd
import numpy as np
from tqdm import tqdm
from openai import OpenAI

try:
    import Levenshtein
except Exception:
    Levenshtein = None

from .data.loader import load_datasets
from .config import DATASET_NAME_RUN, LLM7_KEYS, BASE_URL, llm7_all_models


class OpenAIWrapper:
    def __init__(self, api_keys=None, base_url=None):
        self.api_keys = api_keys or LLM7_KEYS
        self.base_url = base_url or BASE_URL
        self.client = OpenAI(api_key=self.api_keys[0], base_url=self.base_url)

    def list_models(self):
        return self.client.models.list()

    def create_completion(self, **kwargs):
        return self.client.responses.create(**kwargs)


class DefectPredictor:
    def __init__(self, dataset_name: str = DATASET_NAME_RUN):
        self.dataset_name = dataset_name
        self.dataset_map = load_datasets()
        self.past_ver, self.new_ver = self.dataset_map[self.dataset_name]

    def run(self):
        # Example entrypoint
        print(f"Running defect prediction for {self.dataset_name}")
        # TODO: wire up feature extraction, experts, meta-model, output


if __name__ == "__main__":
    predictor = DefectPredictor()
    predictor.run()
