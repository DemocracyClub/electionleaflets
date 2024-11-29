#!/bin/bash
set -euxo pipefail

pipenv run ruff check .
