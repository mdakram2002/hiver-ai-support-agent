def aggregate_judge_scores(rows):

    keys = ["groundedness", "relevance", "helpfulness", "completeness", "tone"]
    return {key: sum(r[key] for r in rows) / len(rows) for key in keys} if rows else {}
