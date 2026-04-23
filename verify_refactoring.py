#!/usr/bin/env python
"""
Verification script to ensure all modules import correctly and key functionality is available.
Run this to verify the refactoring is complete and functional.
"""

import sys
import traceback
from pathlib import Path

def test_imports():
    """Test that all critical modules can be imported."""
    tests_passed = 0
    tests_failed = 0
    
    test_cases = [
        ("Core config", lambda: __import__('sdp.config', fromlist=['DATASET_NAME_RUN'])),
        ("Data loader", lambda: __import__('sdp.data.loader', fromlist=['load_dataset_pair'])),
        ("Diff utilities", lambda: __import__('sdp.analysis.diff', fromlist=['compute_diff'])),
        ("Java parsing", lambda: __import__('sdp.analysis.java_parse', fromlist=['find_java_classes'])),
        ("Hunk dataclass", lambda: __import__('sdp.analysis.hunk', fromlist=['Hunk'])),
        ("Verdict parser", lambda: __import__('sdp.analysis.verdict_parser', fromlist=['parse_judge_verdict'])),
        ("Metrics", lambda: __import__('sdp.analysis.metrics', fromlist=['compute_metrics'])),
        ("LLM wrapper", lambda: __import__('sdp.llm.wrapper', fromlist=['OpenAIWrapper'])),
        ("Expert system", lambda: __import__('sdp.llm.experts', fromlist=['ExpertDebateSystem'])),
        ("Prompts loader", lambda: __import__('sdp.prompts.loader', fromlist=['load_all_prompts'])),
        ("Prompt: Analyzer", lambda: __import__('sdp.prompts.analyzer', fromlist=['get_analyzer_prompt'])),
        ("Prompt: Proposer", lambda: __import__('sdp.prompts.proposer', fromlist=['get_proposer_prompt'])),
        ("Prompt: Skeptic", lambda: __import__('sdp.prompts.skeptic', fromlist=['get_skeptic_prompt'])),
        ("Prompt: Judge", lambda: __import__('sdp.prompts.judge', fromlist=['get_judge_prompt'])),
        ("Experiment: Orchestrator", lambda: __import__('sdp.experiments.orchestrator', fromlist=['run_all_model_combinations'])),
        ("Experiment: Evaluator", lambda: __import__('sdp.experiments.evaluator', fromlist=['test_skeptic_variants_async'])),
        ("Experiment: Visualization", lambda: __import__('sdp.experiments.visualization', fromlist=['plot_time_vs_debate_rounds'])),
        ("CLI", lambda: __import__('sdp.cli', fromlist=['main'])),
    ]
    
    print("=" * 70)
    print("IMPORT VERIFICATION TEST")
    print("=" * 70)
    
    for test_name, test_fn in test_cases:
        try:
            test_fn()
            print(f"✅ {test_name:.<50} PASS")
            tests_passed += 1
        except Exception as e:
            print(f"❌ {test_name:.<50} FAIL")
            print(f"   Error: {str(e)}")
            traceback.print_exc()
            tests_failed += 1
    
    print("=" * 70)
    print(f"Results: {tests_passed} passed, {tests_failed} failed")
    print("=" * 70)
    
    return tests_failed == 0


