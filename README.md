<h1 align="center">Change-aware SDP</h1>

<p align="center">
  <strong>From Illusion to Insight: Change-Aware File-Level Software Defect<br>
  Prediction Using Agentic AI</strong>
</p>

<p align="center">
  <a href="https://arxiv.org/abs/2512.23875"><img src="https://img.shields.io/badge/arXiv-2512.23875-b31b1b.svg" alt="arXiv: 2512.23875"></a>
  <a href="https://github.com/mhhokama/from-illusion-to-insight"><img src="https://img.shields.io/badge/GitHub-Repository-181717?logo=github&amp;logoColor=white" alt="GitHub repository"></a>
  <a href="#result-artifacts"><img src="https://img.shields.io/badge/Results-Kaggle-20BEFF?logo=kaggle&amp;logoColor=white" alt="Results on Kaggle"></a>
  <a href="#quick-start"><img src="https://img.shields.io/badge/Artifact-Reproducibility-2ea44f" alt="Reproducibility package"></a>
</p>

<p align="center">
  <a href="https://arxiv.org/abs/2512.23875">Paper</a> ·
  <a href="#research-contributions">Contributions</a> ·
  <a href="#package-layout">Package</a> ·
  <a href="#quick-start">Quick start</a> ·
  <a href="#result-artifacts">Results</a> ·
  <a href="#citation">Citation</a>
</p>

Implementation and replication package for **“From Illusion to Insight:
Change-Aware File-Level Software Defect Prediction Using Agentic AI.”** The paper is
available as an [arXiv preprint](https://arxiv.org/abs/2512.23875).

> [!CAUTION]
> The original experimental pipeline was developed in notebooks. The current package
> structure was created with GitHub Copilot assistance. Treat this repository as
> research code, inspect the implementation, and reproduce the reported results before
> adapting it for operational or production use.

## Overview

Traditional file-level software defect prediction evaluates models on snapshots from
successive software releases. Because many files persist across releases and retain the
same defect label, this setup can reward file overlap and label persistence instead of
reasoning about the effect of a code change.

This project reformulates defect prediction as a **change-aware** task. Models examine
how a file changes between consecutive versions and predict its resulting defect state.
The evaluation separates four status-transition subsets, making performance on rare but
important defect introductions and fixes visible rather than allowing stable files to
dominate the aggregate score.

| | |
| --- | --- |
| **Task** | File-level software defect prediction across successive releases |
| **Problem addressed** | File overlap and defect-label persistence in conventional evaluation |
| **Evaluation** | Four file-status transition subsets across multiple PROMISE projects |
| **Methods** | 14 LLMs, 8 reasoning strategies, and a change-aware multi-agent debate framework |

## Research contributions

- **Diagnoses the illusion of accuracy.** Shows how conventional file-level evaluation
  can produce deceptively strong aggregate results through file overlap and persistent
  labels.
- **Introduces change-aware prediction.** Models edits and defect-status transitions
  across consecutive project versions instead of treating files as independent static
  snapshots.
- **Evaluates diverse reasoning approaches.** Compares 14 LLMs under 8 reasoning
  strategies using the change-aware formulation.
- **Develops multi-agent debate.** Agents reason over code changes and exchange
  judgments to improve sensitivity to newly introduced defects and balance performance
  across transition subsets.

## Package layout

| Path | Purpose |
| --- | --- |
| `src/sdp/` | Reusable package implementation |
| `src/sdp/data/` | Dataset download, loading, and partition utilities |
| `src/sdp/analysis/` | Diff computation, Java parsing, and context extraction |
| `src/sdp/llm/` | OpenAI and LLM wrappers plus debate orchestration |
| `src/sdp/prompts/` | Prompt templates and prompt loader |
| `src/sdp/experiments/` | Experiment orchestration and result aggregation |
| `data/` | Downloaded files and dataset artifacts |
| `notebooks/` | Original research workflows and experiments |

## Quick start

1. Clone the repository and enter its directory:

   ```bash
   git clone https://github.com/mhhokama/from-illusion-to-insight.git
   cd from-illusion-to-insight
   ```

2. Install the required dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Create or update `.env` with the required dataset paths and OpenAI credentials.

4. Run an example experiment:

   ```bash
   python -m sdp.cli --task codebert
   ```

> [!NOTE]
> LLM-based experiments may call external model APIs and incur usage costs. Check the
> selected task, prompts, model configuration, and dataset paths before starting a full
> run.

## Result artifacts

The reported experiment outputs are archived separately on Kaggle:

| Artifact | Link |
| --- | --- |
| Change-aware LLM baseline results | [Open on Kaggle](https://www.kaggle.com/datasets/behnamrr/change-aware-llm-baseliens-results) |
| Multi-agent debate results | [Open on Kaggle](https://www.kaggle.com/datasets/behnamrr/multi-agent-debate-results) |

## Reproducibility notes

- The `notebooks/` directory preserves the original research workflows.
- The package under `src/sdp/` is the reusable implementation derived from those
  workflows.
- Validate prompt templates, model identifiers, API settings, and intermediate outputs
  before interpreting or extending an experiment.
- Report results by transition subset as well as in aggregate. Aggregate metrics alone
  can conceal poor performance on defect introductions and other rare transitions.

## Citation

If you use the code, results, or change-aware evaluation setup, please cite the paper:

```bibtex
@misc{hesamolhokama2025illusioninsightchangeawarefilelevel,
  title         = {From Illusion to Insight: Change-Aware File-Level Software Defect
                   Prediction Using Agentic AI},
  author        = {Mohsen Hesamolhokama and Behnam Rohani and Amirahmad Shafiee and
                   MohammadAmin Fazli and Jafar Habibi},
  year          = {2025},
  eprint        = {2512.23875},
  archivePrefix = {arXiv},
  primaryClass  = {cs.SE},
  url           = {https://arxiv.org/abs/2512.23875}
}
```

## Repository

Source code and updates are available at
[mhhokama/from-illusion-to-insight](https://github.com/mhhokama/from-illusion-to-insight).
