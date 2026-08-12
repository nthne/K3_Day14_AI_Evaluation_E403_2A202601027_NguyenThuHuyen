"""
Hướng dẫn chạy DeepEval thử nghiệm trên dữ liệu RAG Lab 14.

Điều kiện tiền đề:
    pip install deepeval

Chạy lệnh:
    python test_deepeval.py
    hoặc
    deepeval test run test_deepeval.py
"""

import os
import json
from dotenv import load_dotenv

load_dotenv(".env")

try:
    from deepeval import evaluate
    from deepeval.test_case import LLMTestCase
    from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
except ImportError:
    print("Chưa cài đặt deepeval. Hãy chạy: pip install deepeval")
    exit(1)

def run_deepeval_demo():
    # 1. Đọc dữ liệu từ artifacts
    with open("artifacts/actual_answers.json", "r", encoding="utf-8") as f:
        actual_answers = json.load(f)["answers"]

    with open("golden_dataset.json", "r", encoding="utf-8") as f:
        golden_pairs = {q["id"]: q for q in json.load(f)["qa_pairs"]}

    # Chọn 2 cases tiêu biểu để demo
    demo_ids = ["E01", "E03"]
    test_cases = []

    for qid in demo_ids:
        act = next(a for a in actual_answers if a["id"] == qid)
        gold = golden_pairs[qid]

        retrieved_texts = [c["text"] for c in act["retrieved_contexts"]]

        test_case = LLMTestCase(
            input=gold["question"],
            actual_output=act["actual_answer"],
            expected_output=gold["expected_answer"],
            retrieved_contexts=retrieved_texts
        )
        test_cases.append(test_case)

    # 2. Khởi tạo các metrics của DeepEval (sử dụng GPT-4o-mini qua API KEY trong .env)
    faithfulness_metric = FaithfulnessMetric(threshold=0.7, model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    relevancy_metric = AnswerRelevancyMetric(threshold=0.7, model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

    print("=== Đang chạy DeepEval Benchmark ===")
    evaluate(test_cases, [faithfulness_metric, relevancy_metric])

if __name__ == "__main__":
    run_deepeval_demo()
