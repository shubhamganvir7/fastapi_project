import smtplib
from fastapi import HTTPException
from smtplib import SMTPException
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import random
import socket


# SMTP configuration
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "shubhfast1@gmail.com"
SMTP_PASSWORD = "toxoltgachvggmbl"

# Email templates
VERIFY_EMAIL_TEMPLATE = """
<html>
<head></head>
<body>
    <h2>Email Verification</h2>
    <p>Dear $username,</p>
    <p>Your OTP is: <strong>$otp</strong></p>
</body>
</html>
"""


def send_verification_email(username: str, email: str, otp: str):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Email Verification"
    message["From"] = SMTP_USERNAME
    message["To"] = email

    html_template = Template(VERIFY_EMAIL_TEMPLATE)
    html_content = html_template.substitute(username=username, otp=otp)

    part = MIMEText(html_content, "html")
    message.attach(part)

    try:
        with smtplib.SMTP(SMTP_HOST,SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, email, message.as_string())
    except SMTPException as e:
        raise HTTPException(status_code=500, detail="Failed to send email.")


# from fastapi import FastAPI, Request, Form

# from starlette.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

# import smtplib
# from email.message import EmailMessage

# templates = Jinja2Templates(directory="templates")

# app = FastAPI()

# app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")


# @app.get("/")
# def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


# @app.post("/submit")
# def submit(name: str = Form(), emailAddress: str = Form(), message: str = Form()):
#     print(name)
#     print(emailAddress)
#     print(message)

#     email_address = "shubhfast1@gmail.com"
#     email_password = "toxoltgachvggmbl"


#     msg = EmailMessage()
#     msg['Subject'] = "Email subject"
#     msg['From'] = email_address
#     msg['To'] = "shubhfast1@gmail.com"
#     msg.set_content(
#         f"""\
#     Name : {name}
#     Email : {emailAddress}
#     Message : {message}    
#     """,

#     )

#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#         smtp.login(email_address, email_password)
#         smtp.send_message(msg)

#     return "email successfully sent to Shubham"
