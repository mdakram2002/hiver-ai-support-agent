"""Download the official Customer Support on Twitter dataset via KaggleHub."""

import argparse
import shutil
from pathlib import Path

import kagglehub


DATASET_ID = "thoughtvector/customer-support-on-twitter"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=Path("data/raw/twcs.csv"))
    parser.add_argument("--force", action="store_true", help="Replace an existing target CSV.")
    args = parser.parse_args()
    if args.target.exists() and not args.force:
        raise FileExistsError(f"{args.target} already exists. Use --force to replace it.")
    print(f"Downloading Kaggle dataset: {DATASET_ID}")
    download_dir = Path(kagglehub.dataset_download(DATASET_ID))
    csv_files = sorted(download_dir.rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in KaggleHub cache directory {download_dir}.")
    source = next((path for path in csv_files if path.name.lower() == "twcs.csv"), csv_files[0])
    args.target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, args.target)
    print(f"Copied {source.name} to {args.target}")
    print(f"Dataset size: {args.target.stat().st_size / 1024**3:.2f} GiB")


if __name__ == "__main__":
    main()
