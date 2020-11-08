from django.db import models
from tinymce.models import HTMLField
from taggit.managers import TaggableManager
from django.urls import reverse
from .utils import get_read_time
from markdown_deux import markdown
from .choice import MY_CHOICES
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils import timezone
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.utils.timezone import now
from django.db.models.functions import Now
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime

# from django.utils.text import slugify
from django.template.defaultfilters import slugify
import secrets
import uuid
import os

# now = timezone.now()  # get the current time



CATEGORY = [
    ("vehicle-photo", _("Vehicle photo")),
    ("Vehicle-registration", _("Vehicle registration")),
    ("insurance-police",_("Insurance police")),
    ("other",_("Other")),
]


def image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join("uploads/", filename)


class BlogManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .annotate(
                verify=ExpressionWrapper(
                    Q(schedule__exact=Now()), BooleanField())
            )
        )


class ImageStorage(models.Model):
    title = models.CharField(
        _("Image title if yiu want"), max_length=250, null=True, blank=True
    )
    image = models.ImageField(
        _("Upload any image"), null=True, blank=True, upload_to=image_file_path,
    )
    deleted_at = models.DateTimeField(_("deleted at"), null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title


        

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"{uuid.uuid4()} Image title"
        super(ImageStorage, self).save(*args, **kwargs)


class Category(models.Model):
    category_name = models.CharField(
        _("Category of the post"), max_length=250, null=True, blank=True
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.category_name


class Blog(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post"
    )
    title = models.CharField(
        _("Title of blog post"), max_length=250, null=True, blank=True
    )
    header = models.CharField(
        _("Blog title eg. TIPS, "), max_length=250, null=True, blank=True
    )
    slug = models.SlugField(
        _("Slug of the title"),
        max_length=250,
        unique_for_date="publish",
        null=True,
        blank=True,
    )

    photo = models.ImageField(
        _("Blog post main image"), null=True, blank=True, upload_to=image_file_path,
    )
    read_time = models.TimeField(
        _("Blog post read time"), null=True, blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name=_("Blog category list"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    language = models.CharField(
        _("Blog post programming name if realted to programming"),
        max_length=100,
        choices=MY_CHOICES,
        null=True,
        blank=True,
    )
    publish = models.DateField(blank=True, null=True,)
    photo_url = models.URLField(
        _("Blog post main image url if you don't want to upload image"),
        blank=True,
        null=True,
    )
    tags = TaggableManager(blank=True)
    blog_body = models.TextField(
        _("Blog post body for show case test"), null=True, blank=True
    )
    description = HTMLField(blank=True)
    views = models.IntegerField(_("Total views on post"), default="0")
    post_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="blog_likers",
        blank=True,
        symmetrical=False,
    )
    verified = models.BooleanField(
        _("Approved post before push on production"), default=False
    )
    schedule = models.DateTimeField(
        _("Schedule post by date and time"),
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    seen_at = models.DateTimeField(null=True, blank=True)
    request = models.TextField(null=True, blank=True)
    sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
    key = models.CharField(
        _("Key for email tracking"), max_length=255, null=True, blank=True
    )
    deleted_at = models.DateTimeField(_("deleted at"), null=True, blank=True)
    objects = BlogManager()

    class Meta:
        verbose_name = _("blog")
        verbose_name_plural = _("blogs")

    def get_tags_display(self):
        return self.tags.values_list("name", flat=True)

    def get_tags(self):
        return self.tags.names()

    def number_of_likes(self):
        if self.post_like.count():
            return self.post_like.count()
        else:
            return 0

    def get_markdown(self):
        description = self.description
        markdown_text = markdown(description)
        return mark_safe(markdown_text)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        
        if not self.key:
            self.key = secrets.token_hex(16)

        if self.schedule is None:
            self.schedule = now()
        if not self.sent_at:
            ctx = {
                "author": self.author.fullname
                if self.author.fullname
                else self.author.username,
                "key": self.key,
                "title": self.title,
                "image": self.photo_url if self.photo_url is None else self.photo_url,
                "read_time": self.read_time,
                "publish": self.timestamp,
                "schedule": self.schedule,
                "body": self.blog_body,
                # "tags": self.tags.n,
                "view": self.views,
            }
            tpl = "blog_email.html"
            html_message = render_to_string(tpl, ctx)
            if self.author.email:
                try:
                    send_mail(
                        subject=self.title,
                        message="",
                        html_message=html_message,
                        from_email="SimpleIsBest <contact@vivadrive.io>",
                        recipient_list=[self.author.email],
                    )
                    self.sent_at = now()
                    print("Email Sent to: ", self.author.email)
                except Exception as e:
                    pass
            else:
                self.sent_at = now()
        super(Blog, self).save(*args, **kwargs)

    def get_category_name(self):
        if self.category:
            return self.category.category_name

    @property
    def status(self):
        if self.schedule <= now():
            return ugettext("active")
        return ugettext("schedule")


def pre_save_post(sender, instance, *args, **kwargs):
    if instance.description:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post, sender=Blog)


def generic_upload_blog(instance, filename):
    # return os.path.join(instance.category, folder, filename)
    _datetime = datetime.now()
    datetime_str = _datetime.strftime("%Y-%m-%d")
    return 'Documents/{0}/{1}/{2}/rahul/'.format(instance.name,datetime_str,filename )



class BlogPhoto(models.Model):
  #  created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    blog = models.ForeignKey(Blog, models.CASCADE, verbose_name=_('blog'))
    name = models.CharField(_("Description about image"),max_length=255, null=True, blank=True)
    file = models.ImageField(
        _("Upload documents image"), null=True, blank=True, upload_to=generic_upload_blog, max_length=500
    )



def generic_upload_to(instance, filename):
    # return os.path.join(instance.category, folder, filename)
    _datetime = datetime.now()
    datetime_str = _datetime.strftime("%Y-%m-%d")
    return 'Documents/Fleet/{0}/{1}/{2}/{3}'.format(instance.category, instance.sub_category,datetime_str,filename )

class FavoriteBlog(models.Model):
    favorite_blog = models.ManyToManyField(
        Blog, related_name="favorite", blank=True, symmetrical=False,
    )
    category = models.CharField(max_length=255, choices=CATEGORY, null=True, blank=True)
    sub_category = models.CharField(max_length=255, choices=CATEGORY, null=True, blank=True)
    image = models.ImageField(
        _("Upload documents image"), null=True, blank=True, upload_to=generic_upload_to,
    )


    def number_of_favorite_blog(self):
        if self.favourite_blog.count():
            return self.favourite_blog.count()
        else:
            return 0

    class Meta:
        verbose_name = _("favorite")
        verbose_name_plural = _("favorites")
