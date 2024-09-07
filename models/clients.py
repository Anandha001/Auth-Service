import smtplib
from configs.base_config import BaseConfig

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(BaseConfig.SENDER_EMAIL, BaseConfig.SENDER_PASSWORD)
