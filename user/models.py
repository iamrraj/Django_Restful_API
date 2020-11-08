from django.db import models
import uuid
import os
from django.urls import reverse
from django.db.models.signals import post_save
from datetime import datetime
from django.dispatch import receiver
from django.conf import settings
from django.db import models
from base64 import b64encode
import random
from datetime import datetime, timedelta
from pytz import utc
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from oauth2_provider.models import AccessToken
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from oauth2_provider.models import AbstractAccessToken

# Create your models here.


def image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join("uploads/", filename)


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(
            email=self.normalize_email(email), username=username.lower(), **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    fullname = models.CharField(max_length=60, blank=True)
    country_code = models.CharField(max_length=60, blank=True)
    phone_number = models.CharField(max_length=60, blank=True)
    website = models.CharField(max_length=240, blank=True)
    private_account = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(
        upload_to=image_file_path, default="avatar.png")
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="user_followers",
        blank=True,
        symmetrical=False,
    )
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="user_following",
        blank=True,
        symmetrical=False,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=255, blank=True)
    

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    # def save(self):
    #     if self.country_code:
    #         self.phone_number = self.country_code + self.phone_number

    def number_of_followers(self):
        if self.followers.count():
            return self.followers.count()
        else:
            return 0

    def number_of_following(self):
        if self.following.count():
            return self.following.count()
        else:
            return 0

    def __str__(self):
        return self.username

    # Once you will register you will get confirmation email  on registration email!
    def send_confirmation_email(self):
        confirm_url = reverse("users_confirm", args=[self.token])
        ctx = {"user": self.username, "confirm_url": confirm_url}
        tpl = "user/registration_email.html"
        html_message = render_to_string(tpl, ctx)
        send_mail(
            subject="Registration confirmation email",
            message="",
            html_message=html_message,
            from_email="SimpleBlog <contact@vivadrive.io>",
            recipient_list=[self.email],
        )

    # Welcome message confirmation once your register is successful !
    def send_welcome_email(self):
        ctx = {
            "user": self.username,
        }
        tpl = "user/welcome_email.html"
        html_message = render_to_string(tpl, ctx)
        send_mail(
            subject="Welcome to Simple Blog Family",
            message="",
            html_message=html_message,
            from_email="SimpleBlog <simpleblogvivadrive.io>",
            recipient_list=[self.email],
        )

    def authenticate(self, otp):
        """ This method authenticates the given otp"""
        provided_otp = 0
        try:
            provided_otp = int(otp)
        except:
            return False
        # Here we are using Time Based OTP. The interval is 60 seconds.
        # otp must be provided within this interval or it's invalid
        t = pyotp.TOTP(self.key, interval=300)
        return t.verify(provided_otp)


# @receiver(post_save, sender=AccessToken, dispatch_uid="record_last_login")
# def record_login(sender, instance, created, **kwargs):
#     if created:
#         instance.user.last_login = datetime.now()
#         instance.user.save()


# class Application(AbstractAccessToken):
#     login_time = models.DateTimeField(_("Login time"), auto_now_add=True, null=True)


class UserActivityLogging(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_("user"), default=None)
    user_ipv4 = models.CharField(_("user ipv4"), max_length=16, blank=True)
    event_type = models.CharField(_("event type"), max_length=255, blank=True)
    endpoint = models.TextField(_("endpoint"), blank=True)
    request_method = models.CharField(_("request method"), max_length=10, blank=True)
    response_status = models.CharField(_("response status"), max_length=255, blank=True)
    response_content_type = models.CharField(_("response content type"), max_length=255, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def delete(self, *args, **kwargs):
        return

    class Meta:
        verbose_name = _("user actvity logging")
        verbose_name_plural = _("users actvities loggings")


class ForgottenPasswordToken(models.Model):
    series = models.CharField(max_length=255, primary_key=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True, db_column='ip_adress')
    token_end_date = models.DateTimeField(null=True, blank=True)
    token_value = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, db_column='t_user')
    success = models.BooleanField( default=False)
    ts = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def send_email(self):
        ctx = {
            "user": self.user.username,
            'action_url': "https://beautiresume.herokuapp.com/reset/password/" + "?token=" + self.token_value,
        }
        tpl = "user/password_forget.html"
        html_message = render_to_string(tpl, ctx)
        send_mail(
            subject="Forget Password Email From MyFleet",
            message="",
            html_message=html_message,
            from_email="SimpleBlog <simple@vivadrive.io>",
            recipient_list=[self.user.email],
        )

    def save(self, *args, **kwargs):
        if not self.series:
            self.series = b64encode(
                bytes((
                    random.randint(0,255)
                    for i in range(settings.DDPAUTH_FORGOTTEN_PASSWORD_SERIES_LENGTH)
                )),
                altchars=b'-_'
            ).decode('latin1')
        if not self.token_value:
            self.token_value = b64encode(
                bytes((
                    random.randint(0,255)
                    for i in range(settings.DDPAUTH_FORGOTTEN_PASSWORD_TOKEN_LENGTH)
                )),
                altchars=b'-_'
            ).decode('latin1')

        if self.token_end_date is None:
            self.token_end_date = datetime.now(tz=utc) + timedelta(
                seconds=settings.DDPAUTH_FORGOTTEN_PASSWORD_TOKEN_VALIDITY_SECONDS)

        super().save(*args, **kwargs)


class UserPasswordHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_("user"), default=None)
    password = models.CharField(_('password'), max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
