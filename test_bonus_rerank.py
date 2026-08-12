"""
Script kiểm thử nhanh cho Exercise 3.5 (Bonus Reranking).
Đo Context Recall & Context Precision trước và sau khi gọi rerank_by_overlap().
"""

import sys
import json

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from template import RAGASEvaluator, rerank_by_overlap

def main():
    with open("artifacts/actual_answers.json", "r", encoding="utf-8") as f:
        actual_answers = json.load(f)["answers"]

    with open("golden_dataset.json", "r", encoding="utf-8") as f:
        golden_pairs = {q["id"]: q for q in json.load(f)["qa_pairs"]}

    evaluator = RAGASEvaluator()
    test_ids = ["E02", "E05", "M04", "M07", "H04"]

    print("=== KẾT QUẢ THỬ NGHIỆM RERANKING (Exercise 3.5 Bonus) ===")
    print("| ID | Recall (Trước) | Recall (Sau) | Precision (Trước) | Precision (Sau) | Mức tăng Precision |")
    print("|---|---:|---:|---:|---:|---:|")

    rec_befores, rec_afters, prec_befores, prec_afters = [], [], [], []

    for qid in test_ids:
        act = next(a for a in actual_answers if a["id"] == qid)
        gold = golden_pairs[qid]
        expected = gold["expected_answer"]
        question = gold["question"]
        retrieved_chunks = [c["text"] for c in act["retrieved_contexts"]]

        rec_b = evaluator.evaluate_context_recall(retrieved_chunks, expected)
        prec_b = evaluator.evaluate_context_precision(retrieved_chunks, expected)

        reranked_chunks = rerank_by_overlap(retrieved_chunks, question)

        rec_a = evaluator.evaluate_context_recall(reranked_chunks, expected)
        prec_a = evaluator.evaluate_context_precision(reranked_chunks, expected)

        delta_p = prec_a - prec_b

        rec_befores.append(rec_b)
        rec_afters.append(rec_a)
        prec_befores.append(prec_b)
        prec_afters.append(prec_a)

        print(f"| {qid} | {rec_b:.3f} | {rec_a:.3f} | {prec_b:.3f} | {prec_a:.3f} | +{delta_p:.3f} |")

    avg_rec_b = sum(rec_befores) / len(rec_befores)
    avg_rec_a = sum(rec_afters) / len(rec_afters)
    avg_prec_b = sum(prec_befores) / len(prec_befores)
    avg_prec_a = sum(prec_afters) / len(prec_afters)
    avg_delta = avg_prec_a - avg_prec_b

    print(f"| **Trung bình** | **{avg_rec_b:.3f}** | **{avg_rec_a:.3f}** | **{avg_prec_b:.3f}** | **{avg_prec_a:.3f}** | **+{avg_delta:.3f}** |")

if __name__ == "__main__":
    main()
