# Data pipeline

I built this pipeline to turn the raw Kaggle CSV into a clean, analysis-ready dataset. Supply the CSV locally (raw data is intentionally not committed). Run the numbered scripts in order from this directory. `03_select_brand.py` prints measured eligibility information and requires an actual `author_id`; I chose AmazonHelp after reviewing the volume and diversity of available brands.

I did human review for both the taxonomy and resolution-pair labels before creating embeddings. For faster iteration, I used keyword-based classification in `10_label_resolution_pairs.py` and dummy embeddings in `06_build_embeddings.py` (since I didn't want to incur API costs during development).

After reviewing and labeling the exported pairs, run `06_build_embeddings.py --brand AmazonHelp`, then run `11_mock_import.py` (or `07_import_resolution_pairs.py` with PostgreSQL). The import script only accepts one brand, fully labeled pairs, and 1536-dimension vectors. This is the final step that makes historical evidence available to the backend.
