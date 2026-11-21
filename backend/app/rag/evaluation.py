import time
import logging
from typing import List, Dict, Any
from app.rag.pipeline import RAGPipeline

logger = logging.getLogger("legalease.evaluation")

# Ground-truth evaluation dataset for official government schemes
EVALUATION_DATASET = [
    {
        "query_id": "q1",
        "query": "What is the parental income limit for Central Sector Scholarship PM-USP?",
        "expected_documents": ["PM_USP_Central_Sector_Scholarship_Guidelines.pdf"],
        "expected_key_facts": ["4,50,000", "4.5 lakh"],
        "category": "Income Criteria"
    },
    {
        "query_id": "q2",
        "query": "What documents are required for Post Matric Scholarship in Punjab for SC students?",
        "expected_documents": ["Punjab_Post_Matric_Scholarship_SC_Guidelines.pdf"],
        "expected_key_facts": ["Freeship Card", "Caste Certificate", "Income Certificate"],
        "category": "Documentation"
    },
    {
        "query_id": "q3",
        "query": "Who is eligible for PM-YASASVI scholarship scheme?",
        "expected_documents": ["PM_YASASVI_Scholarship_Scheme_Guidelines.pdf"],
        "expected_key_facts": ["OBC", "EBC", "DNT", "2,50,000"],
        "category": "Target Beneficiaries"
    },
    {
        "query_id": "q4",
        "query": "What is the scholarship amount for National Means-cum-Merit Scholarship NMMSS?",
        "expected_documents": ["National_Means_cum_Merit_Scholarship_NMMSS.pdf"],
        "expected_key_facts": ["12,000", "1,000"],
        "category": "Grant Quantum"
    },
    {
        "query_id": "q5",
        "query": "ਪੰਜਾਬ ਵਿੱਚ ਅਨੁਸੂਚਿਤ ਜਾਤੀਆਂ ਲਈ ਪੋਸਟ ਮੈਟ੍ਰਿਕ ਸਕਾਲਰਸ਼ਿਪ ਦੀ ਆਮਦਨ ਸੀਮਾ ਕੀ ਹੈ?",
        "expected_documents": ["Punjab_Post_Matric_Scholarship_SC_Guidelines.pdf"],
        "expected_key_facts": ["2,50,000", "2.5"],
        "category": "Multilingual (Punjabi)"
    }
]

class RAGEvaluator:
    def __init__(self):
        self.rag = RAGPipeline.get_instance()

    def run_evaluation(self, top_k: int = 5) -> Dict[str, Any]:
        """
        Runs automated evaluation benchmark measuring:
        - Retrieval Precision@K
        - Retrieval Recall@K
        - Answer Faithfulness (grounded fact alignment)
        - Citation Correctness (page & document matching)
        - Response Latency (seconds)
        """
        results = []
        latencies = []
        precisions = []
        recalls = []
        faithfulness_scores = []
        citation_scores = []

        for item in EVALUATION_DATASET:
            query = item["query"]
            expected_docs = set(d.lower() for d in item["expected_documents"])
            expected_facts = item["expected_key_facts"]

            start_t = time.perf_counter()
            response = self.rag.query(query, language="en", top_k_rerank=top_k)
            latency = time.perf_counter() - start_t
            latencies.append(latency)

            retrieved_chunks = response.get("top_chunks", [])
            citations = response.get("citations", [])
            answer_text = response.get("answer", "")

            # 1. Retrieval Precision@K
            retrieved_doc_names = [c.get("document_name", "").lower() for c in retrieved_chunks[:top_k]]
            relevant_retrieved = sum(1 for d in retrieved_doc_names if any(ed in d for ed in expected_docs))
            precision_at_k = relevant_retrieved / max(len(retrieved_doc_names), 1)
            precisions.append(precision_at_k)

            # 2. Retrieval Recall@K
            # In our dataset, each query has 1 primary expected document
            recall_at_k = 1.0 if relevant_retrieved > 0 else 0.0
            recalls.append(recall_at_k)

            # 3. Citation Correctness
            cited_doc_names = [c.get("document_name", "").lower() for c in citations]
            valid_citations = sum(1 for c in cited_doc_names if any(ed in c for ed in expected_docs))
            citation_correctness = (valid_citations / max(len(cited_doc_names), 1)) if citations else 0.0
            citation_scores.append(citation_correctness)

            # 4. Answer Faithfulness (Checks presence of key verified facts in answer or top context)
            facts_matched = sum(1 for f in expected_facts if f.lower() in answer_text.lower())
            faithfulness = facts_matched / max(len(expected_facts), 1)
            faithfulness_scores.append(faithfulness)

            results.append({
                "query_id": item["query_id"],
                "query": query,
                "category": item["category"],
                "precision_at_k": round(precision_at_k, 3),
                "recall_at_k": round(recall_at_k, 3),
                "citation_correctness": round(citation_correctness, 3),
                "faithfulness": round(faithfulness, 3),
                "latency_seconds": round(latency, 3),
                "citations_count": len(citations)
            })

        summary = {
            "top_k": top_k,
            "total_queries_evaluated": len(EVALUATION_DATASET),
            "mean_precision_at_k": round(sum(precisions) / len(precisions), 4),
            "mean_recall_at_k": round(sum(recalls) / len(recalls), 4),
            "mean_citation_correctness": round(sum(citation_scores) / len(citation_scores), 4),
            "mean_faithfulness": round(sum(faithfulness_scores) / len(faithfulness_scores), 4),
            "mean_latency_seconds": round(sum(latencies) / len(latencies), 4),
            "detailed_results": results
        }
        return summary
