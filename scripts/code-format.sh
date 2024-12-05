#!/bin/bash
set -euxo pipefail

uv run ruff format .
uv run ruff check . --fix