def test_key_classes():
    """Test that key classes can be instantiated."""
    print("\n" + "=" * 70)
    print("CLASS INSTANTIATION TEST")
    print("=" * 70)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Hunk dataclass
    try:
        from sdp.analysis.hunk import Hunk
        h = Hunk(
            file_path="test.java",
            src1="old code",
            src2="new code",
            unified_diff="diff",
            changes_dict={},
            relevant_context="context",
            label=1,
            old_label=0,
        )
        print(f"✅ {'Hunk dataclass creation':.<50} PASS")
        tests_passed += 1
    except Exception as e:
        print(f"❌ {'Hunk dataclass creation':.<50} FAIL")
        print(f"   Error: {str(e)}")
        tests_failed += 1
    
    # Test 2: OpenAIWrapper
    try:
        from sdp.llm.wrapper import OpenAIWrapper
        wrapper = OpenAIWrapper(api_keys=["test-key"], base_url="https://api.example.com/v1")
        print(f"✅ {'OpenAIWrapper instantiation':.<50} PASS")
        tests_passed += 1
    except Exception as e:
        print(f"❌ {'OpenAIWrapper instantiation':.<50} FAIL")
        print(f"   Error: {str(e)}")
        tests_failed += 1
    
    # Test 3: ExpertDebateSystem
    try:
        from sdp.llm.wrapper import OpenAIWrapper
        from sdp.llm.experts import ExpertDebateSystem
        wrapper = OpenAIWrapper(api_keys=["test-key"], base_url="https://api.example.com/v1")
        debate = ExpertDebateSystem(llm_client=wrapper, max_rounds=1)
        print(f"✅ {'ExpertDebateSystem instantiation':.<50} PASS")
        tests_passed += 1
    except Exception as e:
        print(f"❌ {'ExpertDebateSystem instantiation':.<50} FAIL")
        print(f"   Error: {str(e)}")
        tests_failed += 1
    
    # Test 4: Verdict parser
    try:
        from sdp.analysis.verdict_parser import parse_judge_verdict, parse_confidence
        verdict, int_val = parse_judge_verdict("### Final Prediction: BENIGN")
        assert verdict == "BENIGN" and int_val == 0, "Verdict parsing failed"
        conf = parse_confidence("### Confidence: 85")
        assert conf == 85, "Confidence parsing failed"
        print(f"✅ {'Verdict parser functions':.<50} PASS")
        tests_passed += 1
    except Exception as e:
        print(f"❌ {'Verdict parser functions':.<50} FAIL")
        print(f"   Error: {str(e)}")
        tests_failed += 1
    
    # Test 5: Metrics computation
    try:
        from sdp.analysis.metrics import normalize_subset, harmonic_mean
        import numpy as np
        norm = normalize_subset("Benign_00")
        assert norm == "B00", "Subset normalization failed"
        hm = harmonic_mean(0.8, 0.6)
        assert not np.isnan(hm), "Harmonic mean computation failed"
        print(f"✅ {'Metrics computation':.<50} PASS")
        tests_passed += 1
    except Exception as e:
        print(f"❌ {'Metrics computation':.<50} FAIL")
        print(f"   Error: {str(e)}")
        tests_failed += 1
    
    # Test 6: Prompt loader
    try:
        from sdp.prompts.loader import load_all_prompts
        loader = load_all_prompts()
        prompt = loader.get_analyzer("diff", "src1", "src2", "BENIGN")
        assert "system" in prompt and "user" in prompt, "Prompt structure invalid"
        print(f"✅ {'Prompt loader':.<50} PASS")
        tests_passed += 1
    except Exception as e:
        print(f"❌ {'Prompt loader':.<50} FAIL")
        print(f"   Error: {str(e)}")
        tests_failed += 1
    
    print("=" * 70)
    print(f"Results: {tests_passed} passed, {tests_failed} failed")
    print("=" * 70)
    
    return tests_failed == 0


def test_java_parsing():
    """Test Java parsing functionality."""
    print("\n" + "=" * 70)
    print("JAVA PARSING TEST")
    print("=" * 70)
    
    try:
        from sdp.analysis.java_parse import find_java_classes, find_java_methods
        
        sample_java = """
        public class TestClass {
            public void testMethod() {
                int x = 5;
            }
        }
        """
        
        classes = find_java_classes(sample_java)
        methods = find_java_methods(sample_java)
        
        assert len(classes) > 0, "No classes found"
        assert len(methods) > 0, "No methods found"
        
        print(f"✅ {'Java class detection':.<50} PASS")
        print(f"✅ {'Java method detection':.<50} PASS")
        print(f"   Found {len(classes)} class(es) and {len(methods)} method(s)")
        return True
    except Exception as e:
        print(f"❌ {'Java parsing':.<50} FAIL")
        print(f"   Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " COMPLEX MODEL SDP - MODULE VERIFICATION ".center(68) + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")
    
    results = []
    
    # Run all tests
    results.append(("Imports", test_imports()))
    results.append(("Classes", test_key_classes()))
    results.append(("Java Parsing", test_java_parsing()))
    
    # Summary
    print("\n" + "=" * 70)
    print("OVERALL VERIFICATION SUMMARY")
    print("=" * 70)
    
    all_passed = all(result[1] for result in results)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<50} {status}")
    
    print("=" * 70)
    
    if all_passed:
        print("\n🎉 ALL VERIFICATION TESTS PASSED! 🎉")
        print("\nThe modular refactoring is complete and functional.")
        print("Ready to run experiments!\n")
        sys.exit(0)
    else:
        print("\n⚠️  SOME TESTS FAILED - Please fix import errors above.")
        sys.exit(1)
