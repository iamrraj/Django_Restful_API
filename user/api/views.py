import django_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import (
    UserSignUpSerializer,
    ProfileInfoSerializer,
    UserProfileSerializer,
    FollowSerializer,
    AllUserListSerializer,
    UserBlogProfileSerializer,
    ChangePasswordSerializer,
    PhoneNumberSerializer
)
from pytz import utc
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
import django_filters.filters
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
import pyotp
from twilio.rest import Client as TwilioClient
from instaclone.response import error_json_response
from ..models import ForgottenPasswordToken,UserPasswordHistory
from rest_framework import serializers
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

# from decouple import config
from datetime import date,datetime
User = get_user_model()


class Userilter(django_filters.FilterSet):
    result = django_filters.CharFilter(
        method="my_custom_filter", label="Username Email, name"
    )

    class Meta:
        model = User
        fields = ["username"]

    def my_custom_filter(self, queryset, name, value):
        return User.objects.filter(
            Q(username__icontains=value)
            | Q(fullname__icontains=value)
            | Q(email__icontains=value)
        )


class UpdatePassword(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return error_json_response(request, 400, "Old Password is wrong")  

            for p in UserPasswordHistory.objects.filter(user=self.object):
                if check_password(serializer.data.get("new_password"), p.password):
                    return  error_json_response(request, 400, "You can not change your password to the previously used one.") 
            
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            UserPasswordHistory.objects.create(user=self.object, password=self.object.password).save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowersLikersPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 5000


class UserSignUpView(generics.CreateAPIView):
    """View For User Registration"""

    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    def get(self, request):
        return Response(
            {
                "minPasswordChars": 8,
                "tos": "https://digitalfleet.eu/legal/tos_eng.html",
                "privacyPolicy": "https://digitalfleet.eu/legal/privacy_eng.html",
                "help": "https://digitalfleet.eu/legal/help_eng.html",
            }
        )

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return error_json_response(
                request, 400, ("All field is required")
            )
        # elif password != password1 or not password:
        #     return Response({'detail': 'Error Setting The Password'}, status=status.HTTP_400_BAD_REQUEST)

        elif User.objects.filter(email=email).exists():
            return error_json_response(request, 400, ("Email already in use"))

        else:
            serializer = UserSignUpSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                u = User.objects.get(username=serializer.data['username'], email=serializer.data['email'])
                don = UserPasswordHistory.objects.create(user=u, password=u.password)
                don.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileInfoSerializer

    def get_object(self):
        return self.request.user


class UserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = get_user_model().objects.all()
    serializer_class = AllUserListSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = Userilter


class UserProfileView(generics.RetrieveAPIView):
    lookup_field = "username"
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.AllowAny,)


class UserBlogProfileView(generics.RetrieveAPIView):
    lookup_field = "username"
    queryset = get_user_model().objects.all()
    serializer_class = UserBlogProfileSerializer
    permission_classes = (permissions.AllowAny,)


class FollowUserView(APIView):
    def get(self, request, format=None, username=None):
        to_user = get_user_model().objects.get(username=username)
        from_user = self.request.user
        follow = None
        if from_user.is_authenticated:
            if from_user != to_user:
                if from_user in to_user.followers.all():
                    follow = False
                    from_user.following.remove(to_user)
                    to_user.followers.remove(from_user)
                else:
                    follow = True
                    from_user.following.add(to_user)
                    to_user.followers.add(from_user)
        data = {"follow": follow}
        return Response(data)


class GetFollowersView(generics.ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = FollowersLikersPagination
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        username = self.kwargs["username"]
        queryset = get_user_model().objects.get(username=username).followers.all()
        return queryset


class GetFollowingView(generics.ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = FollowersLikersPagination
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        username = self.kwargs["username"]
        queryset = get_user_model().objects.get(username=username).following.all()
        return queryset


class PhoneViewset(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = PhoneNumberSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        '''Associate user with phone number'''

        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def send_sms_code(request, format=None):

    # Time based otp
    time_otp = pyotp.TOTP(request.user.key, interval=300)
    time_otp = time_otp.now()
    user_phone_number = request.user.phonenumber.number  # Must start with a plus '+'
    client.messages.create(
        body="Your verification code is "+time_otp,
        from_=twilio_phone,
        to=user_phone_number
    )
    return Response(status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def verify_phone(request, sms_code, format=None):
    code = int(sms_code)
    if request.user.authenticate(code):
        phone = request.user.phonenumber
        phone.verified = True
        phone.save()
        return Response(dict(detail="Phone number verified successfully"), status=201)
    return Response(dict(detail='The provided code did not match or has expired'), status=200)





class SendForgottenPasswordEmail(APIView):
    class serializer_class(serializers.Serializer):
        email = serializers.CharField()

    def post(self, request):
        try:
            data = request.data
            data.get
        except (KeyError, ValueError, AttributeError):
            return error_json_response(request, 400, "Need valid JSON dictionary.")

        email = data.get("email")
        limit_per_day = 5

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return error_json_response(request, 404, ("User not found for this email."))

        tokens = user.forgottenpasswordtoken_set.filter(token_end_date__date__gte=date.today()).count()
        if tokens > limit_per_day:
            return error_json_response(request, 409, ("Limit for password restore requests reached. Please try again later."))

        token = ForgottenPasswordToken(
            user=user,
            ip_address=request.META['REMOTE_ADDR']
        )
        token.save()
        token.send_email()

        return error_json_response(request, 202, f"Email Send Successfully to {email}")



class ChangeForgottenPassword(APIView):
    class serializer_class(serializers.Serializer):
        password = serializers.CharField()
        token = serializers.CharField()

    def post(self, request):
        try:
            data = request.data
            data.get
        except (KeyError, ValueError, AttributeError):
            return error_json_response(request, 400, "Need valid JSON dictionary.")

        password = data.get('password')
        token_value = data.get('token')

        if not password:
            return error_json_response(request, 400, "Password cannot be empty.")

        if not token_value:
            return error_json_response(request, 400, "Token cannot be empty.")
        
        try:
            token = ForgottenPasswordToken.objects.get(token_value=token_value)
        except ForgottenPasswordToken.DoesNotExist:
            return error_json_response(request, 409, "Token not found.")

        if password:
            for p in UserPasswordHistory.objects.filter(user=token.user):
                    if check_password(password, p.password):
                        return error_json_response(request, 400, "You can not change your password to the previously used one.")
            uph = UserPasswordHistory.objects.filter(user=token.user).last()
            if not uph:
                print("no password history")
                uph = UserPasswordHistory.objects.create(user=token.user, password=make_password(password))
                uph.created_at = token.user.date_joined
                uph.save()
            else:
                UserPasswordHistory.objects.create(user=token.user, password=make_password(password)).save()
       
        token.user.set_password(password)
        token.user.save()
        token.success = True
        token.token_end_date = datetime.now(tz=utc)
        token.save()

        
       
        return error_json_response(request, 202, f"Password changed successfully ")
