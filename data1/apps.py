from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DataConfig(AppConfig):
    name = 'data1'
    verbose_name = _('Data1')
