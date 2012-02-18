#!/usr/bin/env python
#-*- coding: utf-8 -*- 
import smtplib
from email.mime.text import MIMEText


def send_mail(subject, message, from_email, recipient_list, smtp_server,email_port,auth_user=None, auth_password=None):            
    server = smtplib.SMTP(smtp_server,email_port)        
    if auth_user and auth_password:
        try:
          server.login(auth_user, auth_password)
        except:              
          try:
            server.esmtp_features["auth"] = "LOGIN PLAIN" # This has been added
            server.login(auth_user, auth_password)
          except:
            raise
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = recipient_list
    server.sendmail(from_email, recipient_list, msg.as_string())        
    # Quit serve    
    server.quit()


def send_mail_ex(subject, message, sender, recipient, smtp_server,email_port,auth_user=None, auth_password=None):            
    server = smtplib.SMTP(smtp_server,email_port)        
    if auth_user and auth_password:
        try:
          server.login(auth_user, auth_password)
        except:              
          try:
            server.esmtp_features["auth"] = "LOGIN PLAIN" # This has been added
            server.login(auth_user, auth_password)
          except:
            raise
     # Make sure email addresses do not contain non-ASCII characters
    sender    = sender.encode('ascii')
    recipient = recipient.encode('ascii')
    # Prepare message
    msg = MIMEText(message.encode("UTF-8"), 'plain', "UTF-8")
    msg['From'] = sender
    msg['To'] = recipient    
    msg['Subject'] = subject
    # Send message
    server.sendmail(sender, recipient, msg.as_string())        
    # Quit serve    
    server.quit()

