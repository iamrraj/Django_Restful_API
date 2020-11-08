from rest_framework import serializers
from ..models import Category,Product

from rest_framework_jwt.settings import api_settings

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class TagSerializerField(serializers.ListField):
    
    child = serializers.CharField()

    def to_representation(self, data):
        return data.values_list("name", flat=True)

