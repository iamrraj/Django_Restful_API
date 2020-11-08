from django.db import models
from django.db import models
from tinymce.models import HTMLField
from taggit.managers import TaggableManager
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
import secrets
import uuid
import os
from django.db.models import Q
from django.utils.translation import override, ugettext_lazy as _

# Create your models here.

User = get_user_model()


def image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join("uploads/", filename)


class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=200)
    icon = models.ImageField(
        _("Category Icon Image"), upload_to=image_file_path, blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categorys")


class Product(models.Model):
    seller = models.ForeignKey(
        User, related_name="user_product", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, related_name="product_category", on_delete=models.CASCADE
    )
    title = models.CharField(_("Product title or name"), max_length=250)
    slug = models.SlugField(
        _("Slug of the title"), max_length=250, null=True, blank=True,
    )
    price = models.DecimalField(
        _("Product Price"), decimal_places=2, max_digits=10, null=True, blank=True
    )
    discount = models.IntegerField(
        _("Discount % on product"), null=True, blank=True, default=0
    )
    discount_price = models.IntegerField(
        _("Discount price after Subtract Percentage"), null=True, blank=True, default=0
    )
    image = models.ImageField(upload_to=image_file_path, blank=True)
    description = HTMLField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    views = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    tags = TaggableManager(_("Write Tags Of Product seprate with ,"), blank=True)
    deleted_at = models.DateTimeField(_("deleted at"), null=True, blank=True)

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_related_products(self):
        title_split = self.title.split(" ")
        lookups = Q(title__icontains=title_split[0])

        for i in title_split[1:]:
            lookups |= Q(title__icontains=i)

        # for i in self.tags.names():
        #     lookups |= Q(tag_list__title__icontains=i.title)

        related_products = (
            Product.objects.filter(lookups).distinct().exclude(id=self.id)
        )
        return related_products

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.discount:
            self.discount_price = self.price - (self.price * discount / 100)
        super(Product, self).save(*args, **kwargs)

