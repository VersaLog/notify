from VersaLog import *
import api_req
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib
import os

logger = VersaLog(enum="detailed", show_tag=True, tag="Request")

load_dotenv()

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def create_message(subject: str, body: str) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"] = os.getenv("MY_MAIL_ADDRESS")
    msg["To"] = os.getenv("TO_MAIL_ADDRESS")
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    return msg


def send_gmail(msg: MIMEMultipart):
    with smtplib.SMTP_SSL(
        os.getenv("SMTP_SERVER"),
        int(os.getenv("SMTP_PORT"))
    ) as server:
        server.login(
            os.getenv("MY_MAIL_ADDRESS"),
            os.getenv("APP_PASS")
        )
        server.send_message(msg)


def log_and_send(level: str, message: str):
    if level == "info":
        logger.info(message)
    elif level == "error":
        logger.error(message)
    elif level == "warn":
        logger.warn(message)

    subject = "[Weather API Notification]"
    if level == "error":
        subject = "[ERROR] Weather API Failure"

    mail = create_message(subject, message)
    send_gmail(mail)

    logger.info("Gmail notification sent successfully")


def weather_task():
    success, result = api_req.get_weather(
        location="Tokyo",
        api_key=WEATHER_API_KEY
    )

    if success:
        log_and_send("info", result)
    else:
        log_and_send("error", result)


if __name__ == "__main__":
    logger.info("Weather notification task started")
    weather_task()
