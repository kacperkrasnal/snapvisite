from django.core.mail import send_mail
from django.conf import settings


def account_confirmation_mail(username, user_email, user_id):
    confirmation_url = f"http://127.0.0.1:8000/account/mail-confirmation/{user_id}/"
    subject = "Thanks for open account in our service."
    message = f"\
    {username}\n\
    Welcome in Snapvisite service. We are happy to see you here.\n\
    Don't waste your time and snap your first visit!\n\
    Our service is still very young, so fell good to send to us your fresh ideas about new functionalities.\n\
    Now you need to confirm your e-mail address. To make it, click link below:\n\
    {confirmation_url}\n\
    Thank you!"

    from_email = settings.EMAIL_HOST_USER
    to_email = [user_email, ]
    send_mail(subject, message, from_email, to_email)
