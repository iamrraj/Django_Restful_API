import uuid
import six
import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from ..models import Blog, Category, ImageStorage, BlogPhoto
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser

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


# class ImageSerializer(serializers.Serializer):
#     image = serializers.ListField(
#         child=serializers.FileField(max_length=100000,
#                                     allow_empty_file=False,
#                                     use_url=False)
#     )

#     def create(self, validated_data):
#         # blogs=ImageStorage.objects.latest('created_at')
#         image = validated_data.pop('image')
#         image = ImageStorage.objects.create(**validated_data)
#         # for img in image:
#         #     photo=Photo.objects.create(image=img,blogs=blogs,**validated_data)
#         # return photo
#         image.save()
#         return image


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(
                    data + '==========' * (-len(data) % 4))
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            # 12 characters are more than enough.
            file_name = str(uuid.uuid4())[:12]
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class BlogPhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    file = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, allow_empty_file=True,)
    # file = Base64ImageField(
    #     max_length=None,
    #     use_url=True,
    #     required=False,
    #     allow_null=True,
    #     allow_empty_file=True
    # )

    class Meta:
        model = BlogPhoto
        exclude = ['blog']

    def get_file(self, obj):
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)

    # def create(self, validated_data):
    #     validated_data['created_by'] = self.context['request'].user
    #     return super().create(validated_data)


class PhotoBlogSerializer(serializers.ModelSerializer):
    blog_photo = BlogPhotoSerializer(
        many=True, source="blogphoto_set", required=False
    )

    class Meta:
        model = Blog
        fields = ["blog_photo"]

    def create(self, validated_data):

        if "blogphoto_set" in validated_data:
            cps = validated_data.pop("blogphoto_set")
        else:
            cps = []

        instance = super().create(validated_data)

        for cp in cps:
            instance.blogphoto_set.create(**cp)

        return instance

    def update(self, instance, validated_data):
        if 'blogphoto_set' in validated_data:
            ids_set = [ndata['id']
                       for ndata in validated_data['blogphoto_set'] if 'id' in ndata]
            instance.blogphoto_set.exclude(id__in=ids_set).delete()
            for ndata in validated_data['blogphoto_set']:
                if ndata.get('id'):
                    note = instance.blogphoto_set.get(id=ndata['id'])
                    ndata.pop('id')
                else:
                    note = BlogPhoto(
                        blog=instance, created_by=self.context['request'].user)
                for k, v in ndata.items():
                    setattr(note, k, v)
                note.save()
            validated_data.pop('blogphoto_set')

        return super().update(instance, validated_data)


class ImageSerializer(serializers.ModelSerializer):

    parser_classes = (FormParser, MultiPartParser, FileUploadParser, )
    """Serializer for object image  info"""
    class Meta:
        model = ImageStorage
        exclude = (

            "deleted_at",

        )


class BlogAuthorSerializer(serializers.ModelSerializer):
    """Serializer for object author info"""

    class Meta:
        model = get_user_model()
        fields = ("username", "fullname", "profile_pic", "bio", "website")


class WriteBlog(serializers.ModelSerializer):
    tags = TagSerializerField()
    # photo = serializers.ImageField(max_length=None, allow_empty_file=True)

    class Meta:
        model = Blog
        fields = (
            "title",
            "header",
            "slug",
            "tags",
            "photo",
            "language",
            "blog_body",
            "description",
            "schedule",
            "publish",
            "category",
        )

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        instance = super(WriteBlog, self).create(validated_data)
        instance.tags.set(*tags)
        return instance


class BlogSerializer(serializers.ModelSerializer):

    get_tags = serializers.ListField(read_only=True)
    status = serializers.CharField(read_only=True)
    get_category_name = serializers.CharField(read_only=True)
    author = BlogAuthorSerializer(read_only=True)
    number_of_likes = serializers.IntegerField(read_only=True)
   # recommendations = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        exclude = (
            "request",
            "seen_at",
            "key",
            "publish",
            "schedule",
            "deleted_at",
            "verified",
            "category",
            "photo_url",
            "post_like",
            "sent_at"
        )
        read_only_fields = (
            "read_time",
            "timestamp",
            "verified",
            "number_of_likes",
            "views",
            "photo_url",
        )
