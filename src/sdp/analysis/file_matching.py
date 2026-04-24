import re
import random
from typing import Optional

import pandas as pd

try:
    import javalang
except ImportError:  # pragma: no cover
    javalang = None

try:
    from rapidfuzz import fuzz
except ImportError:  # pragma: no cover
    fuzz = None


def sanitize_java_source(src: str) -> str:
    if not isinstance(src, str):
        return src
    lines = src.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("#", "import ", "package ", "class ", "interface ", "enum ")):
            cleaned.append(line)
        elif cleaned:
            cleaned.append(line)
    return "\n".join(cleaned)


def get_java_ast_sequence(source_code: str) -> Optional[str]:
    if javalang is None:
        raise ImportError(
            "javalang is required for AST-based matching. Install it with `pip install javalang`."
        )
    if not isinstance(source_code, str) or not source_code.strip():
        return None

    key = hash(source_code)
    source_code = sanitize_java_source(source_code)

    try:
        tree = javalang.parse.parse(source_code)
        nodes = [type(node).__name__ for _, node in tree]
        return " ".join(nodes)
    except Exception:
        return None


def exact_path_matches(df_old: pd.DataFrame, df_new: pd.DataFrame, file_col: str = "File") -> pd.DataFrame:
    common = set(df_old[file_col]) & set(df_new[file_col])
    return pd.DataFrame(
        {
            "df_new_file": list(common),
            "df_old_file": list(common),
            "similarity": [1.0] * len(common),
        }
    )


def remove_exact_matches(df_old: pd.DataFrame, df_new: pd.DataFrame, exact_df: pd.DataFrame, file_col: str = "File"):
    old_used = set(exact_df["df_old_file"])
    new_used = set(exact_df["df_new_file"])
    df_old_rem = df_old[~df_old[file_col].isin(old_used)].reset_index(drop=True)
    df_new_rem = df_new[~df_new[file_col].isin(new_used)].reset_index(drop=True)
    return df_old_rem, df_new_rem


def match_ast_files(
    df_old: pd.DataFrame,
    df_new: pd.DataFrame,
    src_col: str = "SRC",
    file_col: str = "File",
    similarity_threshold: float = 0.9,
    random_seed: int = 42,
) -> pd.DataFrame:
    if fuzz is None:
        raise ImportError(
            "rapidfuzz is required for AST-based file matching. Install it with `pip install rapidfuzz`."
        )

    df_old = df_old.dropna(subset=[src_col]).reset_index(drop=True).copy()
    df_new = df_new.dropna(subset=[src_col]).reset_index(drop=True).copy()

    df_old["AST"] = df_old[src_col].apply(get_java_ast_sequence)
    df_new["AST"] = df_new[src_col].apply(get_java_ast_sequence)

    used_old = set()
    matches = []

    old_indices = list(df_old.index)
    random.Random(random_seed).shuffle(old_indices)
    max_matches = min(len(df_old), len(df_new))

    for _, new_row in df_new.iterrows():
        if len(used_old) >= max_matches:
            break
        if new_row.AST is None:
            continue

        best_score = 0.0
        best_idx = None

        for idx in old_indices:
            if idx in used_old:
                continue
            old_row = df_old.loc[idx]
            if old_row.AST is None:
                continue

            score = fuzz.ratio(new_row.AST, old_row.AST) / 100.0
            if score > best_score:
                best_score = score
                best_idx = idx

        if best_idx is not None and best_score >= similarity_threshold:
            used_old.add(best_idx)
            matches.append(
                {
                    "df_new_file": new_row[file_col],
                    "df_old_file": df_old.loc[best_idx, file_col],
                    "similarity": best_score,
                }
            )

    return pd.DataFrame(matches)


def match_files_full(
    df_old: pd.DataFrame,
    df_new: pd.DataFrame,
    src_col: str = "SRC",
    file_col: str = "File",
    similarity_threshold: float = 0.8,
) -> pd.DataFrame:
    exact_df = exact_path_matches(df_old, df_new, file_col=file_col)
    df_old_rem, df_new_rem = remove_exact_matches(df_old, df_new, exact_df, file_col=file_col)
    ast_df = match_ast_files(
        df_old_rem,
        df_new_rem,
        src_col=src_col,
        file_col=file_col,
        similarity_threshold=similarity_threshold,
    )
    return pd.concat([exact_df, ast_df], ignore_index=True)
