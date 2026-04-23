"""
Experiments module for orchestrating defect prediction experiments.
"""
from .orchestrator import (
    run_all_model_combinations,
    run_debate_complexity_experiment,
    run_context_complexity_experiment,
)
from .evaluator import test_skeptic_variants_async, async_run_model_single
from .visualization import (
    plot_time_vs_debate_rounds,
    plot_time_vs_max_lines,
    plot_accuracy_by_subset,
    plot_kde_time_distributions,
    plot_model_comparison,
)

__all__ = [
    "run_all_model_combinations",
    "run_debate_complexity_experiment",
    "run_context_complexity_experiment",
    "test_skeptic_variants_async",
    "async_run_model_single",
    "plot_time_vs_debate_rounds",
    "plot_time_vs_max_lines",
    "plot_accuracy_by_subset",
    "plot_kde_time_distributions",
    "plot_model_comparison",
]
