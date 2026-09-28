#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
npm run build
npm test
python3 infrastructure/provision.py
python3 infrastructure/deploy.py
