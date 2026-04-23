"""
Visualization utilities for experiment results.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional
from scipy import stats


def plot_time_vs_debate_rounds(
    results_dict: Dict[int, List[float]],
    time_col: str = "total_runtime_sec",
    figsize: tuple = (12, 6),
) -> None:
    """
    Plot timing metrics vs number of debate rounds with confidence intervals.
    
    Args:
        results_dict: Dictionary mapping debate_round -> list of times
        time_col: Time column name (for labeling)
        figsize: Figure size
    """
    debates = sorted(results_dict.keys())
    means = []
    cis = []
    
    for n in debates:
        times = np.array(results_dict[n])
        mean = times.mean()
        std = times.std()
        ci = stats.t.interval(0.95, len(times) - 1, loc=mean, scale=std / np.sqrt(len(times)))
        ci_err = mean - ci[0]
        
        means.append(mean)
        cis.append(ci_err)
    
    plt.figure(figsize=figsize)
    plt.errorbar(debates, means, yerr=cis, marker='o', capsize=5, linewidth=2)
    plt.xlabel("Number of Debate Rounds", fontsize=14)
    plt.ylabel("Time (seconds)", fontsize=14)
    plt.title(f"Time Complexity: {time_col}", fontsize=16)
    plt.grid(True, alpha=0.3)
    plt.xticks(debates)
    plt.tight_layout()
    plt.show()


def plot_time_vs_max_lines(
    results_by_max_lines: Dict[int, List[float]],
    max_lines_values: Optional[List[int]] = None,
    figsize: tuple = (12, 6),
) -> None:
    """
    Plot timing metrics vs max_context_lines with confidence intervals.
    
    Args:
        results_by_max_lines: Dictionary mapping max_lines -> list of times
        max_lines_values: Ordered list of max_lines values
        figsize: Figure size
    """
    if max_lines_values is None:
        max_lines_values = sorted(results_by_max_lines.keys())
    
    means = []
    cis = []
    
    for ml in max_lines_values:
        if ml not in results_by_max_lines:
            continue
        
        times = np.array(results_by_max_lines[ml])
        if len(times) == 0:
            continue
        
        mean = times.mean()
        std = times.std()
        if len(times) > 1:
            ci = stats.t.interval(0.95, len(times) - 1, loc=mean, scale=std / np.sqrt(len(times)))
            ci_err = mean - ci[0]
        else:
            ci_err = 0
        
        means.append(mean)
        cis.append(ci_err)
    
    plt.figure(figsize=figsize)
    plt.plot(max_lines_values, means, marker='o', linewidth=2, markersize=8)
    plt.fill_between(max_lines_values, np.array(means) - np.array(cis), 
                     np.array(means) + np.array(cis), alpha=0.2)
    plt.xlabel("Max Context Lines", fontsize=14)
    plt.ylabel("Time (seconds)", fontsize=14)
    plt.title("Time Complexity vs Context Size", fontsize=16)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_accuracy_by_subset(
    df: pd.DataFrame,
    subset_col: str = "subset_norm",
    figsize: tuple = (10, 6),
) -> None:
    """
    Plot accuracy by subset with error bars.
    
    Args:
        df: Results DataFrame
        subset_col: Column name for subset labels
        figsize: Figure size
    """
    subsets = ["B00", "B10", "D01", "D11"]
    accuracies = []
    errors = []
    
    for subset in subsets:
        subset_df = df[df[subset_col] == subset]
        if len(subset_df) == 0:
            continue
        
        acc = (subset_df["verdict_int"] == subset_df["new_label"]).mean()
        n = len(subset_df)
        se = np.sqrt(acc * (1 - acc) / n) if n > 0 else 0
        
        accuracies.append(acc)
        errors.append(1.96 * se)  # 95% CI
    
    plt.figure(figsize=figsize)
    plt.bar(subsets, accuracies, yerr=errors, capsize=10, alpha=0.7)
    plt.ylabel("Accuracy", fontsize=14)
    plt.xlabel("Subset", fontsize=14)
    plt.title("Accuracy by Subset", fontsize=16)
    plt.ylim([0, 1])
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()


def plot_kde_time_distributions(
    df: pd.DataFrame,
    time_col: str = "total_runtime_sec",
    label_col: str = "new_label",
    figsize: tuple = (12, 6),
) -> None:
    """
    Plot KDE distributions of timing by label (benign vs defective).
    
    Args:
        df: Results DataFrame
        time_col: Time column name
        label_col: Label column name
        figsize: Figure size
    """
    plt.figure(figsize=figsize)
    
    benign_times = df[df[label_col] == 0][time_col].dropna()
    defective_times = df[df[label_col] == 1][time_col].dropna()
    
    if len(benign_times) > 0:
        benign_times.plot(kind='kde', label='Benign', linewidth=2)
    if len(defective_times) > 0:
        defective_times.plot(kind='kde', label='Defective', linewidth=2)
    
    plt.xlabel(f"{time_col} (seconds)", fontsize=14)
    plt.ylabel("Density", fontsize=14)
    plt.title(f"Time Distribution by Label", fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_model_comparison(
    results_df: pd.DataFrame,
    metric: str = "accuracy",
    figsize: tuple = (12, 6),
) -> None:
    """
    Plot comparison of models by a metric.
    
    Args:
        results_df: Results grouped by model
        metric: Metric column name
        figsize: Figure size
    """
    if "skeptic_model" in results_df.columns:
        groupby_col = "skeptic_model"
    elif "analyzer_model" in results_df.columns:
        groupby_col = "analyzer_model"
    else:
        return
    
    agg_df = results_df.groupby(groupby_col)[metric].agg(['mean', 'std', 'count'])
    agg_df['se'] = agg_df['std'] / np.sqrt(agg_df['count'])
    
    plt.figure(figsize=figsize)
    agg_df['mean'].plot(kind='bar', yerr=agg_df['se'], capsize=5, alpha=0.7)
    plt.ylabel(metric.title(), fontsize=14)
    plt.xlabel("Model", fontsize=14)
    plt.title(f"Model Comparison: {metric.title()}", fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()
