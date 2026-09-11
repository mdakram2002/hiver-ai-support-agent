# Golden-set annotation guide

I annotated 54 customer messages from AmazonHelp conversations, keeping their source conversation IDs for traceability. I sampled from the evaluation set (isolated from training) to ensure no leakage. For each example, I:

1. **Intent classification**: Assigned one of my 10 intents based on the customer's core issue
2. **Escalation decision**: Marked as true when an autonomous reply would be unsafe or lacks a supported resolution
3. **Expected resolution**: Wrote a short, evidence-grounded outcome (not a fabricated reply)
4. **Difficulty rating**: Categorized as easy/medium/hard based on ambiguity and complexity
5. **Notes**: Added context about why I made specific labeling decisions

I focused on including edge cases and ambiguous examples to stress-test the system. Given time constraints, I did single annotation rather than dual annotation, though I recognize dual annotation would be ideal for measuring inter-annotator agreement.