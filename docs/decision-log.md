# Decision log

1. **AmazonHelp brand selection** — I chose AmazonHelp after reviewing brand volumes because it had sufficient conversation volume (586 in my sample) and diverse issue types; trade-off: results may not generalize to other brands.

2. **100K sample from 3M dataset** — I sampled for faster iteration while maintaining enough data for analysis; trade-off: may miss rare edge cases present in full dataset.

3. **10-intent taxonomy** — I developed this from the data to keep annotation tractable while covering major issue types; trade-off: some ambiguous cases don't fit cleanly.

4. **Keyword-based training labels** — I used simple keyword matching instead of human labeling for training data to iterate quickly; trade-off: training labels are noisy compared to human labels.

5. **Dummy embeddings** — I used random vectors instead of real OpenAI embeddings to avoid API costs during development; trade-off: can't evaluate real retrieval quality.

6. **54-example golden set** — I hand-labeled this many examples due to time constraints; trade-off: below the 150-250 I'd recommend for statistical significance.

7. **TF-IDF baseline** — I chose this as my "simple" baseline because it's interpretable and fast; trade-off: doesn't capture semantic meaning like embeddings would.

8. **Majority baseline** — I included this trivial baseline to show the improvement from any actual signal; trade-off: sets a very low bar.

9. **LLM judge rubric** — I implemented a 5-dimension rubric for response quality; trade-off: didn't have time to measure human-judge agreement.

10. **Conversation-level split** — I split by conversation ID to prevent leakage; trade-off: reduces effective training data compared to message-level split.

11. **No UI focus** — I prioritized backend correctness over frontend polish; trade-off: the UI is functional but not production-ready.

12. **Macro F1 reporting** — I emphasized macro F1 alongside accuracy to protect minority intents; trade-off: macro F1 is sensitive to class imbalance and annotation ambiguity.
