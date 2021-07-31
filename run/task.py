from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from custom_user import secrets



@shared_task
def send_mail_to_user(user_otp,email):
    subject = 'OTP'
    email_from = secrets.EMAIL_HOST_USER
    recipient_list = [email, ] 
    send_mail(subject,user_otp,email_from,recipient_list)
    return '{} mail sent'