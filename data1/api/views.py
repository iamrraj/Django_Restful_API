from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import generics
from . import serializers
from rest_framework import filters
from ..models import Personal, Education, Work, Project, Skill, Language, Hobbies, Techonogie
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import viewsets


class ResumeView(generics.ListCreateAPIView):
    queryset = Personal.objects.all()
    serializer_class = serializers.AddSerializer


class ResumeViewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Personal.objects.all()
    serializer_class = serializers.AddSerializer


class ResumeViewUser(generics.ListCreateAPIView):
    queryset = Personal.objects.all()
    serializer_class = serializers.AddSerializer

    def get_queryset(self):
        return Personal.objects.filter(user=self.request.user).order_by('-timestamp')
