"""
Command-line interface for running defect prediction experiments.
"""
import argparse
import logging
import sys
from typing import Optional

from .config import DATASET_NAME_RUN, DATA_DIR, llm7_all_models
from .data.loader import load_dataset_pair
from .analysis.diff import compute_diffs
from .llm.wrapper import OpenAIWrapper
from .llm.experts import ExpertDebateSystem


def setup_logger(level=logging.INFO):
    """Configure logging for the CLI."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def run_defect_prediction(
    dataset_name: str = DATASET_NAME_RUN,
    max_samples: Optional[int] = None,
    model: str = "gpt-4.1-nano-2025-04-14",
    debate_rounds: int = 3,
) -> None:
    """
    Run defect prediction on a dataset using the expert debate system.
    
    Args:
        dataset_name: Name of the dataset (e.g., 'camel', 'lucene')
        max_samples: Maximum number of samples to process (None = all)
        model: Model name to use for all experts
        debate_rounds: Number of debate rounds
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Loading dataset: {dataset_name}")
    
    try:
        # Load dataset pair
        past_version, new_version = load_dataset_pair(dataset_name)
        logger.info(f"Loaded {len(past_version)} samples from {dataset_name}")
        
        # Initialize LLM client and debate system
        llm_client = OpenAIWrapper()
        debate_system = ExpertDebateSystem(
            llm_client=llm_client,
            analyzer_model=model,
            proposer_model=model,
            skeptic_model=model,
            judge_model=model,
            max_rounds=debate_rounds,
        )
        
        # Process samples
        sample_count = 0
        for idx, row in past_version.iterrows():
            if max_samples and sample_count >= max_samples:
                break
            
            file_name = row.get("File")
            bug_label = row.get("Bug")
            src = row.get("SRC")
            
            if not all([file_name, src]):
                logger.warning(f"Skipping sample {idx}: missing File or SRC")
                continue
            
            # Find corresponding file in new version
            new_row = new_version[new_version["File"] == file_name]
            if new_row.empty:
                logger.debug(f"File {file_name} not found in new version")
                continue
            
            new_src = new_row.iloc[0].get("SRC")
            if not new_src:
                logger.warning(f"Skipping {file_name}: missing SRC in new version")
                continue
            
            # Compute diff
            try:
                diffs = compute_diffs(src, new_src)
                if not diffs or all(len(v) == 0 for v in diffs.values()):
                    logger.debug(f"No diffs found for {file_name}")
                    continue
            except Exception as e:
                logger.error(f"Error computing diff for {file_name}: {e}")
                continue
            
            # Run debate
            logger.info(f"Processing {file_name} (sample {sample_count + 1})")
            try:
                prediction, confidence, history = debate_system.run_debate(
                    diff_text="\n".join(diffs.get("unified", [])),
                    src1_context=src[:500],  # Truncate for context
                    src2_context=new_src[:500],
                    context=new_src[:1000],
                    previous_status="BENIGN" if bug_label == 0 else "DEFECTIVE",
                )
                
                logger.info(f"  → Prediction: {prediction} (confidence: {confidence}%)")
                sample_count += 1
            except Exception as e:
                logger.error(f"Error running debate for {file_name}: {e}")
                continue
        
        logger.info(f"Completed processing {sample_count} samples")
    
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Run defect prediction experiments with expert debate system."
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default=DATASET_NAME_RUN,
        help=f"Dataset name (default: {DATASET_NAME_RUN})",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Maximum number of samples to process (default: all)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4.1-nano-2025-04-14",
        help="Model to use for all experts (default: gpt-4.1-nano-2025-04-14)",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=3,
        help="Number of debate rounds (default: 3)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models and exit",
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logger(level=getattr(logging, args.log_level))
    logger = logging.getLogger(__name__)
    
    # List models if requested
    if args.list_models:
        logger.info("Available models:")
        for model in llm7_all_models:
            print(f"  - {model}")
        sys.exit(0)
    
    # Run defect prediction
    run_defect_prediction(
        dataset_name=args.dataset,
        max_samples=args.max_samples,
        model=args.model,
        debate_rounds=args.rounds,
    )


if __name__ == "__main__":
    main()
