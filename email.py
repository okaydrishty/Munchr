import smtplib 
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()


smtp_server=os.getenv("SMTP_SERVER")
smtp_pass=os.getenv("SMTP_PASS")
port=int(os.getenv("PORT_NO",587))
sender_mail=os.getenv("SENDER_MAIL")


def send_email(msg:EmailMessage):
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_mail, smtp_pass)
            server.send_message(msg)
    except Exception as e:
        raise Exception(f"Failed to send email: {e}")