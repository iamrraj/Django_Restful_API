from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from django.contrib.auth.forms import PasswordResetForm
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import serializers

User = get_user_model()


def confirm(request, key):
    profile = get_object_or_404(User, token=key)
    if profile.is_active:
        return redirect("https://front-beta.digitalfleet.eu/")
    else:
        try:
            profile.is_active = True
            profile.send_welcome_email()
            profile.save()
            return render(request, "user/confirm.html")
        except Exception as e:
            pass


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordReset(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        f = PasswordResetForm({"email": serializer.validated_data['email']})
        f.is_valid()
        f.save(use_https=True, request=request)
        return Response({})

   
