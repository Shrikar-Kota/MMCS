import smtplib, ssl

port = 465
smtp_server = "smtp.gmail.com"
sender_email = "multimediacontentsummarizer@gmail.com"
password = "kiran_9901"


def send_verification_email(receiver_email, url):
    context = ssl.create_default_context()
    message = f"""\
        Subject: VERIFICATION EMAIL

        Please click the link to verify your account.\n\n{url}"""
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
