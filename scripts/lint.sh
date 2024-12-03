#!/bin/bash
set -euxo pipefail

uv run ruff format . --check
uv run ruff check .
