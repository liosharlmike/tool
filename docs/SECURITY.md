# Security Notes

## Authorization model
This application requires a clear target, purpose, and explicit authorization flag before performing active assessment work.

## Safe execution
- No automatic privilege escalation.
- No `shell=True` command execution.
- External tools are invoked with argument separation.
- Timeouts and error capture are enforced.

## Data handling
- Sensitive values are redacted before logging.
- Reports are stored in controlled directories.
- Secrets remain in `.env` files and are not committed to source control. 
