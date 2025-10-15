#!/usr/bin/env bash
set -euo pipefail

# Simple helper to tag a release and remind about Zenodo
if [ $# -lt 1 ]; then
  echo "Usage: ./scripts/make_release.sh vX.Y.Z"
  exit 1
fi

TAG="$1"

# Lint & test
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest ruff black
ruff check .
black --check .
pytest -q

# Git tag
git add -A
git commit -m "chore(release): ${TAG}" || true
git tag -a "${TAG}" -m "Release ${TAG}"
git push origin "${TAG}" || true

echo "==> Reminder:"
echo " - Create GitHub Release for ${TAG} (attach wheel/zip if desired)"
echo " - If Zenodo is linked, a DOI will be minted on first release."
echo " - Update CITATION.cff with the minted DOI."
