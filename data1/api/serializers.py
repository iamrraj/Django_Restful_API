from rest_framework import serializers
from ..models import Personal, Education, Work, Project, Skill, Language, Hobbies, Techonogie
from django.contrib.auth.models import User
from blog.api.serializers import Base64ImageField


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ['personal']


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        exclude = ['personal']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ['personal']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        exclude = ['personal']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        exclude = ['personal']


class HobbiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobbies
        exclude = ['personal']


class TechSerializer(serializers.ModelSerializer):

    class Meta:
        model = Techonogie
        exclude = ['personal']


class PersonalSerializers(serializers.ModelSerializer):
    photo = Base64ImageField(
        max_length=None,
        use_url=True,
        required=False,
        allow_null=True,
        allow_empty_file=True
    )
    class Meta:
        model = Personal
        exclude = ['user']

    def get_file(self, obj):
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AddSerializer(PersonalSerializers):
    educations = EducationSerializer(
        many=True, source='education_set', required=False)
    works = WorkSerializer(many=True, source='work_set', required=False)
    projects = ProjectSerializer(
        many=True, source='project_set', required=False)
    languages = LanguageSerializer(
        many=True, source='language_set', required=False)
    skills = SkillSerializer(many=True, source='skill_set', required=False)
    hobbies = HobbiesSerializer(
        many=True, source='hobbies_set', required=False)

    def create(self, validated_data):
        if 'education_set' in validated_data:
            educations = validated_data.pop('education_set')
        else:
            educations = []
        if 'work_set' in validated_data:
            works = validated_data.pop('work_set')
        else:
            works = []

        if 'project_set' in validated_data:
            projects = validated_data.pop('project_set')
        else:
            projects = []

        if 'language_set' in validated_data:
            languages = validated_data.pop('language_set')
        else:
            languages = []
        if 'skill_set' in validated_data:
            skills = validated_data.pop('skill_set')
        else:
            skills = []
        if 'hobbies_set' in validated_data:
            hobbies = validated_data.pop('hobbies_set')
        else:
            hobbies = []

        instance = super().create(validated_data)

        for ed in educations:
            instance.education_set.create(**ed)

        for wd in works:
            instance.work_set.create(**wd)

        for pd in projects:
            instance.project_set.create(**pd)

        for ld in languages:
            instance.language_set.create(**ld)

        for sd in skills:
            instance.skill_set.create(**sd)

        for hd in hobbies:
            instance.hobbies_set.create(**hd)

        return instance


class PersonalItemSerializer(AddSerializer):
    educations = EducationSerializer(
        many=True, source='education_set', write_only=True, required=False)
    works = WorkSerializer(many=True, source='work_set',
                           write_only=True, required=False)
    projects = ProjectSerializer(
        many=True, source='project_set', write_only=True, required=False)
    languages = EducationSerializer(
        many=True, source='language_set', write_only=True, required=False)
    skills = WorkSerializer(many=True, source='skill_set',
                            write_only=True, required=False)
    hobbies = ProjectSerializer(
        many=True, source='hobbies_set', write_only=True, required=False)
