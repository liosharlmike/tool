#!/usr/bin/env bash
set -eu

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

for path in "$PROJECT_ROOT"/reports "$PROJECT_ROOT"/logs "$PROJECT_ROOT"/data "$PROJECT_ROOT"/config "$PROJECT_ROOT"/backups "$PROJECT_ROOT"/exports; do
  if [ ! -d "$path" ]; then
    echo "Missing required directory: $path" >&2
    exit 1
  fi
done

if [ ! -f "$PROJECT_ROOT/requirements.txt" ]; then
  echo "requirements.txt is missing." >&2
  exit 1
fi

if [ -d "$PROJECT_ROOT/.venv" ]; then
  echo "Virtual environment present: $PROJECT_ROOT/.venv"
else
  echo "Virtual environment missing" >&2
  exit 1
fi

python "$PROJECT_ROOT/main.py" --dashboard >/dev/null

echo "Health check passed."
