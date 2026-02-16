# PyMailer V1.1.0
# Developed By Atif © 2026 Atif's Codeworks.

import sys
import os
import ssl
import smtplib
import mimetypes
import ctypes
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton,
    QFileDialog, QMessageBox, QFrame,
    QSystemTrayIcon, QMenu
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QAction


# =========================
# Load Environment Variables Safely
# =========================

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SENDER_NAME = os.getenv("SENDER_NAME", "Regular Human")
SIGNATURE_NAME = os.getenv("SIGNATURE_NAME", SENDER_NAME)
GREET = os.getenv("GREET", "Best regards")

if not all([SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD]):
    raise RuntimeError(
        "Missing SMTP configuration. Please run setup.py before starting PYMailer."
    )

SMTP_PORT = int(SMTP_PORT)


# =========================
# Email Thread
# =========================
class EmailThread(QThread):
    status = pyqtSignal(str)
    success = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        try:
            import html

            self.status.emit("Preparing email...")

            msg = EmailMessage()
            msg["From"] = f"{SENDER_NAME} <{EMAIL_ADDRESS}>"
            msg["To"] = self.data["recipient"]
            msg["Subject"] = self.data["subject"]

            if self.data["cc"]:
                msg["Cc"] = self.data["cc"]
            if self.data["bcc"]:
                msg["Bcc"] = self.data["bcc"]

            # Preserve line breaks and escape HTML
            body_text = self.data["body"]
            safe_body = html.escape(body_text)
            body_html = safe_body.replace("\n", "<br>")

            html_body = f"""
<div style="width: 90%; max-width: 600px; margin: 30px auto; background: #fafafa; border-radius: 20px; border: 1px solid #ddd; font-family: Verdana, sans-serif; color: #333; overflow: hidden;">
    
    <div style="background: linear-gradient(to right, #2563eb, #38bdf8); padding: 20px 30px; text-align: center;">
        <h1 style="margin: 0; font-size: 26px; font-weight: bold; color: #ffffff;">
            {SENDER_NAME}
        </h1>
    </div>

    <div style="padding: 30px;">
        <p style="font-size: 15px; line-height: 1.6;">
            {body_html}
        </p>

        <p style="margin-top: 40px;">{GREET},</p>

        <p style="margin-top: 5px; font-weight: bold; font-size: 14px;">
            {SIGNATURE_NAME}
        </p>
    </div>

    <div style="background: #e2e8f0; padding: 20px; text-align: center; font-size: 13px; color: #444;">
        <p style="margin: 0;">
            Sent from <b>PyMailer</b> By Atif's Codeworks.
        </p>
    </div>

</div>
"""

            msg.set_content(body_text)
            msg.add_alternative(html_body, subtype="html")

            # Attachment
            if self.data["attachment"]:
                self.status.emit("Attaching file...")
                mime_type, _ = mimetypes.guess_type(self.data["attachment"])

                if mime_type:
                    maintype, subtype = mime_type.split("/")
                else:
                    maintype, subtype = "application", "octet-stream"

                with open(self.data["attachment"], "rb") as f:
                    msg.add_attachment(
                        f.read(),
                        maintype=maintype,
                        subtype=subtype,
                        filename=os.path.basename(self.data["attachment"])
                    )

            self.status.emit("Connecting to server...")
            context = ssl.create_default_context()

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls(context=context)
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

                self.status.emit("Uploading to server...")
                server.send_message(msg)

            self.status.emit("Email sent successfully.")
            self.success.emit()

        except Exception as e:
            self.error.emit(str(e))


# =========================
# Main Window
# =========================
class PYMailer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Atif's Codeworks - PYMailer")
        self.setWindowIcon(QIcon("mail.ico"))
        self.resize(900, 720)

        self.attachment_path = None

        self.init_ui()
        self.apply_styles()
        self.init_tray()

    def init_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(40, 40, 40, 40)

        self.container = QFrame()
        self.container.setObjectName("container")
        layout = QVBoxLayout(self.container)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Compose Email")
        title.setFont(QFont("Verdana", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.recipient = self.create_input(layout, "Recipient")
        self.cc = self.create_input(layout, "CC")
        self.bcc = self.create_input(layout, "BCC")
        self.subject = self.create_input(layout, "Subject")

        self.body = QTextEdit()
        self.body.setPlaceholderText("Type your message here...")
        self.body.setMinimumHeight(200)
        layout.addWidget(self.body)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        attach_btn = QPushButton("Choose Attachment")
        attach_btn.clicked.connect(self.choose_file)
        layout.addWidget(attach_btn)

        self.send_btn = QPushButton("Send Email")
        self.send_btn.clicked.connect(self.send_email)
        layout.addWidget(self.send_btn)

        outer_layout.addWidget(self.container)

    def create_input(self, layout, placeholder):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        layout.addWidget(field)
        return field

    def choose_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Attachment")
        if file:
            self.attachment_path = file

    def send_email(self):
        if not self.recipient.text() or not self.body.toPlainText():
            QMessageBox.warning(self, "Error", "Recipient and Body required.")
            return

        self.fade_ui(True)

        data = {
            "recipient": self.recipient.text(),
            "cc": self.cc.text(),
            "bcc": self.bcc.text(),
            "subject": self.subject.text(),
            "body": self.body.toPlainText(),
            "attachment": self.attachment_path
        }

        self.thread = EmailThread(data)
        self.thread.status.connect(self.status_label.setText)
        self.thread.success.connect(self.handle_success)
        self.thread.error.connect(self.handle_error)
        self.thread.start()

    def fade_ui(self, sending):
        self.container.setEnabled(not sending)

    def handle_success(self):
        self.fade_ui(False)
        self.reset_form()
        QMessageBox.information(self, "Success", "Email sent successfully.")

    def handle_error(self, error):
        self.fade_ui(False)
        QMessageBox.critical(self, "Error", error)

    def reset_form(self):
        self.recipient.clear()
        self.cc.clear()
        self.bcc.clear()
        self.subject.clear()
        self.body.clear()
        self.attachment_path = None
        self.status_label.clear()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1c1f2b;
                color: #e3f2fd;
                font-family: Verdana;
                font-size: 14px;
            }

            QFrame#container {
                background-color: #2b2f3b;
                border-radius: 15px;
            }

            QLineEdit, QTextEdit {
                background-color: #1c1f2b;
                border: 2px solid #34495e;
                border-radius: 8px;
                padding: 8px;
            }

            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #009ffd;
            }

            QPushButton {
                background-color: #009ffd;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2a72c4;
            }
        """)

    def init_tray(self):
        icon = QIcon(os.path.abspath("mail.ico"))
        self.setWindowIcon(icon)

        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(icon)
        self.tray.setToolTip("Atif's Codeworks - PYMailer")

        menu = QMenu()

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.showNormal)

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(QApplication.quit)

        menu.addAction(open_action)
        menu.addSeparator()
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.show()


# =========================
# App Entry
# =========================
if __name__ == "__main__":
    myappid = "atifs.codeworks.pymailer.1.0"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    window = PYMailer()
    window.show()
    sys.exit(app.exec())
