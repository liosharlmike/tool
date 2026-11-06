#!/usr/bin/env bash
set -eu

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

if ! grep -qi "kali" /etc/os-release 2>/dev/null; then
  echo "Warning: This suite is designed for Kali Linux, but the current system does not appear to be Kali." >&2
fi

python3 --version >/dev/null 2>&1 || { echo "Python 3 is required but not available." >&2; exit 1; }

mkdir -p "$PROJECT_ROOT"/{reports,logs,data,config,backups,exports}

if [ ! -d "$PROJECT_ROOT/.venv" ]; then
  python3 -m venv "$PROJECT_ROOT/.venv"
fi

# shellcheck disable=SC1091
source "$PROJECT_ROOT/.venv/bin/activate"
python -m pip install --upgrade pip >/dev/null
python -m pip install -r "$PROJECT_ROOT/requirements.txt"

if [ -f "$PROJECT_ROOT/config/app_config.json" ]; then
  echo "Configuration already present."
else
  cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
fi

python "$PROJECT_ROOT/main.py" --dashboard

echo "Installation complete. Use ./scripts/launch.sh to run the application."
