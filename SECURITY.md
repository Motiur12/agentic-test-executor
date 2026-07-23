# Credential setup

This project reads CartUp credentials from environment variables. Set them in
your shell before running a test:

```powershell
$env:CARTUP_USERNAME = "your-username"
$env:CARTUP_PASSWORD = "your-password"
$env:CARTUP_OTP = "your-otp"
python main.py
```

Alternatively, keep those names in a local `.env` file for your own tooling;
`.env` files are ignored by Git. The application itself deliberately does not
load `.env` files, so no additional dependency is required.

If a placeholder such as `${PASSWORD}` is used without its environment
variable, execution stops with an actionable error instead of submitting an
empty or literal placeholder value.
