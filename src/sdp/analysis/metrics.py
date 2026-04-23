"""
Metrics computation for defect prediction evaluation.
"""
import numpy as np
import pandas as pd
from typing import Dict, Optional
from sklearn.metrics import precision_score, recall_score, f1_score


def normalize_subset(subset: str) -> Optional[str]:
    """
    Normalize subset names to standard format.
    
    Args:
        subset: Subset identifier (e.g., 'Defective_01', 'Benign_00')
    
    Returns:
        Normalized subset code ('D01', 'D11', 'B00', 'B10') or None
    """
    if pd.isna(subset):
        return None
    subset_str = str(subset)
    
    if "Defective_01" in subset_str or "D01" in subset_str:
        return "D01"
    if "Defective_11" in subset_str or "D11" in subset_str:
        return "D11"
    if "Benign_00" in subset_str or "B00" in subset_str:
        return "B00"
    if "Benign_10" in subset_str or "B10" in subset_str:
        return "B10"
    return None


def subset_accuracy(df: pd.DataFrame, subset_name: str) -> float:
    """
    Compute accuracy on a specific subset.
    
    Args:
        df: Results DataFrame with 'subset_norm', 'verdict_int', 'new_label' columns
        subset_name: Subset identifier ('B00', 'B10', 'D01', 'D11')
    
    Returns:
        Accuracy (or NaN if subset is empty)
    """
    sub = df[df["subset_norm"] == subset_name]
    if len(sub) == 0:
        return np.nan
    return (sub["verdict_int"] == sub["new_label"]).mean()


def harmonic_mean(a: float, b: float) -> float:
    """
    Compute harmonic mean of two values.
    
    Args:
        a: First value
        b: Second value
    
    Returns:
        Harmonic mean or NaN if either is NaN or sum is 0
    """
    if pd.isna(a) or pd.isna(b) or (a + b) == 0:
        return np.nan
    return 2 * a * b / (a + b)


def compute_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Compute comprehensive evaluation metrics for defect prediction.
    
    Subsets:
    - B00: Bug_old == 0 and Bug_new == 0 (unchanged benign)
    - B10: Bug_old == 1 and Bug_new == 0 (fixed defect)
    - D01: Bug_old == 0 and Bug_new == 1 (introduced defect)
    - D11: Bug_old == 1 and Bug_new == 1 (unchanged defective)
    
    Args:
        df: Results DataFrame with required columns
    
    Returns:
        Dictionary with metrics:
        - B00, B10, D01, D11: subset accuracies
        - HMB: harmonic mean of B00 and D01 (benign changes)
        - HMD: harmonic mean of B10 and D11 (defective changes)
        - F1_changed: macro F1 on changed files
        - F1_unchanged: macro F1 on unchanged files
        - F1_total: macro F1 overall
    """
    # Normalize subsets
    if "subset_norm" not in df.columns:
        df["subset_norm"] = df["subset"].apply(normalize_subset)
    
    metrics = {}

    # Subset accuracies
    A_B00 = subset_accuracy(df, "B00")
    A_B10 = subset_accuracy(df, "B10")
    A_D01 = subset_accuracy(df, "D01")
    A_D11 = subset_accuracy(df, "D11")
    
    metrics["B00"] = A_B00
    metrics["B10"] = A_B10
    metrics["D01"] = A_D01
    metrics["D11"] = A_D11
    
    # Harmonic means for benign and defective changes
    metrics["HMB"] = harmonic_mean(A_B00, A_D01)  # Benign-change harmonic mean
    metrics["HMD"] = harmonic_mean(A_B10, A_D11)  # Defective-change harmonic mean

    # F1 scores by change status
    gt = df["new_label"].astype(int)
    pred = df["verdict_int"].astype(int)

    changed = df["old_label"] != df["new_label"]
    unchanged = ~changed

    if changed.any():
        metrics["F1_changed"] = f1_score(gt[changed], pred[changed], average='macro', zero_division=0)
    else:
        metrics["F1_changed"] = np.nan

    if unchanged.any():
        metrics["F1_unchanged"] = f1_score(gt[unchanged], pred[unchanged], average='macro', zero_division=0)
    else:
        metrics["F1_unchanged"] = np.nan

    metrics["F1_total"] = f1_score(gt, pred, average='macro', zero_division=0)

    # Additional metrics
    metrics["macro_precision"] = precision_score(gt, pred, average='macro', zero_division=0)
    metrics["macro_recall"] = recall_score(gt, pred, average='macro', zero_division=0)
    metrics["accuracy"] = (pred == gt).mean()

    return metrics


def compute_metrics_by_group(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """
    Compute metrics grouped by a column (e.g., 'skeptic_model', 'subset').
    
    Args:
        df: Results DataFrame
        group_col: Column name to group by
    
    Returns:
        DataFrame with metrics per group
    """
    metrics_rows = []
    
    for group_val, group_df in df.groupby(group_col):
        metrics = compute_metrics(group_df)
        metrics[group_col] = group_val
        metrics_rows.append(metrics)
    
    return pd.DataFrame(metrics_rows)
