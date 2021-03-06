import smtplib, ssl
from email.mime.text import MIMEText

port = 465
smtp_server = "smtp.gmail.com"
sender_email = "multimediacontentsummarizer@gmail.com"
password = "rbwnpgfaemycwjlc"

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

def send_summmary_processing_notification_mail(receiver_email, username, filename):
    body = f"Hello {username},\n\tYour request to generate summary for the file {filename} has been processed and the summary generation process has started.\n\n Note: This email is sent to <{receiver_email}>. Please ignore if you are not the intended receiver.\n\nDO NOT REPLY TO THIS MESSAGE."
    message = MIMEText(body)
    message['Subject'] = "SUMMARY GENERATION PROCESS STARTED"
    message['From'] = sender_email
    message['To'] = receiver_email
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def send_summmary_failed_notification_mail(receiver_email, username, filename):
    body = f"Hello {username},\n\tYour request to generate summary for the file {filename} has failed.\n\n Note: This email is sent to <{receiver_email}>. Please ignore if you are not the intended receiver.\n\nDO NOT REPLY TO THIS MESSAGE."
    message = MIMEText(body)
    message['Subject'] = "SUMMARY GENERATION PROCESS FAILED"
    message['From'] = sender_email
    message['To'] = receiver_email
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# def reset_password_mail(receiver_email, username, url):
#     body = f"Hello {username},\n\tA request to reset the password of your account has been sent to the server. Please click the link given below to reset your passwod. The link expires in 10 minutes. Please ignore this message if you haven't requested for the password reset.\n\n{url}.\n\nNote: This email is sent to <{receiver_email}>. Please ignore if you are not the intended receiver.\n\nDO NOT REPLY TO THIS MESSAGE."
#     message = MIMEText(body)
#     message['Subject'] = "RESET PASSWORD"
#     message['From'] = sender_email
#     message['To'] = receiver_email
    
#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message.as_string())
