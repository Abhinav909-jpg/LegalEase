#!/usr/bin/env python
"""
LegaleEase RAG Evaluation Benchmark CLI
Measures:
- Precision@5
- Recall@5
- Answer Faithfulness
- Citation Correctness
- Response Latency
"""
import json
from app.rag.evaluation import RAGEvaluator

def main():
    print("=" * 65)
    print("      LEGALEASE RAG PIPELINE EVALUATION BENCHMARK      ")
    print("=" * 65)
    evaluator = RAGEvaluator()
    summary = evaluator.run_evaluation(top_k=5)

    print(f"\nTotal Queries Evaluated: {summary['total_queries_evaluated']}")
    print(f"Top-K (Retrieval Depth):  {summary['top_k']}")
    print("-" * 65)
    print(f"Mean Retrieval Precision@5:    {summary['mean_precision_at_k'] * 100:.2f}%")
    print(f"Mean Retrieval Recall@5:       {summary['mean_recall_at_k'] * 100:.2f}%")
    print(f"Mean Citation Correctness:     {summary['mean_citation_correctness'] * 100:.2f}%")
    print(f"Mean Answer Faithfulness:      {summary['mean_faithfulness'] * 100:.2f}%")
    print(f"Mean Response Latency:         {summary['mean_latency_seconds']:.3f} seconds")
    print("-" * 65)
    print("\nDetailed Query Breakdown:")
    for res in summary["detailed_results"]:
        print(f"[{res['query_id']}] Category: {res['category']}")
        print(f"     Query:       {res['query']}")
        print(f"     Prec@5:      {res['precision_at_k']:.2f} | Recall@5: {res['recall_at_k']:.2f}")
        print(f"     Citation:    {res['citation_correctness']:.2f} | Faithfulness: {res['faithfulness']:.2f}")
        print(f"     Latency:     {res['latency_seconds']:.3f}s")
        print()
    print("=" * 65)

if __name__ == "__main__":
    main()
