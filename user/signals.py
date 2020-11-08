# from django.core.mail import EmailMultiAlternatives
# from django.dispatch import receiver
# from django.template.loader import render_to_string
# from django.urls import reverse

# from django_rest_passwordreset.signals import reset_password_token_created
# from django.core.mail import send_mail
# from django.contrib.auth import get_user_model
# from django.db.models.signals import pre_save

# from .models import User
# import pyotp


# User = get_user_model()

# def generate_key():
#     """ User otp key generator """
#     key = pyotp.random_base32()
#     if is_unique(key):
#         return key
#     generate_key()

# def is_unique(key):
#     try:
#         User.objects.get(token=key)
#     except User.DoesNotExist:
#         return True
#     return False

# @receiver(pre_save, sender=User)
# def create_key(sender, instance, **kwargs):
#     """This creates the key for users that don't have keys"""
#     if not instance.key:
#         instance.key = generate_key()

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'fullname': reset_password_token.user.fullname,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format("/evbus/reset/password/", reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('user/password_reset.html', context)
    email_plaintext_message = render_to_string(
        'user/password_reset.txt', context)


    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="General"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@digitalmobility.pl",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
