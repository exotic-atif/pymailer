# PYMailer Setup Wizard
# © 2026 Atif's Codeworks

import os
import getpass

PROVIDERS = {
    "1": {
        "name": "Gmail",
        "SMTP_SERVER": "smtp.gmail.com",
        "SMTP_PORT": "587"
    },
    "2": {
        "name": "Yahoo",
        "SMTP_SERVER": "smtp.mail.yahoo.com",
        "SMTP_PORT": "587"
    },
    "3": {
        "name": "Outlook",
        "SMTP_SERVER": "smtp.office365.com",
        "SMTP_PORT": "587"
    }
}


def get_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.\n")


def get_valid_port(prompt):
    while True:
        port = input(prompt).strip()
        if port.isdigit():
            return port
        print("Port must be a number.\n")


def escape_env(value):
    return value.replace('"', '\\"')


def main():

    print(r"█████▄ ██  ██ ██▄  ▄██  ▄▄▄  ▄▄ ▄▄    ▄▄▄▄▄ ▄▄▄▄    ▄█████ ▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄ ▄▄ ▄▄▄▄  ")
    print(r"██▄▄█▀  ▀██▀  ██ ▀▀ ██ ██▀██ ██ ██    ██▄▄  ██▄█▄   ▀▀▀▄▄▄ ██▄▄    ██   ██ ██ ██▄█▀ ")
    print(r"██       ██   ██    ██ ██▀██ ██ ██▄▄▄ ██▄▄▄ ██ ██   █████▀ ██▄▄▄   ██   ▀███▀ ██    ")
    print()

    print("Select Email Provider:\n")
    print("1) Gmail")
    print("2) Yahoo")
    print("3) Outlook")
    print("4) Custom SMTP\n")

    choice = input("Enter choice (1-4): ").strip()

    if choice in PROVIDERS:
        provider = PROVIDERS[choice]
        smtp_server = provider["SMTP_SERVER"]
        smtp_port = provider["SMTP_PORT"]

        print(f"\nSelected: {provider['name']}")
        print(f"SMTP Server: {smtp_server}")
        print(f"SMTP Port: {smtp_port}")

    elif choice == "4":
        print("\nCustom SMTP Configuration\n")
        print("Common SMTP Examples:")
        print("  Gmail: smtp.gmail.com")
        print("  Yahoo: smtp.mail.yahoo.com")
        print("  Outlook: smtp.office365.com")
        print("  Zoho: smtp.zoho.com")
        print("  cPanel hosting: mail.yourdomain.com\n")

        smtp_server = get_non_empty("Enter SMTP Host: ")
        smtp_port = get_valid_port("Enter SMTP Port (e.g. 587 or 465): ")

    else:
        print("\nInvalid choice.")
        return

    print("\n========== Account Configuration ==========\n")

    email_address = get_non_empty("Enter Email Address: ")
    email_password = getpass.getpass("Enter Email App Password (Won't be visible): ").strip()

    if not email_password:
        print("Password cannot be empty.")
        return

    print("\n========== Branding Configuration ==========\n")

    sender_name = get_non_empty("Enter Company Name (Email Header Name): ")
    signature_name = get_non_empty("Enter Signature Name (Displayed in email): ")
    greet = get_non_empty("Enter Greeting (e.g. Best regards): ")

    # Overwrite check
    if os.path.exists(".env"):
        print("\nA configuration file (.env) already exists.")
        confirm = input("Do you want to overwrite it? (y/n): ").strip().lower()

        if confirm != "y":
            print("\nSetup cancelled. Existing configuration preserved.\n")
            input("Press Enter to exit setup.")
            return

    # Write .env file
    with open(".env", "w", encoding="utf-8") as f:
        f.write(f"SMTP_SERVER={smtp_server}\n")
        f.write(f"SMTP_PORT={smtp_port}\n")
        f.write(f"EMAIL_ADDRESS=\"{escape_env(email_address)}\"\n")
        f.write(f"EMAIL_PASSWORD=\"{escape_env(email_password)}\"\n")
        f.write(f"SENDER_NAME=\"{escape_env(sender_name)}\"\n")
        f.write(f"SIGNATURE_NAME=\"{escape_env(signature_name)}\"\n")
        f.write(f"GREET=\"{escape_env(greet)}\"\n")

    print("\nConfiguration saved successfully.")
    print("'.env' file has been created.\n")
    print("You can now run PYMailer.\n")

    input("Press Enter to exit setup.")


if __name__ == "__main__":
    main()
