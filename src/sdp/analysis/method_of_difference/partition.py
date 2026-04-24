from typing import Dict


def partition_dataset_versions(
    past_df,
    new_df,
    file_col: str = "File",
    src_col: str = "SRC",
    bug_col: str = "Bug",
) -> Dict[str, object]:
    """Partition two dataset versions into shared and changed subsets."""
    if file_col not in past_df.columns or file_col not in new_df.columns:
        raise ValueError(f"Missing required file column: {file_col}")

    files_past = set(past_df[file_col])
    case1 = new_df[~new_df[file_col].isin(files_past)].copy()
    case2 = new_df[new_df[file_col].isin(files_past)].copy()

    merged = case2.merge(
        past_df[[file_col, src_col, bug_col]],
        on=file_col,
        how="inner",
        suffixes=("_new", "_past"),
    )

    case2a = merged[merged[f"{src_col}_new"] == merged[f"{src_col}_past"]].copy()
    case2b = merged[merged[f"{src_col}_new"] != merged[f"{src_col}_past"]].copy()
    case2b1 = case2b[case2b[f"{bug_col}_new"] != case2b[f"{bug_col}_past"]].copy()
    case2b2 = case2b[case2b[f"{bug_col}_new"] == case2b[f"{bug_col}_past"]].copy()
    case2b1_false_to_true = case2b1[
        (case2b1[f"{bug_col}_past"] == 0) & (case2b1[f"{bug_col}_new"] == 1)
    ].copy()
    case2b1_true_to_false = case2b1[
        (case2b1[f"{bug_col}_past"] == 1) & (case2b1[f"{bug_col}_new"] == 0)
    ].copy()

    return {
        "case1": case1,
        "case2": case2,
        "case2a": case2a,
        "case2b": case2b,
        "case2b1": case2b1,
        "case2b2": case2b2,
        "case2b1_false_to_true": case2b1_false_to_true,
        "case2b1_true_to_false": case2b1_true_to_false,
        "merged": merged,
    }
