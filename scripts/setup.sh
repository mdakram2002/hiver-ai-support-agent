#!/usr/bin/env sh
set -eu
cp -n .env.example .env 2>/dev/null || true
(cd backend && npm install)
(cd frontend && npm install)
python -m pip install -r data-pipeline/requirements.txt
echo "Set SELECTED_BRAND and OPENAI_API_KEY in .env after inspecting the dataset."
