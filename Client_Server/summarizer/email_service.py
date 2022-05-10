import smtplib, ssl
from email.mime.text import MIMEText

port = 465
smtp_server = "smtp.gmail.com"
sender_email = "multimediacontentsummarizer@gmail.com"
password = "3ed5ec66ca3003"

def send_summmary_generated_notification_mail(receiver_email, username, url, filename):
    body = f"Hello {username},\n\tYour request to generate summary for the file {filename} has been processed and the summary has been generated successfully. Please click the below link to download the summary.\n\n{url}.\n\nNote: This email is sent to <{receiver_email}>. Please ignore if you are not the intended receiver.\n\nDO NOT REPLY TO THIS MESSAGE."
    message = MIMEText(body)
    message['Subject'] = "SUMMARY GENERATED"
    message['From'] = sender_email
    message['To'] = receiver_email
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

