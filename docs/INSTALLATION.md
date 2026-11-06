# Installation Guide

## Kali Linux setup
1. Ensure Python 3 is installed.
2. Clone or copy the project into a working directory.
3. Create a virtual environment: `python3 -m venv .venv`
4. Activate it: `source .venv/bin/activate`
5. Install dependencies: `python -m pip install -r requirements.txt`
6. Use `./scripts/install.sh` for the default setup workflow.

## Optional external tools
The suite gracefully handles missing tools. If you want richer coverage, install Kali packages such as:
- `nmap`
- `whatweb`
- `nikto`
- `sqlmap`
- `gobuster`
- `curl`

## Starting the application
- `./scripts/launch.sh --dashboard`
- or `python main.py --dashboard`
