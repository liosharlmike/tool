# User Guide

## Dashboard
The dashboard shows environment state, tool availability, and context for assessments.

## Running a safe assessment
Use:
`python main.py --target 192.168.1.0/24 --purpose "authorized internal assessment" --scope "lab" --authorize --dashboard --report`

The application validates the target and checks authorization before continuing. Unauthorized scanning is rejected.

## AI Assistant
If Ollama is available and configured, the AI assistant can explain scan findings and remediation guidance.

## Reporting
Reports are generated in the `reports/` directory as HTML, JSON, and TXT files.
