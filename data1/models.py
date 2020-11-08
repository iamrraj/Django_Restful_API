from django.conf import settings
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Personal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE,
        null=True, blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(null=True, blank=True)
    name = models.CharField(blank=True,
                            max_length=240, help_text="Your Name")
    location = models.CharField(
        blank=True, max_length=240, help_text="You Location Where you stay")
    github = models.URLField(blank=True,
                             help_text="Your gihub Link")
    phone = models.CharField(blank=True,
                             max_length=240, help_text="Your Phone Nummer")
    email = models.EmailField(blank=True,
                              help_text="Your email address")
    web = models.URLField(blank=True,
                          help_text="Your Portfolio link")
    linkedin = models.URLField(
        blank=True, help_text="Your linkedin link")
    skype = models.CharField(blank=True,
                             max_length=240, help_text="Your skype id")
    about = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Education(models.Model):
    personal = models.ForeignKey(Personal, models.CASCADE)
    # date = models.DateField(blank=True)
    university = models.CharField(blank=True,
                                  max_length=240, help_text="University Name")
    majorsubject = models.CharField(blank=True,
                                    max_length=240, help_text="Major Subject Name (CS, ME, Civil...)")
    degree = models.CharField(blank=True,
                              max_length=240, help_text="Degree Name (Bachelor, Master ..)")
    startyear = models.DateField(blank=True, null=True)
    endyear = models.DateField(blank=True, null=True)
    grade = models.FloatField(blank=True, null=True, default=0)
    total = models.IntegerField(blank=True, null=True, default=0)
    ulocation = models.CharField(blank=True,
                                 max_length=240, help_text="Location Of Your University", default=".")


class Work(models.Model):
    personal = models.ForeignKey(Personal, models.CASCADE)
    postion = models.CharField(blank=True,
                               max_length=240, help_text="Job postion")
    cname = models.CharField(blank=True,
                             max_length=240, help_text="Compnay Name")
    employe = models.CharField(blank=True,
                               max_length=240, help_text="Type of job(fulltime, parttime,...)")
    startdate = models.DateField(blank=True,null=True,)
    enddate = models.DateField(blank=True,null=True,)
    wlocation = models.CharField(blank=True,
                                 max_length=240, help_text="Work Location Name")
    description = models.TextField(null=True, blank=True)


class Project(models.Model):
    personal = models.ForeignKey(Personal, models.CASCADE)
    title = models.CharField(blank=True,
                             max_length=240, help_text="Title Of the project")
    projectdetails = models.TextField(null=True, blank=True)
    link = models.URLField(
        blank=True, help_text="Link Of the project")


class Language(models.Model):

    personal = models.ForeignKey(Personal, models.CASCADE)
    language = models.CharField(blank=True,
                                max_length=240, help_text="Language name that you know")
    level = models.CharField(blank=True,
                             max_length=240, help_text="Level of your langauge")


class Skill(models.Model):
    personal = models.ForeignKey(Personal, models.CASCADE)
    skilss = models.CharField(blank=True,
                              max_length=240, help_text="Skill that You know")


class Hobbies(models.Model):

    personal = models.ForeignKey(Personal, models.CASCADE)
    intrest = models.CharField(
        blank=True, max_length=240, help_text="Skill that You know")


class Techonogie(models.Model):
    personal = models.ForeignKey(Personal, models.CASCADE)
    tech = models.CharField(blank=True,
                            max_length=240, help_text="Skill that You know")
