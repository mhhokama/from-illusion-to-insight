# Change-aware SDP

This repository contains the implementation and code for the paper [From Illusion to Insight: Change-Aware File-Level Software Defect Prediction Using Agentic AI](https://arxiv.org/abs/2512.23875).

> **Warning:** The original pipeline was developed in notebooks, and the current package structure was built with GitHub Copilot assistance. Use the code carefully and validate results before applying it in production.

## What the paper says

- **Analyzes the illusion of accuracy in traditional SDP:** Shows that standard file-level evaluation setups can suffer from file overlap and label-persistence bias, creating deceptively high reported performance.
- **Introduces a change-aware formulation and evaluation:** Proposes a software evolution-aware setup that explicitly models edits and status transitions across four transition subsets.
- **Evaluates diverse change-aware reasoning methods:** Tests 14 LLMs across 8 different reasoning strategies to compare performance under this new formulation.
- **Presents a multi-agent debate framework:** Develops a change-aware debate approach where agents reason over code changes, improving sensitivity to introduced defects and balancing performance across transition subsets.

## What’s inside

- `src/sdp/` - reusable package implementation
- `src/sdp/data/` - dataset loading, download, and partition utilities
- `src/sdp/analysis/` - diff computation, Java parsing, and context extraction
- `src/sdp/llm/` - OpenAI/LLM wrapper and debate orchestration
- `src/sdp/prompts/` - prompt templates and prompt loader
- `src/sdp/experiments/` - experiment orchestration and result aggregation
- `data/` - dataset artifacts and downloaded files
- `notebooks/` - original notebook workflows and experiments

## Key links

- Paper: [From Illusion to Insight: Change-Aware File-Level Software Defect Prediction Using Agentic AI](https://arxiv.org/abs/2512.23875)

- Data:
  - [Results of Change-aware LLM Baselines](https://www.kaggle.com/datasets/behnamrr/change-aware-llm-baseliens-results)
  - [Results of Multi-Agent Debate](https://www.kaggle.com/datasets/behnamrr/multi-agent-debate-results)

## Quick start

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Create or update `.env` with dataset paths and OpenAI credentials.

3. Run an example experiment:

```bash
python -m sdp.cli --task codebert
```

## Notes

- The `notebooks/` folder contains the original research notebooks.
- Verify prompt behavior and results before using any experimental setup.
