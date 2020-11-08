
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext


class SubscribeModel(models.Model):
    sys_id = models.AutoField(primary_key=True, null=False, blank=True)
    email = models.EmailField(_("Subscribed user email"),null=False, blank=True, max_length=200, unique=True)
    status = models.CharField(_("Subscribed or  Unsubscribe")max_length=64, null=False, blank=True)
    created_date = models.DateTimeField(null=False, blank=True)
    updated_date = models.DateTimeField(null=False, blank=True)

    class Meta:
        app_label = "appname"
        db_table = "appname_subscribe"

    def __str__(self):
        return self.email