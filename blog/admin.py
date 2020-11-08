from django.contrib import admin
from django.conf import Settings
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import Blog, Category, FavoriteBlog, ImageStorage, BlogPhoto


# Register your models here.


class BlogPhotoAdmin(admin.ModelAdmin):
    model = BlogPhoto
    list_display = [
        "id",
        "name",
        "blog",
        "file",
    
    ]
    list_per_page = 25
    
admin.site.register(BlogPhoto, BlogPhotoAdmin)
    



class BlogAdmin(admin.ModelAdmin):
    model = Blog
    list_display = [
        "title",
        "language",
        "author",
        "category",
        "verified",
        "schedule",
        "deleted_at",
    ]
    # prepopulated_fields = {'slug': ('title',)}
    list_filter = ["timestamp", "language", "author", "verified"]
    search_fields = ("title", "author", "language", "category")
    # date_hierarchy = 'created_at'
    list_per_page = 25
    actions = [
        "undelete",
    ]

    def undelete(self, request, queryset):
        queryset.update(deleted_at=None)

    undelete.description = "Undelete notifications."

    def get_queryset(self, request):
        return self.model.objects.all()


class ImageAdmin(admin.ModelAdmin):
    model = Blog
    list_display = [
        "image",
        "title",
    ]
    list_per_page = 25
    actions = [
        "undelete",
    ]
    def undelete(self, request, queryset):
        queryset.update(deleted_at=None)
    undelete.description = "Undelete notifications."
    def get_queryset(self, request):
        return self.model.objects.all()

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category)
admin.site.register(FavoriteBlog)
admin.site.register(ImageStorage,ImageAdmin)
