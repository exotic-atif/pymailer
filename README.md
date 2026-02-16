# 📦 PYMailer

A modern desktop email sender built with Python & PyQt6.  
Clean UI. Safe configuration. Version-aware installer.  

Developed by **Atif's Codeworks**

---

## ✨ Features

- Modern PyQt6 Desktop UI
- HTML Styled Emails
- Configurable Branding (Company Name, Signature, Greeting)
- Version-aware Installer & Updater
- Dependency Auto-Check (with user consent)
- Secure `.env` configuration
- No Git required for installation

---

# 🚀 Quick Install (Recommended)

Open **PowerShell** in the folder where you want PYMailer installed and run:

```powershell
iwr https://raw.githubusercontent.com/exotic-atif/pymailer/main/install.py -OutFile install.py; python install.py; Remove-Item install.py
```

This will:
1. Download installer
2. Install or update PYMailer
3. Check required dependencies
4. Clean up installer file

No Git required.

---

# 🧠 Requirements

- Python 3.9 or higher
- Internet connection
- Gmail / Yahoo / Outlook (or custom SMTP provider)

Check Python version:

```powershell
python --version
```

If Python is not installed, download from:
https://www.python.org/downloads/

---

# 🔐 Getting Your Email App Password (IMPORTANT)

⚠️ Do NOT use your normal email password.

You must generate an **App Password**.

---

## 📧 Gmail App Password

### Step 1 — Enable 2-Step Verification

Go to:
https://myaccount.google.com/security

Enable **2-Step Verification**.

### Step 2 — Generate App Password

Go to:
https://myaccount.google.com/apppasswords

1. Select App: Mail
2. Select Device: Windows Computer
3. Click Generate
4. Copy the 16-character password

Example:
```
abcd efgh ijkl mnop
```

Use that password inside PYMailer setup.

---

## 📧 Outlook App Password

1. Go to:
https://account.microsoft.com/security
2. Enable Two-Step Verification
3. Create App Password
4. Use generated password

---

## 📧 Yahoo App Password

1. Go to:
https://login.yahoo.com/account/security
2. Enable Two-Step Verification
3. Generate App Password

---

# ⚙️ First-Time Setup

After installation, run:

```powershell
python setup.py
```

This will:
- Ask your email provider
- Set correct SMTP automatically
- Ask for company name
- Ask for signature name
- Ask for greeting
- Save configuration safely in `.env`

No manual editing required.

---

# ▶ Running PYMailer

After setup:

```powershell
python pymailer.py
```

Or double-click:
```
pymailer.pyw
```

---

# 🔄 Updating PYMailer

To check for updates, run the install command again:

```powershell
iwr https://raw.githubusercontent.com/exotic-atif/pymailer/main/install.py -OutFile install.py; python install.py; Remove-Item install.py
```

The installer will:
- Compare versions using `.ver`
- Skip if latest
- Prompt if update available

Safe and automatic.

---

# 🧩 Project Structure

```
PYMailer/
│
├── pymailer.py       # Main application
├── pymailer.pyw      # Consoleless UI 
├── setup.py          # Setup wizard
├── install.py        # Installer / Updater
├── .ver              # Version file
├── mail.ico          # Application icon
└── README.md
```

---

# 🛡 Security Notes

- App passwords are stored in `.env`
- Do NOT share your `.env` file
- Do NOT commit `.env` to GitHub
- Regenerate password if exposed

---

# 🧪 Troubleshooting

## Error: "PyQt6 not found"

Run:

```powershell
pip install PyQt6 python-dotenv
```

Or rerun installer and approve dependency installation.

---

## Error: SMTP Authentication Failed

Check:
- App password is correct
- 2-Step Verification enabled
- SMTP server correct

---

# 🏗 Built With

- Python
- PyQt6
- python-dotenv
- Standard Library Installer System

---

# 📜 License

MIT License  
© 2026 Atif Arman — Atif's Codeworks

---

# ❤️ Final Words

PYMailer was designed to be:

Simple  
Secure  
Install-friendly  
Future-proof  

Happy coding.  
— Atif's Codeworks
