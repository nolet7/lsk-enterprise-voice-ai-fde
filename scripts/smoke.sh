#!/usr/bin/env bash
set -euo pipefail
curl -fsS http://127.0.0.1:18743/healthz
python -m pytest -q tests
