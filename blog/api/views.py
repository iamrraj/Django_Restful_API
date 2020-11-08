import json
from django.http import QueryDict
from rest_framework.response import Response
from ..models import Blog, FavoriteBlog, ImageStorage, BlogPhoto

# from user.models import Profile
# from user.api.serializers import ProfileSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import generics
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.views import APIView
from drf_multiple_model.views import (
    ObjectMultipleModelAPIView,
    FlatMultipleModelAPIView,
)
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now
from rest_framework import filters
from .serializers import BlogSerializer, WriteBlog, BlogAuthorSerializer, ImageSerializer, PhotoBlogSerializer
from django_filters.rest_framework import DjangoFilterBackend
import django_filters.filters
import django_filters.rest_framework
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Case, Value, When, F
from django.utils.timezone import now
from Post.api.permission import IsOwnerOrReadOnly, IsOwnerOrPostOwnerOrReadOnlyBlog
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework import parsers


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class BlogFilter(django_filters.FilterSet):
    result = django_filters.CharFilter(
        method="my_custom_filter", label="Username Email, name"
    )
    status = django_filters.ChoiceFilter(
        choices=[("active", "active"), ("schedule", "schedule")],
        method="filter_status",
        label="Staus",
    )

    class Meta:
        model = Blog
        fields = ["result", "tags__name", "language", "category", "author"]

    def filter_status(self, qs, name, value):
        if value == "active":
            return qs.filter(schedule__lte=now())
        if value == "schedule":
            return qs.filter(schedule__gte=now())
        return qs

    def my_custom_filter(self, queryset, name, value):
        return Blog.objects.filter(
            Q(title__icontains=value)
            | Q(description__icontains=value)
            | Q(tags__name__icontains=value)
        )


# class ProfileView(generics.ListAPIView):
#     serializer_class = ProfileSerializer

#     def get_queryset(self):
#         queryset = Profile.objects.filter(blog__author=self.request.user)
#         return queryset


class CreateBlog(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WriteBlog

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogImagelView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PhotoBlogSerializer
    # parser_classes = [FileUploadParser]

    def post(self, request):
        # file_contents = SimpleUploadedFile("%d.jpg" % request.user.id, request.body, "image/jpeg")
        # request.user.avatar.save("%d.jpg" % request.user.id, file_contents, save=True)
        newFile.file = request.data['file']
        newFile.save()
        return HttpResponse('file upload success')

    # def put(self, request, filename, format=None):
    #     newFile = File()
    #     newFile.file = request.data['file']
    #     newFile.save()
    #     return HttpResponse('file upload success')

    def get_queryset(self):
        return Blog.objects.all()


class MultipartJsonParser(parsers.MultiPartParser):
    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        data = {}
        # find the data field and parse it
        data = json.loads(result.data["data"])
        qdict = QueryDict('', mutable=True)
        qdict.update(data)
        return parsers.DataAndFiles(qdict, result.files)


class BlogImagel1View(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PhotoBlogSerializer
  #  parser_classes = (MultiPartParser,)
    parser_classes = (MultiPartParser, FormParser)

    # def put(self, request, format=None, *args, **kwargs):
    #     image = request.FILES.get('file')
    #     name = request.data.get("name")
    #     BlogPhoto.objects.create(name=name, file=image)
    #     return Response({'name:': obj.name}, status=201)

    def get_queryset(self):
        return Blog.objects.all()


class EditBlog(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = WriteBlog

    def get_queryset(self):
        return Blog.objects.filter(deleted_at=None)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ImageListView(generics.ListCreateAPIView):
    parser_classes = (MultiPartParser, JSONParser,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageSerializer

    def get_queryset(self):
        return ImageStorage.objects.filter(deleted_at=None).order_by(
            "-timestamp"
        )

    def delete(self, request, pk):
        ImageStorage.objects.filter(pk=pk).update(deleted_at=now())
        return Response({})


class BlogViewList(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BlogFilter

    def get_queryset(self):
        return Blog.objects.filter(deleted_at=None).order_by(
            "-timestamp"
        )  # author=self.request.user,


class BlogView(generics.ListCreateAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BlogFilter

    def get_queryset(self):
        return Blog.objects.filter(deleted_at=None).order_by("-timestamp")

    # def perform_create(self, serializer):
    #     created_object = serializer.save()
    #     send_mail(
    #         "Subject here",
    #         "Here is the message.",
    #         "from@example.com",
    #         [created_object.email],
    #         fail_silently=False,
    #     )

    # def put(self, request):
    #     self.filter_queryset(self.get_queryset()).update(isRead=Q(isRead=False))
    #     return Response({})


class BlogDetailView(generics.RetrieveDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (IsOwnerOrPostOwnerOrReadOnlyBlog,)
    serializer_class = BlogSerializer

    def get_queryset(self):
        return Blog.objects.filter(deleted_at=None)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Blog.objects.filter(pk=instance.pk).update(views=F("views") + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, pk):
        Blog.objects.filter(author=self.request.user,
                            pk=pk).update(deleted_at=now())
        return Response({})


class BlogLike(APIView):
    def get(self, request, format=None, pk=None):
        post = Blog.objects.get(pk=pk)
        user = self.request.user
        if user.is_authenticated:
            if user in post.post_like.all():
                like = False
                post.post_like.remove(user)
            else:
                like = True
                post.post_like.add(user)
        data = {"like": like}
        return Response(data)


class FavoriteBllog(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None, pk=None):
        post = FavoriteBlog.objects.get(pk=pk)
        blog = Blog.objects.filter(author=self.request.user)
        if user.is_authenticated:
            if user in post.favorite_blog.all():
                like = False
                post.favorite_blog.remove(user)
            else:
                like = True
                post.favorite_blog.add(user)
        data = {"like": like}
        return Response(data)


class GetLikersView(generics.ListAPIView):
    serializer_class = BlogAuthorSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        pk = self.kwargs["pk"]
        queryset = Blog.objects.get(pk=pk).post_like.all()
        return queryset
