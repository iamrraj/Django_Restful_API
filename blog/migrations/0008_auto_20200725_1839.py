# Generated by Django 2.2.8 on 2020-07-25 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20200725_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='request',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='seen_at',
            field=models.DateTimeField(null=True),
        ),
    ]
