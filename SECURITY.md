# Credential setup

This project reads CartUp credentials from environment variables. Set them in
your shell before running a test:

```powershell
$env:CARTUP_USERNAME = "your-username"
$env:CARTUP_PASSWORD = "your-password"
$env:CARTUP_OTP = "your-otp"
python main.py
```

Alternatively, copy `.env.example` to a local `.env` file and fill in the
values. `.env` files are ignored by Git and are loaded by the application with
the Python standard library, so no additional dependency is required. Shell
environment variables take precedence over `.env` values.

If a placeholder such as `${PASSWORD}` is used without its environment
variable, execution stops with an actionable error instead of submitting an
empty or literal placeholder value.
