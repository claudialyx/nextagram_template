import boto3, botocore
from app import app
import sendgrid
import os
import json
from models.user import User
from flask_login import current_user
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

# verifying credentials
s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

def email_notification(amount, receiver, image_name):
    from_email=Email('donation@nextagram.com')
    to_receiver_email=Email(receiver.email)
    to_donor_email=Email(current_user.email)
    subject='[NEXTAGRAM] Donation'
    content = Content("text/plain", f'{current_user.username} has donated {amount} to {receiver.username} for the following image: {image_name}')
    mail=Mail(from_email, subject, to_receiver_email, content)
    mail1=Mail(from_email, subject, to_donor_email, content)
    response=sg.client.mail.send.post(request_body=mail.get())
    response=sg.client.mail.send.post(request_body=mail1.get())
