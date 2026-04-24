import os
import time
import random
from pathlib import Path
from queue import Queue, Empty
from threading import Thread, Lock, Event
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

import pandas as pd
from tqdm.auto import tqdm

from ..analysis.diff import compute_diff
from ..analysis.method_of_difference import generate_prompt, generate_prompt_v2
from ..llm.wrapper import OpenAIWrapper

RESULT_COLUMNS = [
    "File",
    "Bug_290",
    "Bug_300",
    "SRC_290",
    "SRC_300",
    "method",
    "model",
    "prompt",
    "response",
    "time_taken",
]

SYSTEM_PROMPT = (
    "You are a seasoned software engineer and code reviewer with a sharp eye for detail and a deep understanding "
    "of programming best practices. Your expertise spans multiple programming languages, frameworks, and development "
    "environments, allowing you to scrutinize code thoroughly for bugs, logical errors, security vulnerabilities, and "
    "performance issues. You're adept at interpreting complex code snippets and identifying subtle defects that could "
    "cause runtime failures or bugs. Your approach is methodical and precise, combining analytical skills with a solid "
    "grasp of coding standards and idiomatic practices. Whether it's reviewing a small function or a large codebase, your "
    "insights are clear, constructive, and aimed at improving code quality and reliability."
)


def gather_existing_results(
    base_save_path: str,
    lucene290_path: str = None,
    lucene300_path: str = None,
    generate_prompt_func=generate_prompt,
) -> pd.DataFrame:
    all_results = []
    base_path = Path(base_save_path)
    if not base_path.exists():
        return pd.DataFrame(columns=RESULT_COLUMNS)

    for method_folder in base_path.iterdir():
        if not method_folder.is_dir():
            continue
        for model_folder in method_folder.iterdir():
            if not model_folder.is_dir():
                continue
            csv_file = model_folder / "results.csv"
            if not csv_file.exists():
                continue
            try:
                df = pd.read_csv(csv_file)
                df["method"] = int(method_folder.name)
                df["model"] = model_folder.name
                all_results.append(df)
            except Exception:
                continue

    if not all_results:
        return pd.DataFrame(columns=RESULT_COLUMNS)

    combined = pd.concat(all_results, ignore_index=True)

    if lucene290_path is not None and os.path.exists(lucene290_path):
        lucene290 = pd.read_csv(lucene290_path)
        lucene290 = lucene290.rename(columns={"SRC": "SRC_290"})
        combined = combined.merge(lucene290[["File", "SRC_290"]], on="File", how="left")

    if lucene300_path is not None and os.path.exists(lucene300_path):
        lucene300 = pd.read_csv(lucene300_path)
        lucene300 = lucene300.rename(columns={"SRC": "SRC_300"})
        combined = combined.merge(lucene300[["File", "SRC_300"]], on="File", how="left")

    prompts = []
    for _, row in combined.iterrows():
        prompt = generate_prompt_func(
            src1=row["SRC_290"],
            src2=row["SRC_300"],
            bug_label=int(row["Bug_290"]),
            diffs=compute_diff(row["SRC_290"], row["SRC_300"]),
            method=int(row["method"]),
        )
        prompts.append(prompt)

    combined["prompt"] = prompts
    for col in RESULT_COLUMNS:
        if col not in combined.columns:
            combined[col] = None
    return combined[RESULT_COLUMNS]


def run_experiments_parallel_safe(
    df_codes: pd.DataFrame,
    methods: List[int],
    models: List[str],
    save_path: str,
    max_workers: int = 5,
    per_future_timeout: int = 30,
    retries: int = 3,
    base_delay: float = 1.0,
    generate_prompt_func=generate_prompt,
    system_prompt: str = SYSTEM_PROMPT,
) -> List[Dict]:
    save_base = Path(save_path)
    save_base.mkdir(parents=True, exist_ok=True)

    done = set()
    all_results = []
    done_lock = Lock()
    result_queue = Queue()
    stop_event = Event()

    if save_base.exists():
        existing = gather_existing_results(save_path, generate_prompt_func=generate_prompt_func)
        done.update(zip(existing["File"], existing["method"], existing["model"]))
        all_results.extend(existing.to_dict("records"))

    def writer():
        while not stop_event.is_set():
            try:
                item = result_queue.get(timeout=0.5)
            except Empty:
                continue
            if item == "DONE":
                break
            key = (item["File"], item["method"], item["model"])
            with done_lock:
                if key in done:
                    result_queue.task_done()
                    continue
                done.add(key)

            folder = save_base / str(item["method"]) / item["model"]
            folder.mkdir(parents=True, exist_ok=True)
            csv_file = folder / "results.csv"
            row = {k: v for k, v in item.items() if k in RESULT_COLUMNS}
            df = pd.DataFrame([row])
            if csv_file.exists():
                df.to_csv(csv_file, index=False, header=False, mode="a")
            else:
                df.to_csv(csv_file, index=False)
            all_results.append(item)
            result_queue.task_done()

    writer_thread = Thread(target=writer, daemon=True)
    writer_thread.start()

    def process_row_with_retry(row, method, model_name):
        key = (row["File"], method, model_name)
        with done_lock:
            if key in done or stop_event.is_set():
                return

        src1 = row["SRC_290"]
        src2 = row["SRC_300"]
        bug_label = int(row["Bug_290"])
        diffs = compute_diff(src1, src2)
        prompt = generate_prompt_func(src1=src1, src2=src2, bug_label=bug_label, diffs=diffs, method=method)

        wrapper = OpenAIWrapper()
        for attempt in range(retries):
            if stop_event.is_set():
                return
            start = time.time()
            try:
                response = wrapper.create_completion(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.00001,
                    max_tokens=2048,
                )
                end = time.time()
                break
            except Exception as exc:
                wait = base_delay * (2 ** attempt)
                time.sleep(wait)
                if attempt == retries - 1:
                    return
                continue

        result = {
            "File": row["File"],
            "Bug_290": bug_label,
            "Bug_300": row.get("Bug_300"),
            "SRC_290": src1,
            "SRC_300": src2,
            "method": method,
            "model": model_name,
            "prompt": prompt,
            "response": response,
            "time_taken": round(end - start, 4),
        }
        result_queue.put(result)

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for model_name in models:
                for method in methods:
                    rows = [row for _, row in df_codes.iterrows()]
                    for row in rows:
                        if (row["File"], method, model_name) not in done:
                            futures.append(executor.submit(process_row_with_retry, row, method, model_name))

            for f in tqdm(as_completed(futures), total=len(futures), desc="Experiment jobs"):
                try:
                    f.result(timeout=per_future_timeout)
                except Exception:
                    continue
    finally:
        stop_event.set()
        result_queue.put("DONE")
        writer_thread.join()

    return all_results
