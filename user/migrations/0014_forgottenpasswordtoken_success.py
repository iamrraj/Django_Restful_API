# Generated by Django 2.2.13 on 2020-10-30 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_forgottenpasswordtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='forgottenpasswordtoken',
            name='success',
            field=models.BooleanField(default=False),
        ),
    ]
