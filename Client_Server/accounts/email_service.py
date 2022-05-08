import smtplib, ssl
from email.mime.text import MIMEText

port = 465
smtp_server = "smtp.gmail.com"
sender_email = "multimediacontentsummarizer@gmail.com"
password = "3ed5ec66ca3003"


def send_verification_email(receiver_email, username, url):
    body = f"Hello {username},\n\tThanks for creating an account with us. As a part of verification, you need to click the below link to verify your account. The link expires in 24 hours.\n\n{url}.\n\nNote: This email is sent to <{receiver_email}>. Please ignore if you are not the intended receiver.\n\nDO NOT REPLY TO THIS MESSAGE."
    message = MIMEText(body)
    message['Subject'] = "ACCOUNT VERIFICATION"
    message['From'] = sender_email
    message['To'] = receiver_email
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def send_forgotpassword_email(receiver_email, username, url):
    body = f"Hello {username},\n\tA request to reset the password of your account has been sent to the server. Please click the link given below to reset your passwod. The link expires in 10 minutes. Please ignore this message if you haven't requested for the reset.\n\n{url}.\n\nNote: This email is sent to <{receiver_email}>. Please ignore if you are not the intended receiver.\n\nDO NOT REPLY TO THIS MESSAGE."
    message = MIMEText(body)
    message['Subject'] = "FORGOT PASSWORD"
    message['From'] = sender_email
    message['To'] = receiver_email
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

