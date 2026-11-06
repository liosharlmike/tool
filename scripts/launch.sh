#!/usr/bin/env bash
set -eu

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

if [ ! -d "$PROJECT_ROOT/.venv" ]; then
  echo "Virtual environment not found. Run ./scripts/install.sh first." >&2
  exit 1
fi

# shellcheck disable=SC1091
source "$PROJECT_ROOT/.venv/bin/activate"
python -m pip install -r "$PROJECT_ROOT/requirements.txt" >/dev/null 2>&1 || true

if [ "${1:-}" = "--gui" ] || [ "${1:-}" = "gui" ]; then
  python "$PROJECT_ROOT/gui.py"
  exit 0
fi

python "$PROJECT_ROOT/main.py" "$@"
