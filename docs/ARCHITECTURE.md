# Architecture

The Liosharl suite is organized around a small set of service layers: configuration, secure process control, validation and authorization, persistent storage, feature modules, and a terminal UI.

## Core layers
- `core/` contains configuration, authorization, validation, logging, database access, and central process execution.
- `integrations/` contains adapters for external tools such as Nmap, NVD, and Ollama.
- `modules/` contains feature-specific orchestration logic for dashboard, network, vulnerability, web, AI, reporting and history.
- `ui/` provides the terminal interface rendered through rich text.

## Execution flow
1. Application loads configuration.
2. Logging and environment state are initialized.
3. User input is validated and authorization is checked.
4. Feature modules execute their relevant operations.
5. Results are stored in SQLite and optionally exported to reports.

## Security controls
- No `shell=True` execution is used.
- Commands are passed as argument lists with timeouts.
- Local data is stored under controlled directories.
- Sensitive values are redacted during logging.
