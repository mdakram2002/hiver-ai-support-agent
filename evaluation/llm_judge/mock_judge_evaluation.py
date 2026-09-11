"""Mock LLM judge evaluation for demonstration purposes."""

import json
import random
import warnings
from pathlib import Path
import pandas as pd

warnings.filterwarnings("ignore")


def mock_judge_response(message, intent, evidence, reply):
    """Generate mock judge scores for demonstration."""
    # Simulate judge scores
    scores = {
        "groundedness": random.randint(3, 5),
        "relevance": random.randint(3, 5),
        "helpfulness": random.randint(3, 5),
        "completeness": random.randint(3, 5),
        "tone": random.randint(4, 5),
        "unsupported_claims": random.choice([True, False]),
        "rationale": "Mock evaluation for demonstration purposes"
    }
    return scores


def main():
    # Load golden set
    golden_path = Path(__file__).parent.parent / "golden_set/golden_set_annotated.csv"
    if not golden_path.exists():
        print("Golden set not found. Cannot run judge evaluation.")
        return
    
    df = pd.read_csv(golden_path)
    print(f"Loaded {len(df)} examples from golden set")
    
    # Generate mock responses for demonstration
    # In production, these would come from the AI agent
    mock_responses = []
    for _, row in df.iterrows():
        mock_response = f"Thank you for contacting us about your {row['expected_intent']}. We're here to help."
        mock_responses.append(mock_response)
    
    df['ai_response'] = mock_responses
    
    # Run mock judge evaluation
    judge_results = []
    for _, row in df.iterrows():
        result = mock_judge_response(
            message=row['customer_message'],
            intent=row['expected_intent'],
            evidence="Mock historical evidence for demonstration",
            reply=row['ai_response']
        )
        result['id'] = row['id']
        judge_results.append(result)
    
    # Calculate aggregate statistics
    avg_scores = {
        'groundedness': sum(r['groundedness'] for r in judge_results) / len(judge_results),
        'relevance': sum(r['relevance'] for r in judge_results) / len(judge_results),
        'helpfulness': sum(r['helpfulness'] for r in judge_results) / len(judge_results),
        'completeness': sum(r['completeness'] for r in judge_results) / len(judge_results),
        'tone': sum(r['tone'] for r in judge_results) / len(judge_results),
        'unsupported_claims_rate': sum(1 for r in judge_results if r['unsupported_claims']) / len(judge_results)
    }
    
    # Save results
    results = {
        "evaluation_type": "MOCK_LLM_JUDGE",
        "total_examples": len(judge_results),
        "average_scores": {k: round(v, 2) for k, v in avg_scores.items()},
        "note": "This is a mock evaluation. In production, actual AI agent responses would be evaluated.",
        "individual_results": judge_results
    }
    
    output_path = Path(__file__).parent.parent.parent / "reports/llm_judge_results.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Mock LLM judge evaluation completed")
    print(f"Average scores:")
    for metric, score in avg_scores.items():
        print(f"  {metric}: {score:.2f}")
    print(f"Results saved to {output_path}")


if __name__ == "__main__":
    main()