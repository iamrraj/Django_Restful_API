from django.contrib import admin
from .models import Personal ,Education, Work, Project,Skill,Language,Hobbies,Techonogie
# Register your models here.


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1
    # fields = '__all__'


class WorkInline(admin.TabularInline):
    model = Work
    extra = 1
    # fields = '__all__'


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1
    # fields = '__all__'


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    # fields = '__all__'


class LanguagIenline(admin.TabularInline):
    model = Language
    extra = 1
    # fields = '__all__'


class hobbiesInline(admin.TabularInline):
    model = Hobbies
    extra = 1
    # fields = '__all__'


class TechInline(admin.TabularInline):
    model = Techonogie
    extra = 1
    # fields = '__all__'


class AboutAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
    list_display = ['name', 'location', 'email', 'phone']
    list_filter = ['user', 'timestamp']
    search_fields = ['user__name', 'user__location',
                     'name', 'location', 'email', 'user__username']
    inlines = [EducationInline, WorkInline, ProjectInline,
               SkillInline, LanguagIenline, hobbiesInline, TechInline, ]


admin.site.register(Personal, AboutAdmin)
