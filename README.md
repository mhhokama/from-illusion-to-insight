# Change-aware SDP

This repository contains prototype notebooks and a new modular Python package for defect prediction experiments.

## Project structure

- `src/sdp/` - reusable package code
- `src/sdp/data/` - dataset download, loading, and partition utilities
- `src/sdp/analysis/` - diff extraction and Java context utilities
- `src/sdp/llm/` - OpenAI / LLM wrapper and prompt execution
- `src/sdp/experiments/` - CodeBERT/OpenAI embedding and evaluation pipelines
- `scripts/` - runnable helper scripts
- `data/` - downloaded datasets and generated artifacts
- `.env` - configuration values for dataset and API keys

## Getting started

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Configure `.env` with your keys and preferred dataset.

3. Run an experiment (example):

```bash
python -m sdp.cli --task codebert
```

## Notes

- Datasets are downloaded into `data/`.
- Notebook files remain as reference; the new package is the starting point for future cleanup.
