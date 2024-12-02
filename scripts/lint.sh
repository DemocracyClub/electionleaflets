#!/bin/bash
set -euxo pipefail

uv run ruff check .
