from rest_framework import serializers
from Post.models import Post, Comment
from blog.models import Blog
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.auth.tokens import default_token_generator
from blog.api.serializers import BlogSerializer
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class PhoneNumberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields =['phone_number']

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class UserSignUpSerializer(serializers.ModelSerializer):
    """DRF Serializer For User Registration"""

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
        ]  # You can add here first_name ,last_name

    def create(self, validated_data):
        password = validated_data.pop("password")
        user_instance = User.objects.create(**validated_data)
        user_instance.set_password(password)
        user_instance.is_active = False
        user_instance.token = default_token_generator.make_token(user_instance)
        user_instance.send_confirmation_email()
        user_instance.save()
        return user_instance


class ProfileInfoSerializer(serializers.ModelSerializer):
    """Serializer for the user settings objects"""

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "username",
            "password",
            "phone_number",
            "private_account",
            "website",
            "fullname",
            "bio",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "allow_null": True,
                "required": False,
                "min_length": 5,
            },
            "username": {"min_length": 3},
        }

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserPostsSerializer(serializers.ModelSerializer):
    number_of_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "photo",
            "text",
            "location",
            "number_of_likes",
            "number_of_comments",
            "posted_on",
        )

    def get_number_of_comments(self, obj):
        return Comment.objects.filter(post=obj).count()


class UserBlogProfileSerializer(serializers.ModelSerializer):
    number_of_posts = serializers.SerializerMethodField()
    blog_post_list = serializers.SerializerMethodField(
        "paginated_user_posts", source="post"
    )
    followed_by_req_user = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "fullname",
            "phone_number",
            "website",
            "is_verify",
            "bio",
            "profile_pic",
            "number_of_followers",
            "number_of_following",
            "number_of_posts",
            "blog_post_list",
            "followed_by_req_user",
        ]

    def get_number_of_posts(self, obj):
        return Blog.objects.filter(author=obj).count()

    def paginated_user_posts(self, obj):
        page_size = 20
        paginator = Paginator(obj.post.all(), page_size)
        page = self.context["request"].query_params.get("page") or 1

        post = paginator.page(page)
        serializer = BlogSerializer(post, many=True)

        return serializer.data

    def get_followed_by_req_user(self, obj):
        user = self.context["request"].user
        return user in obj.followers.all()


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing a user posts"""

    number_of_posts = serializers.SerializerMethodField()
    followed_by_req_user = serializers.SerializerMethodField()
    user_posts = serializers.SerializerMethodField("paginated_user_posts")
    

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "fullname",
            "phone_number",
            "website",
            "is_verify",
            "bio",
            "profile_pic",
            "number_of_followers",
            "number_of_following",
            "number_of_posts",
            "user_posts",
            "followed_by_req_user",
            "private_account",
            "is_superuser"
        )

  
    def get_number_of_posts(self, obj):
        return Post.objects.filter(author=obj).count()

    def paginated_user_posts(self, obj):
        page_size = 20
        paginator = Paginator(obj.user_posts.all(), page_size)
        page = self.context["request"].query_params.get("page") or 1

        user_posts = paginator.page(page)
        serializer = UserPostsSerializer(user_posts, many=True)

        return serializer.data

    def get_followed_by_req_user(self, obj):
        user = self.context["request"].user
        return user in obj.followers.all()


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for listing all followers"""

    class Meta:
        model = get_user_model()
        fields = ("username", "profile_pic")


class AllUserListSerializer(serializers.ModelSerializer):

    # last_login_time = serializers.SerializerMethodField()
    # client_ip = serializers.SerializerMethodField()

    # def get_last_login_time(self, obj):
    #     last_login = obj.last_login.last()
    #     if last_login is not None:
    #         return last_login.time
    #     return None

    # def get_client_ip(self,request):
    #     x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    #     if x_forwarded_for:
    #         print("returning FORWARDED_FOR")
    #         ip = x_forwarded_for.split(",")[-1].strip()
    #     elif request.META.get("HTTP_X_REAL_IP"):
    #         print("returning REAL_IP")
    #         ip = request.META.get("HTTP_X_REAL_IP")
    #     else:
    #         print("returning REMOTE_ADDR")
    #         ip = request.META.get("REMOTE_ADDR")
    #     return ip

    class Meta:
        model = get_user_model()
        fields = "__all__"

