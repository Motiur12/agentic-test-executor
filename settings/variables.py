import os


# Store local credentials in environment variables, never in source control.
VARIABLES = {
    "USERNAME": os.getenv("CARTUP_USERNAME"),
    "PASSWORD": os.getenv("CARTUP_PASSWORD"),
    "OTP": os.getenv("CARTUP_OTP"),
}
