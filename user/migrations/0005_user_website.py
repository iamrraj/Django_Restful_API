# Generated by Django 2.2.8 on 2020-07-12 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_is_verify'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='website',
            field=models.CharField(blank=True, max_length=240),
        ),
    ]